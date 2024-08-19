import numpy as np
import os
import copy
from .helper_func import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle
from bisect import bisect
from typing import TextIO
import numbers
from typing import Literal, get_args

class FieldData():
    '''
    Class to create a field data file (\*_gaca.fd.txt) as input for TSWC-GACA.
    Later on the following methods need to be performed for each instance of the class.
    For each step the according methods will check for correct inputs and prevent error in the exported txt-file.

    Workflow for Generating field data.

    ---- 1. BOREHOLE ----
        1. 'add_boreholeVector'
        2. 'add_radialComment' (optional)
        3. 'add_boreholeInclination'
        4. 'add_materialProperty' (depending on vertical discretisation)
        5. 'add_temperature' - borehole
    ---- 2. CAVNERN ----
        1. 'add_cavernVector'
        2. 'add_temperature' - cavern
        3. 'add_cavernCharacteristics'

    ---- The last step is to export the field data to an txt-file with the method 'export_fieldData'. ----
    '''

    #: Doc comment for class attribute Foo.bar.
    #: It can have multiple lines.
    def __init__(self, n_fluid:int, tvd:float, delta_z:float,
                 medium_type:str,medium_id:str):
        """Initialise GacaFieldData class.

        :param n_boreholes:  usually 1
        :type n_boreholes: int
        :param n_fluid: how many flow spaces (Strömungsräume)
        :type n_fluid: int
        :param tvd: maximum TVD of the borehole
        :type tvd: float
        :param delta_z: vertical discretisation of TVD_max
        :type delta_z: float
        :param medium_type_cavern: Which medium type (must be 'GAS')
        :type medium_type_cavern: str
        :param medium_id_cavern: which substance (defined in fluid library of TSWC)
        :type medium_id_cavern: str
        """        

        self.n_fluid            = n_fluid
        self.p_borehole         = int(np.round(tvd / delta_z))
        self.delta_z    	    = delta_z
        self.medium_type        = medium_type
        self.medium_id          = medium_id

        self.m_borehole         = -1   # specified later, -1 for assertation purpose
        self.m_cavern           = -1
        self.tvd   = tvd
        self.radialComment      = None


        self.materialNames = [''] * self.p_borehole

        self.radial_vector_borehole    = [] 
        self.heat_capacity             = None
        self.thermal_conductivity      = None
        self.bottom_edge_vertical = np.linspace(start=0, stop=self.tvd, num = self.p_borehole + 1)[1:]

        # for format
        self._vspace = '\n\n'

    def add_boreholeVector(self,radial_vector, aggregate_state): #TODO: Unit conversion
        """Adds a radial vector within the borehole [m] and respective aggregate states ('FLUID' or 'SOLID').

        :param radial_vector: must be strictly increasing, will define self.m_borehole [int].
        :type radial_vector:  list or array [m] 
        :param aggregate_state: list of strings either 'FLUID' or 'SOLID'.
                                Does not need to have the same length as radial_vector.
                                Remaining values will be filled with 'SOLID'.
        :type aggregate_state: string array
        """      

        assert all(i < j for i, j in zip(radial_vector, radial_vector[1:])), 'List is not strictly increasing!'
        self.radial_vector_borehole    = radial_vector
        self.m_borehole                = radial_vector.shape[0]

        # Create vector for aggregate states (column_character_borehole), check spelling
        column_character_borehole = []
        for element in aggregate_state:
            state = element.upper()
            assert state in ['FLUID', 'SOLID'], 'Rechtschreibfehler in column_character_borehole %s' %(element)
            column_character_borehole.append(state)

        assert column_character_borehole.count('FLUID') == self.n_fluid, '"FLUID" does not match self.n_fluid!'
        
        diff = self.m_borehole - len(column_character_borehole) 
        if diff > 0 : # Fill remaining values with 'SOLID' so user only needs to define states near construction (formation points are always solid)
        
            for _ in range(diff):
                column_character_borehole.append('SOLID')
            
        self.column_character_borehole = column_character_borehole

        # pre-allocate space for material properties
        self.thermal_conductivity = np.ones((self.p_borehole, self.m_borehole))*-1 
        self.heat_capacity        = np.ones((self.p_borehole, self.m_borehole))*-1 
       

    def add_radialComment(self,radialComment):
        """Add comments for radial borehole vector. Will be displayed lather in txt file (OPTIONAL - for overview purpose only).
        If the array has a length of e.g. 5, then the comment is valid for the first five radial elements.
        

        :param radialComment: E.g. ['ID 858','OD 858','ID 1134', 'ZEMENT', 'FORMATION']
        :type radialComment: array
        """      
        self.radialComment = radialComment



    def add_boreholeInclination(self,inclination):
        """Add inclination for borehole

        :param inclination: either array [1 x p_borehole] with deg data or 'vertical'
        :type inclination: array [1xp_borehole] oder 'vertical'
        """        
        if type(inclination) == str: 
            self.inclination = np.zeros([self.p_borehole,1])
        else:
            self.inclination = inclination

    
    def add_materialProperty(self,top,bottom,heat_capacity,thermal_conductivity,name=None):
        """Adds material properties to the borehole.
        The value for the center of gravity of the layer is then modeled, with indication in relation to the bottom edge of the layer. 
        Hierarchical; new values overwrite respective old values at the same intervals.

        :param top: start of layer [m]
        :type top: int or float
        :param bottom: end of layer [m]
        :type bottom: int or float
        :param heat_capacity:  [MJ/(m3K)]
        :type heat_capacity: array [1 x m_borehole]
        :param thermal_conductivity: [1 x m_borehole] 
        :type thermal_conductivity: [W/(m K)]
        :param name:  Name of the layer, will be displayed in .txt file when exported, defaults to None
        :type name: str, optional
        """        
        assert self.m_borehole > 0, 'Please define radial_vector_borehole via add_boreholeVector first.'
        assert heat_capacity.shape[0] == self.m_borehole, 'Fehler bei cp in %s' %(name)
        assert thermal_conductivity.shape[0] == self.m_borehole, 'Fehler bei T in %s' %(name)

        idx_top     = find_nearest(self.bottom_edge_vertical,top)
        idx_bottom  = find_nearest(self.bottom_edge_vertical,bottom)

        self.heat_capacity[idx_top:idx_bottom + 1,:]        = heat_capacity
        self.thermal_conductivity[idx_top:idx_bottom + 1,:] = thermal_conductivity

        if name is not None:
            for i in range(idx_top, idx_bottom + 1):
                self.materialNames[i] = name

    def initialise_formation(self, radial_vector_formation):
        """Initilise radial points for formation

        :param radial_vector_formation: radial points
        :type radial_vector_formation: array
        """
        if all(i < j for i, j in zip(radial_vector_formation, radial_vector_formation[1:])) == False:
            print('radial_vector is not strictly increasing, it will be sorted')
            radial_vector_formation = np.sort(radial_vector_formation)

        self.m_borehole = radial_vector_formation.shape[0]
        self.thermal_conductivity = np.zeros((self.p_borehole, self.m_borehole))
        self.heat_capacity        = np.zeros((self.p_borehole, self.m_borehole))
        self.radial_vector_borehole = radial_vector_formation

    def add_formation(self, top:float, bottom:float, material_data:dict, name:str = None):
        """Add Formation elements after having initilised formation.

        :param top: start of layer [m]
        :type top: float
        :param bottom: end of layer [m]
        :type bottom: float
        :param material_data: for example: {'rho': 1000, 'cp': 4180,'lambda': 0.6} Units respt. in [kg/m3],  [J/kg*K],  [W/(m*K)], 
        :type material_data: dict
        :param name: _description_, defaults to None
        :type name: str, optional
        """
        idx_top     = find_nearest(self.bottom_edge_vertical,top)
        idx_bottom  = find_nearest(self.bottom_edge_vertical,bottom)


        assert all(key in material_data for key in ['rho', 'cp', 'lambda'])

        self.heat_capacity[idx_top:idx_bottom + 1,:]        = material_data['rho'] * material_data['cp'] * 1e-6
        self.thermal_conductivity[idx_top:idx_bottom + 1,:] = material_data['lambda']

        if name is not None:
            for i in range(idx_top, idx_bottom + 1):
                self.materialNames[i] = name

    def add_element(self, starting_coor:tuple, end_coor:tuple, material_data:dict, name = None):
        """Add material properties of an element to the borehole model. 

        :param starting_coor: (z0, x0) - Top coordinates of element at the top left corner.
        :type starting_coor: tuple
        :param end_coor: (z1, x1) - Bottom coordinates of element at the bottom right corner.
        :type end_coor: tuple
        :param material_data: for example: {'rho': 1000, 'cp': 4180,'lambda': 0.6} Units respt. in [kg/m3],  [J/kg*K],  [W/(m*K)], 
        :type material_data: dict
        :param name: Name, defaults to None
        :type name: _type_, optional
        """
        assert all(key in material_data for key in ['rho', 'cp', 'lambda'])

        radial_vector_borehole = self.radial_vector_borehole
        thermal_conductivity   = self.thermal_conductivity
        heat_capacity          = self.heat_capacity

        # check if matrices have been initilized
        if np.any([heat_capacity is None, thermal_conductivity is None]):
            print('Please initilise the geological formation with the function initialise_formation() and add values to it with add_formation().')
            return
        
        # check all points have non-zero values in matrices
        # if np.any([np.nonzero(heat_capacity == 0), np.nonzero(thermal_conductivity == 0)]):
        #     print('There are still zero values in the matrices heat_capacity or thermal_conductivity. Please check that all points have been allocated with values.')
        #     return

        x0 = starting_coor[1]
        x1 = end_coor[1]
        z0 = starting_coor[0]
        z1 = end_coor[0]  

        z_i0 = find_nearest(self.bottom_edge_vertical, z0)
        z_i1 = find_nearest(self.bottom_edge_vertical, z1) + 1  # +1 due to slicing principle in python

        i_x_new = []
        for x_val in [x0, x1]:
            if x_val not in radial_vector_borehole: 
                i_new_temp = bisect(radial_vector_borehole, x_val)
                radial_vector_borehole = np.insert(radial_vector_borehole, i_new_temp, x_val) # add new x_val to radial borehole vector
                print('Inserted new radial point at %.4fm' % (x_val))
                if i_new_temp == thermal_conductivity.shape[1]:
                    new_col_therm = thermal_conductivity[:, -1]
                else:
                    new_col_therm = thermal_conductivity[:, i_new_temp]
                thermal_conductivity = np.insert(thermal_conductivity, i_new_temp, new_col_therm, axis = 1)

                if i_new_temp == heat_capacity.shape[1]:
                    new_col_heat = heat_capacity[:, -1]
                else:
                    new_col_heat = heat_capacity[:, i_new_temp]
                heat_capacity = np.insert(heat_capacity, i_new_temp, new_col_heat, axis = 1)

                i_x_new.append(i_new_temp)
            else:
                i_x_new.append(find_nearest(radial_vector_borehole, x_val))

        heat_capacity_val = material_data['rho'] * material_data['cp'] * 1e-6
        thermal_conductivity_val = material_data['lambda']

        thermal_conductivity[z_i0:z_i1, i_x_new[0] + 1:i_x_new[1] + 1] = thermal_conductivity_val
        heat_capacity[z_i0:z_i1, i_x_new[0] + 1:i_x_new[1] + 1]        = heat_capacity_val
        
        print('Updated values for points:')
        for z_val in self.bottom_edge_vertical[z_i0:z_i1]:
            print('- %.2f m |  ' %(z_val), end ='')
            for x_val in radial_vector_borehole[i_x_new[0] + 1:i_x_new[1] + 1]:
                print('%.3f m \t' %(x_val) , end = '')
            print('| c*rho = %.2f MJ/(K*m3) | lambda = %.2f W/(m*K)\n' %(heat_capacity_val, thermal_conductivity_val), end = "")

        if name is not None:
            for i in range(z_i0, z_i1):
                self.materialNames[i] += '_' + name

        self.thermal_conductivity      = thermal_conductivity
        self.heat_capacity             = heat_capacity
        self.radial_vector_borehole    = radial_vector_borehole
        self.m_borehole                = radial_vector_borehole.shape[0]
        self.column_character_borehole = ['SOLID'] * self.m_borehole

    def define_fluid_space(self, indices):
        """Define which elements of radial_borehole_vector are not 'SOLID'-

        :param indices: If integer -> index, if float -> search for closest match in radial_borehole_vector
        :type indices: int or float
        :param names: either 'FLUID' or ???
        :type names: string
        """
        if type(indices) is not list: indices = [ indices ]

        for idx in indices:
            if isinstance(idx, int):
                idx_temp = idx
            elif isinstance(idx, float):
                idx_temp = find_nearest(self.radial_vector_borehole, idx)
            else:
                print(f'Could not find any match for {idx}. Please check if it is either a int or float.')
                continue
            self.column_character_borehole[idx_temp] = 'FLUID'
            self.heat_capacity[:, idx_temp] = 0
            self.thermal_conductivity[:, idx_temp] = 0
            print('Set %.4f m as "FLUID". Material properties for this element are set to 0.' %(self.radial_vector_borehole[idx_temp]))


    def add_temperature(self, temperature, mode:str):
        """ Adds temperature data to the borehole or cavern.

        :param temperature: (p_borehole x m_borehole) array for 'borehole or
                        (m_cavern) for cavern 
        :type temperature: _type_
        :param mode: either 'borehole', 'cavern', 'reservoir'
        :type mode: str
        """    
        match mode:
            case 'borehole':
                assert self.m_borehole > 0, 'Please define radial_vector_borehole via add_boreholeVector first.'
                assert temperature.shape == (self.p_borehole, self.m_borehole)
                self.temperature_borehole = temperature

            case 'cavern':
                assert self.m_cavern > 0, 'Please define radial_vector_cavern via add_boreholeVector first.'
                assert temperature.shape == (self.m_cavern,)
                self.temperature_cavern = temperature

            case 'reservoir':
                assert isinstance(temperature, numbers.Number)
                self.temperature_reservoir = temperature

        print('Added Temperature')

    def plot_geometry(self, xlimits:list = None, export_folder:str = None):
        """Plots geometry.

        :param xlimits: start and end value of radial range, defaults to None
        :type xlimits: list, optional
        :param export_folder: Export plot data into folder, defaults to None
        :type export_folder: str, optional
        :return: Two figures for heat capacity * rho and lambda
        :rtype: fig_cp, fig_lambda
        """

        x = self.radial_vector_borehole
        y = self.bottom_edge_vertical  
        X,Y = np.meshgrid(np.insert(x, 0, 0), np.insert(y, 0, 0))

        colormap = mpl.colormaps.get_cmap('jet')
        colormap.set_bad('magenta')
        # heat capacity * rho
        fig_cp, ax = plt.subplots()
        fig_cp.canvas.manager.set_window_title('Geometry_HeatCapactiyRho') 
        Z = self.heat_capacity

        cm = ax.pcolormesh(X, Y, Z, cmap = colormap)
        
        ax.set_title('Dichte * spez. Wärmekapazität')
        plt.suptitle('Visualisierung der Modellgeometrie durch Stoffwertematrix')
        ax.set_xlabel('x [m] (Beginned ab Bohrlochachse)')
        ax.set_ylabel('z [m]')
        ax.invert_yaxis()

        if xlimits is not None:
            ax.set(xlim=xlimits)

        cbar = plt.colorbar(cm, ax = ax) #, format = '%.1f K', label = 'Temperature')
        cbar.ax.invert_yaxis()
        cbar.ax.set_title('[MJ/(K*m3)]', loc='center')
        
        # mplcursors.cursor(hover=2)
        # thermal conductivity
        fig_lambda, ax = plt.subplots()
        fig_lambda.canvas.manager.set_window_title('Geometry_ThermalConductivity') 
        Z = self.thermal_conductivity
        cm = ax.pcolormesh(X, Y, Z, cmap = colormap, vmax = 10)
        ax.set_title('Wärmeleitfähigkeit')
        plt.suptitle('Visualisierung der Modellgeometrie durch Stoffwertematrix')
        ax.set_xlabel('x [m] (Beginned ab Bohrlochachse)')
        ax.set_ylabel('z [m]')
        ax.invert_yaxis()
        if xlimits is not None:
            ax.set(xlim=xlimits)
        cbar = plt.colorbar(cm, ax = ax) #, format = '%.1f K', label = 'Temperature')
        cbar.ax.invert_yaxis()
        cbar.ax.set_title('[W/(m*K)]', loc='center')

        if export_folder is not None:
            if Path(export_folder).exists() and Path(export_folder).is_dir(): # it must be a valid path and a folder
                width  = 406 / 25.4 # inches
                height = 229 / 25.4 # inches
                dpi    = max([1536/width, 864/height])
                save_geom_path = Path(export_folder)

                fig_cp.set_size_inches(width, height)
                fig_cp.savefig(save_geom_path.joinpath('Geometry_HeatCapactiyRho.png'), dpi = dpi)
                print('Exported %s' %(save_geom_path.joinpath('Geometry_HeatCapactiyRho.png')))

                fig_lambda.set_size_inches(width, height)
                fig_lambda.savefig(save_geom_path.joinpath('Geometry_ThermalConductivity.png'), dpi = dpi)
                print('Exported %s' %(save_geom_path.joinpath('Geometry_ThermalConductivity.png')))   
            else:
                print('Für den Export bitte einen gültigen Ordnerpfad angeben.\n%s konnte nicht gefunden werden.\n' %(export_folder))

        return fig_cp, fig_lambda

    def _write_npMatrix2Fid(self, matrix,  fid, axis=1, bottom_edges=None):

        if matrix.ndim > 1 or axis == 0:
            for i,row in enumerate(matrix):
                row.tofile(fid,sep='\t',format='%.3f')
                if bottom_edges is not None:
                    fid.write('\t# UK %.2fm - %s' %(bottom_edges[i], self.materialNames[i]))
                fid.write('\n')    
        else:
            matrix.tofile(fid,sep='\t',format='%.4f')

    def _create_export_folder(self, save_folder:Path, project_name:str, suffix:str, is_binary_export:bool):
        save_path = save_folder.joinpath(project_name)
        if not (save_path.exists()):
            save_path.mkdir(parents=True, exist_ok=False)
            print('Created new folder %s' %(save_path))

        if is_binary_export:
            pickle_path = save_path.joinpath(project_name + '_fd.pickle')
            with open(pickle_path, 'wb') as f:
                pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
                print('Exported %s\n' %(pickle_path))

        return save_path.joinpath(project_name + suffix)
    
    def _export_meta_data(self, fid:TextIO):															
        fid.write('N_FLUID\t%d\n' %(self.n_fluid)	)														
        fid.write('M_BOREHOLE\t%d\t# (M)\n' %(self.m_borehole)	)														
        fid.write('P_BOREHOLE\t%d\t# (P)\n' %(self.p_borehole)	)															
        fid.write('DL\t%.4f\t# [m]\n' %(self.delta_z)	)

    def _export_borehole_data(self, fid:TextIO):
        fid.write('RADIAL_VECTOR_BOREHOLE # [m]\n')
        if self.radialComment is not None:
            fid.write('#%s\n' %('\t'.join(self.radialComment)))		
        self._write_npMatrix2Fid(self.radial_vector_borehole, fid)
        fid.write(self._vspace)

        fid.write('COLUMN_CHARACTER_BOREHOLE # [/] der Radialelemente um die Bohrung (M Werte)\n')	
        fid.write('\t'.join(self.column_character_borehole))
        fid.write(self._vspace)

        fid.write('HEAT_CAPACITY_BOREHOLE # [MJ/(K*m3)]  Dichte * spez. Waermekapazitaet der Radialelemente um die Bohrung (P*M Werte)\n')
        if self.radialComment is not None:
            fid.write('#%s\n' %('\t'.join(self.radialComment)))
        self._write_npMatrix2Fid(self.heat_capacity, fid, bottom_edges=self.bottom_edge_vertical)
        fid.write(self._vspace)

        fid.write('THERMAL_CONDUCTIVITY_BOREHOLE # [W/(m*K)]  Waermeleitfaehigkeit der Radialelemente um die Bohrung (P*M Werte)\n')
        if self.radialComment is not None:
            fid.write('#%s\n' %('\t'.join(self.radialComment)))
        self._write_npMatrix2Fid(self.thermal_conductivity, fid, bottom_edges=self.bottom_edge_vertical)
        fid.write(self._vspace)

        fid.write('TEMPERATURE_BOREHOLE  # [deg C] Temperatur der Radialelemente um die Bohrung (P*M Werte)\n')
        if self.radialComment is not None:
            fid.write('#%s\n' %('\t'.join(self.radialComment)))
        self._write_npMatrix2Fid(self.temperature_borehole, fid, bottom_edges=self.bottom_edge_vertical)
        fid.write(self._vspace)

        fid.write('WELL_VERTICALITY  # [deg] Winkel zwischen Bohrlochachse und Bohrung (P Werte)\n')
        self._write_npMatrix2Fid(self.inclination, fid, axis= 0,bottom_edges=self.bottom_edge_vertical)
        fid.write(self._vspace)

class TsgfFieldData(FieldData):
    def __init__(self, n_fluid, tvd, delta_z, medium_type_cavern, medium_id_cavern):
        super().__init__(n_fluid, tvd, delta_z, medium_type_cavern, medium_id_cavern)

    def add_reservoirCharacteristics(self, refdepth_reservoir:float, pressure_reservoir:float, minsky_A:float, minsky_B:float):
        """Adds reservoir characteristics.

        :param refdepth_reservoir: reference depth for reservoir pressure and modeling [m]
        :type refdepth_reservoir: float
        :param pressure_reservoir: reservoir pressure [MPa]
        :type pressure_reservoir: float
        :param minsky_A: Filtration coefficient A 
        :type minsky_A: float
        :param minsky_B: Filtration coefficient B
        :type minsky_B: float
        """        

        self.refdepth_reservoir = refdepth_reservoir
        self.pressure_reservoir = pressure_reservoir            
        self.minsky_A           = minsky_A
        self.minsky_B           = minsky_B

    def export_fieldData(self, save_folder:Path, project_name:str, is_binary_export: bool = False):
        """Exports TSCW konform txt-File with suffix "_tsgf.fd.txt". 

        Args:
            save_folder (Path): Folder where the project is located.
            project_name (str): Project name (this will be a subfolder in save_folder)
            is_binary_export (bool, optional): Export an additional *.pickle file which can be later loaded into python. Defaults to False.
        """
        file_path = self._create_export_folder(save_folder, project_name, '_tsgf.fd.txt', is_binary_export)
        fid = open(file_path, 'w')

        self._export_meta_data(fid)
											
        fid.write('\nMEDIUM_TYPE_RESERVOIR' 	)
        write_kwargs2Fid(self.medium_type, fid)																		
        fid.write('\nMEDIUM_ID_RESERVOIR' )	
        write_kwargs2Fid(self.medium_id, fid)	 						
        fid.write('\nDEPTH_RESERVOIR\t%.2f\t# Referenztiefe fuer Druck' %(self.refdepth_reservoir)	)		
        fid.write(self._vspace)

        self._export_borehole_data(fid)

        fid.write('TEMPERATURE_RESERVOIR\t%.2f\t#[deg C]\n' %(self.temperature_reservoir))
        fid.write('PRESSURE_RESERVOIR\t%.2f\t#[MPa]\n' %(self.pressure_reservoir))
        fid.write('FILTRATION_COEFFICIENT_A\t%.2e\t#[MPa2/(Nm3/h)]\n' %(self.minsky_A))
        fid.write('FILTRATION_COEFFICIENT_B\t%.2e\t#[MPa2/(Nm3/h)2]' %(self.minsky_B))

        fid.close()
        print('Run sucessfull')
        print(file_path)
        self.file_path = file_path

class GacaFieldData(FieldData):

    def __init__(self, n_boreholes, n_fluid, tvd, delta_z, medium_type_cavern, medium_id_cavern):

        self.n_boreholes = n_boreholes   
        super().__init__(n_fluid, tvd, delta_z, medium_type_cavern, medium_id_cavern)

    def add_cavernVector(self,radial_vector): 
        """Adds a radial vector within the cavern. The first element is the cavern radius.

        :param radial_vector: must be strictly increasing, will define self.m_cavern [int].
        :type radial_vector: list or array [m]
        """      
        assert all(i < j for i, j in zip(radial_vector, radial_vector[1:])), 'List is not strictly increasing!'

        self.radial_vector_cavern = radial_vector
        self.m_cavern = radial_vector.shape[0]

    def add_cavernCharacteristics(self,refdepth_cavern:float,density_salt:float,specific_heat_capacity_salt:float,heat_conductivity_salt:float,
                                  height_cavern:float, volume_brine_equivalent:float, radius_brine_level:float, pressure_cavern:float, temperature_brine_equivalent:float = None):
        """Add cavern characteristics:

        :param refdepth_cavern: reference depth for cavern pressure and modeling [m]
        :type refdepth_cavern: float
        :param density_salt:  [kg/m3]
        :type density_salt: float
        :param specific_heat_capacity_salt: [J/kgK]
        :type specific_heat_capacity_salt: float
        :param heat_conductivity_salt: [W/mK]
        :type heat_conductivity_salt: float
        :param height_cavern: consists of H_zy + 2*rad_cav [m]
        :type height_cavern: float
        :param volume_brine_equivalent: [m3]
        :type volume_brine_equivalent: float
        :param radius_brine_level: [m]
        :type radius_brine_level: float
        :param pressure_cavern: [MPa]
        :type pressure_cavern: float
        :param temperature_brine_equivalent: [°C], defaults to None
        :type temperature_brine_equivalent: float, optional
        """

        self.refdepth_cavern              = refdepth_cavern  
        self.density_salt                 = density_salt
        self.specific_heat_capacity_salt  = specific_heat_capacity_salt
        self.heat_conductivity_salt       = heat_conductivity_salt
        self.height_cavern                = height_cavern
        self.volume_brine_equivalent      = volume_brine_equivalent
        self.radius_brine_level           = radius_brine_level      
        self.temperature_brine_equivalent = temperature_brine_equivalent
        self.pressure_cavern              = pressure_cavern

    def export_fieldData(self, save_folder:Path, project_name:str, is_binary_export: bool = False):
        """Exports TSCW konform txt-File with suffix "_gaca.fd.txt". 

        Args:
            save_folder (Path): Folder where the project is located.
            project_name (str): Project name (this will be a subfolder in save_folder)
            is_binary_export (bool, optional): Export an additional *.pickle file which can be later loaded into python. Defaults to False.
        """   
        file_path = self._create_export_folder(save_folder, project_name, '_gaca.fd.txt', is_binary_export)
        fid = open(file_path, 'w')

        fid.write('NUMBER_BOREHOLES\t%d\n' %(self.n_boreholes))	

        self._export_meta_data(fid)

        fid.write('M_CAVERN\t%d\t# (MK)\n' %(self.m_cavern)	)													
        fid.write('MEDIUM_TYPE_CAVERN')
        write_kwargs2Fid(self.medium_type, fid)																		
        fid.write('MEDIUM_ID_CAVERN' %(self.medium_id)	)
        write_kwargs2Fid(self.medium_id, fid)			 						
        fid.write('DEPTH_CAVERN\t%.2f\t# Referenztiefe fuer Druck' %(self.refdepth_cavern)	)		
        fid.write(self._vspace)
        
        self._export_borehole_data(fid)

        fid.write('RADIAL_VECTOR_CAVERN # [m] (MK Werte)\n')
        self._write_npMatrix2Fid(self.radial_vector_cavern, fid)
        fid.write(self._vspace)

        fid.write('TEMPERATURE_CAVERN  #  [deg C] Temperatur der Radialelemente um die Kaverne (MK Werte) \n')
        self._write_npMatrix2Fid(self.temperature_cavern, fid)
        fid.write(self._vspace)

        fid.write('DENSITY_SALT\t%.2f\t#[kg/m3]\n' %(self.density_salt))																	
        fid.write('SPECIFIC_HEAT_CAPACITY_SALT\t%.2f\t#[J/(kg*K)]\n' %(self.specific_heat_capacity_salt))														
        fid.write('HEAT_CONDUCTIVITY_SALT\t%.2f\t#[W/(m*K)]\n' %(self.heat_conductivity_salt))														
        fid.write('HEIGHT_CAVERN\t%.2f\t#[m]\n' %(self.height_cavern))														
        fid.write('VOLUME_BRINE_EQUIVALENT\t%.2f\t#[m3]\n' %(self.volume_brine_equivalent))
        fid.write('RADIUS_BRINE_LEVEL\t%.2f\t#[m]\n' %(self.radius_brine_level))
        if self.temperature_brine_equivalent is not None:
            fid.write('TEMPERATURE_BRINE_EQUIVALENT\t%.2f\t#[deg C] optional\n' %(self.temperature_brine_equivalent))
        fid.write('PRESSURE_CAVERN\t%.2f\t#[MPa] at DEPTH_CAVERN %.2fm\n' %(self.pressure_cavern,self.refdepth_cavern))

        fid.close()
        print('Run sucessfull')
        print(file_path)
        
class TsclFieldData(FieldData):

    def __init__(self, n_fluid, tvd, delta_z, medium_type_cavern, medium_id_cavern):

        super().__init__(n_fluid, tvd, delta_z, medium_type_cavern, medium_id_cavern)
        
    
    def add_cavernCharacteristics(self,
                                  cavern_net_volume_0:float,
                                  medium_type_cavern:str,
                                  medium_id_cavern: int,
                                  depth_cavern:float,
                                  dr_max_cavern:float,  
                                  dr_1_cavern:float,
                                  dr_1_saltrock:float,
                                  f_dr:float,
                                  r_max_cavern:float ,
                                  temperature_cavern:float ,
                                  temperature_salt:float ,
                                  density_salt:float ,
                                  specific_heat_capacity_salt:float,
                                  heat_conductivity_salt:float,
                                  height_cavern:float,
                                  conductance_weight_factor:float):
        """Add cavern charistics

        Args:
            cavern_net_volume_0 (float): _description_
            medium_type_cavern (str): _description_
            medium_id_cavern (int): _description_
            depth_cavern (float): _description_
            dr_max_cavern (float): _description_
            dr_1_cavern (float): _description_
            dr_1_saltrock (float): _description_
            f_dr (float): _description_
            r_max_cavern (float): _description_
            temperature_cavern (float): _description_
            temperature_salt (float): _description_
            density_salt (float): _description_
            specific_heat_capacity_salt (float): _description_
            heat_conductivity_salt (float): _description_
            height_cavern (float): _description_
            conductance_weight_factor (float): _description_
        """        
        self.cavern_net_volume_0 = cavern_net_volume_0
        self.medium_type_cavern = medium_type_cavern
        self.medium_id_cavern = medium_id_cavern
        self.depth_cavern = depth_cavern
        self.dr_max_cavern = dr_max_cavern
        self.dr_1_cavern = dr_1_cavern
        self.dr_1_saltrock = dr_1_saltrock
        self.f_dr = f_dr
        self.r_max_cavern = r_max_cavern
        self.temperature_cavern = temperature_cavern
        self.temperature_salt = temperature_salt
        self.density_salt = density_salt
        self.specific_heat_capacity_salt = specific_heat_capacity_salt
        self.heat_conductivity_salt = heat_conductivity_salt
        self.height_cavern = height_cavern
        self.conductance_weight_factor = conductance_weight_factor


    def export_fieldData(self, save_folder:Path, project_name:str, is_binary_export: bool = False):
        """Exports TSCW konform txt-File with suffix "_tscl.fd.txt". 

        Args:
            save_folder (Path): Folder where the project is located.
            project_name (str): Project name (this will be a subfolder in save_folder)
            is_binary_export (bool, optional): Export an additional *.pickle file which can be later loaded into python. Defaults to False.
        """   
        file_path = self._create_export_folder(save_folder, project_name, '_tscl.fd.txt', is_binary_export)
        fid = open(file_path, 'w')
        
        self._export_meta_data(fid)

        fid.write('CAVERN_NET_VOLUME_0\t%d\t# [m3]\n' %(self.cavern_net_volume_0)	)
        fid.write('MEDIUM_TYPE_CAVERN\t%s\t# [-]\n' %(self.medium_type_cavern)	)
        fid.write('MEDIUM_ID_CAVERN\t%d\t# [-]\n' %(self.medium_id)	)
        fid.write('DEPTH_CAVERN\t%.2f\t# [m]\n' %(self.depth_cavern)	)
        fid.write('DR_MAX_CAVERN\t%.2f\t# [m]\n' %(self.dr_max_cavern)	)
        fid.write('DR_1_CAVERN\t%.3f\t# [m]\n' %(self.dr_1_cavern)	)
        fid.write('DR_1_SALTROCK\t%.3f\t# [m]\n' %(self.dr_1_saltrock)	)
        fid.write('F_DR\t%.3f\t# [-]\n' %(self.f_dr)	)
        fid.write(self._vspace)
        
        self._export_borehole_data(fid)
        
        fid.write(self._vspace)
        
        fid.write('R_MAX_CAVERN\t%.3f\t# [m]\n' %(self.r_max_cavern)	)
        fid.write('TEMPERATURE_CAVERN\t%.3f\t# [deg]\n' %(self.temperature_cavern)	)
        fid.write('TEMPERATURE_SALT\t%.3f\t# [deg]\n' %(self.temperature_salt)	)
        fid.write('DENSITY_SALT\t%.3f\t# [kg/m3]\n' %(self.density_salt)	)
        fid.write('SPECIFIC_HEAT_CAPACITY_SALT\t%.3f\t# [J/(kg*K)]\n' %(self.specific_heat_capacity_salt)	)
        fid.write('HEAT_CONDUCTIVITY_SALT\t%.3f\t# [W/(m*K)]\n' %(self.heat_conductivity_salt)	)
        fid.write('HEIGHT_CAVERN\t%.3f\t# [m]\n' %(self.height_cavern)	)
        fid.write('CONDUCTANCE_WEIGHT_FACTOR\t%.3f\t# [-]\n' %(self.conductance_weight_factor)	)

        fid.close()
        print('Run sucessfull')
        print(file_path)

####################################################################################




_FILE_EXT = Literal['gaca','tsgf','tscl']

class ProcessData():
    
    MAP_MODULE_TO_FILE_EXT = {
            'gaca' : '_gaca.pd.txt',
            'tsgf' : '_tsgf.pd.txt',
            'tscl' : '_tscl.pd.txt'
    }
    
    
    
    def __init__(self,description:str, coupled_annuli:list, medium_type:list, medium_id:list, tscw_module: _FILE_EXT = 'gaca'):
        """Created process data for TSWC that can be exported to a txt-file.

        :param description: description to be displayed in txt-file.
        :type description: str
        :param coupled_annuli: _description_
        :type coupled_annuli: list or np.array [1 x N_FLUID]
        :param medium_type: _description_
        :type medium_type: string array [1 x N_FLUID]
        :param medium_id: _description_
        :type medium_id: list [1 x N_FLUID]
        :param tscw_module: defined in self.MAP_MODULE_TO_FILE_EXT
        :type tscw_module: list [1 x N_FLUID]
        """     
        if isinstance(coupled_annuli, list) or isinstance(medium_id, list):
            assert len(coupled_annuli) == len(medium_id), 'MEDIUM ID und COUPLED ANNULI do must have same length!'
        assert tscw_module in self.MAP_MODULE_TO_FILE_EXT.keys(), f'Incorrect module name: {tscw_module}.'

        self.description    = description
        self.medium_type    = medium_type
        self.medium_id      = medium_id
        self.coupled_annuli = coupled_annuli
        self.tscw_module    = tscw_module

        self.n_stages   = 0
        self.stages_param = dict()

        if isinstance(medium_type, str):
            self.n_fluid = 1
        else:
            self.n_fluid = len(medium_type)

    def add_stage(self,stage_data: dict):
        """Erlaubt flexibles hinzufügen von stages. Stages werden chronologisch hinzugefügt.
        WICHTIG: Schlüsselnamen aus dict müssen mit Variablenname von TSWC übereinstimmen, erlaubt sind folgende Namen:
            - 'TERMINATION_ID',
            - 'TERMINATION_QUANTITY',
            - 'DT_MAX',
            - 'FLOW_RATE',
            - 'P_BOUNDARY_CONDITION',
            - 'BOUNDARY_PRESSURE',
            - 'T_BOUNDARY_CONDITION',
            - 'BOUNDARY_TEMPERATURE',
            - 'K_S'

        'TERMINATION_ID' und 'TERMINATION_QUANTITY' müssen eingegeben werden!

        :param stage_data: Enthält alle erforderlichen Parameter in der Form {Schlüssel: Wert}
        :type stage_data: dict
        """        '''

        '''

        # allowed key names
        variable_names_pd = [
        'TERMINATION_ID',
        'TERMINATION_QUANTITY',
        'DT_MAX',
        'FLOW_RATE',
        'P_BOUNDARY_CONDITION',
        'BOUNDARY_PRESSURE',
        'T_BOUNDARY_CONDITION',
        'BOUNDARY_TEMPERATURE',
        'K_S',
        'CAVERN_NET_VOLUME',
        'STAGE_DURATION'
        ]

        # boundary_conditions_module = {
        #     'gaca' : ['WELLHEAD', 'BOTTOM', 'CAVERN', 'COUPLED', 'NONE'],
        #     'tsgf' : ['WELLHEAD', 'BOTTOM', 'RESERVOIR', 'COUPLED', 'NONE'],
        # }

        # termination_id_module = {
        #     'gaca' : [1,2,3,4,6,7,8,9,10],
        #     'tsgf' : [1],
        # }

        # check spelling of keys:
        for key in stage_data.keys():
            assert key in variable_names_pd, 'Spelling error %s' %(key)
        # assert 'TERMINATION_ID' in stage_data.keys()
        # assert 'TERMINATION_QUANTITY' in stage_data.keys()

        # add stage to stages_param
        self.stages_param[self.n_stages] = copy.deepcopy(stage_data)
        self.n_stages += 1


    def export_processData(self,save_folder:Path,project_name:str, subfolder = ''):
        """Exports class to a txt-File with the suffix depending on tscw_module.
        Will will be exported to a folder named (path, project_name, suffix). If it does not exist, it will be created.

        :param save_folder: _description_
        :type save_folder: str
        :param project_name: _description_
        :type project_name: str
        :param subfolder: defaults to ''
        :type subfolder: str, optional
        """     
        save_path = save_folder.joinpath(project_name, subfolder)
        if not (save_path.exists()):
            save_path.mkdir(parents=True, exist_ok=False)
            print('Created new folder %s' %(save_path))

        file_name =  save_path.joinpath(project_name + subfolder + self.MAP_MODULE_TO_FILE_EXT[self.tscw_module])
        assert len(str(file_name)) <= 260, f'Process data file path is {len(str(file_name))} but max length is 260.'
        fid = open(file_name, 'w')

        fid.write('DESCRIPTION\t%s\n' %(self.description))																	
        fid.write('N_FLUID\t%d\n' %(self.n_fluid)	)														
        fid.write('NUMBER_OF_STAGES [/]\t%d\n\n' %(self.n_stages)	)														
        fid.write('MEDIUM_TYPE [/]')
        write_kwargs2Fid(self.medium_type, fid)
        fid.write('\nMEDIUM_ID [/]')
        write_kwargs2Fid(self.medium_id, fid)    
        fid.write('\nCOUPLED_ANNULI [integer required!]')
        write_kwargs2Fid(self.coupled_annuli,fid)    
        fid.write('\n')

        for i_stage in range(self.n_stages):
            fid.write('\n\n# ++++++++++++++++++++++++++++++++\n')
            fid.write('STAGE\t%d\n' %(i_stage + 1)	)
            fid.write('# ++++++++++++++++++++++++++++++++\n')
            for key, value in self.stages_param[i_stage].items():
                fid.write('\n%s' %(key))
                write_kwargs2Fid(value,fid)

        fid.close()
        print('Run sucessfull')
        print(file_name)
        self.file_path = file_name

####################################################################################

