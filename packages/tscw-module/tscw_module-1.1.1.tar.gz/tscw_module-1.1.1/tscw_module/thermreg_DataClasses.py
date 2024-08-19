import numpy as np
import re
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import mplcursors
from tkinter import *
from tkinter.ttk import *
from .helper_func import *
from .tscw_DataClassesOutput import TSCW_Output

class ThermregData(TSCW_Output):
    '''
    Read in and process Thermreg output data.
    '''
    def __init__(self, path:str, n_depths:int = None):
        '''
        path: absolute path of Regtherm file (*.txt).
        n_dephts: how many vertical depth points (including z0 = 0m)
        '''
        self.path = path
        super().__init__()

        
        if type(n_depths) is int:
            self.n_depths = n_depths
        elif type(n_depths) is list or isinstance(n_depths, np.ndarray):
            self.n_depths = len(n_depths)
            self.depth_array = n_depths
        else:
            self.depth_array = None

        if n_depths is not None:
            temp_array  = np.empty((0,self.n_depths), float)
            press_array = np.empty((0,self.n_depths), float)
        else:
            temp_array  = None
            press_array = None

        t_total     = np.array([])
        t_etappe    = np.array([])
        t_neueEtappe = np.array([])
        temp_field   = None

        temp_split = 'T,GRD C:'
        pres_split = 'P,MPA  :'
        temp_field_split = 'TEMPERATURFELD'

        is_readNextRow = 0
        with open(path) as fid:
            for row in fid:

                if temp_split in row:
                    row_val = re.split(temp_split, row)[-1].split()
                    row_val = np.array([row_val], dtype=float)

                    if temp_array is None:
                        self.n_depths = row_val.shape[1]
                        temp_array = np.empty((0,self.n_depths), float)
                        press_array = np.empty((0,self.n_depths), float)

                    temp_array = np.append(temp_array, row_val, axis=0)
                    
                    row_val = prev_row.split()[0]
                    t_total = np.append(t_total,float(row_val))
                    
                    row_val = prev_row.split()[1]
                    t_etappe = np.append(t_etappe,float(row_val))

                if pres_split in row:
                    row_val = re.split(pres_split, row)[-1].split()
                    row_val = np.array([row_val], dtype=float)
                    press_array = np.append(press_array, row_val, axis=0)

                if temp_field_split in row:
                    is_readNextRow = self.n_depths - 1
                    continue

                if is_readNextRow > 0 and len(row) > 3: #avoid next line \n 
                    row_val     = np.array([row.split()], dtype=float)

                    if temp_field is None:
                        temp_field = np.empty((0,row_val.shape[1]), float)

                    temp_field  = np.append(temp_field, row_val, axis=0)
                    is_readNextRow -= 1

                prev_row = row

                if 'ETAPPE' in row:
                    try:
                        t_neueEtappe = np.append(t_neueEtappe, t_total[-1])
                    except:
                        pass

        self.t_neueEtappe = t_neueEtappe

        t_neueEtappe = np.append(t_neueEtappe, t_total[-1])

        i_etappen = np.zeros_like(t_total)
        idx1 = find_nearest(t_total, t_neueEtappe[0]) + 1
        i_etappen[:idx1] = 1
        etappen_counter = 2
        for i_etappe in range(len(t_neueEtappe[:-2])):
            idx1 = find_nearest(t_total, t_neueEtappe[i_etappe]) + 1
            idx2 = find_nearest(t_total, t_neueEtappe[i_etappe + 1]) + 1
            i_etappen[idx1:idx2] = etappen_counter
            etappen_counter += 1

        i_etappen[idx2:] = etappen_counter

        self.t_total = t_total
        self.temp_array = temp_array
        self.press_array = press_array
        self.i_etappen = i_etappen
        self.t_etappe = t_etappe
        self.temp_field = temp_field

        headers = ['STAGE'] + ['t_TOTAL [h]'] + ['t_Etappe [h]'] + ['T_z%d [deg]' % (i) for i in range(self.n_depths)] + ['p_z%d [MPa]' % (i) for i in range(self.n_depths)] 
        df = pd.DataFrame(np.column_stack((self.i_etappen,self.t_total,self.t_etappe,self.temp_array,self.press_array)))
        df.columns = headers

        self.stage_idx = np.unique(df.STAGE, return_index=True)

        self.df = df

        # if n_depths is list, make same structure as for TSCW
        if type(n_depths) is list or isinstance(n_depths, np.ndarray):
            headers = ['%.2f' %(depth) for depth in n_depths]
            vertT_df = pd.DataFrame(self.temp_array) 
            vertT_df.columns = headers
            vertP_df = pd.DataFrame(self.press_array) 
            vertP_df.columns = headers

            self.vertT_df = vertT_df
            self.vertP_df = vertP_df

        print('Succesfully imported Thermreg data %s' %(path))

    def export_csv(self):
        '''
        Export Thermreg p-T data into a xlsx file.
        '''
        dir_path = Path(self.path).parent
        file_name = Path(self.path).stem
        new_path = dir_path.joinpath(file_name + '_export.xlsx')
        self.df.to_excel(new_path, index=False, header=True)
        print('Succesfully exported Regtherm data to %s' %(new_path))

    def plot_tp_vs_depth(self,time_t = None,time_p = None, is_export = False):
        """Plots borehole temperature - pressure development over depth.

        :param depth_t: which time intervals for Temperature, by default all
        :type depth_t: _type_, optional
        :param depth_p: which time intervals for Pressure, by default all
        :type depth_p: _type_, optional
        :param is_export: defaults to False
        :type is_export: bool, optional
        """        
        
        if time_t is None:
            time_t = self.t_total
        
        if time_p is None:
            time_p = self.depth_array

        all_plot_points = [time_t, time_p]
        all_data        = [self.vertT_df,self.vertP_df]

        data = self.create_data_array2plot(all_plot_points, all_data, 'depth')

        meta = {
            'title': 'p-T Distribution',
            'subtitle' : Path(self.path).name,
            'is_export'   : is_export,
            'suffix': 'tp_vs_depth',
            'xlabel'   : 'depth'
        }

        self.create_pT_plot(data, meta)

    def plot_tp_vs_time(self,depth_t = None,depth_p = None, is_export = False):
        """_summary_

        :param depth_t:  which depth intervals for Temperature, by default all
        :type depth_t: _type_, optional
        :param depth_p: _description_, defaults to None
        :type depth_p: which depth intervals for Pressure, by default all
        :param is_export: defaults to False
        :type is_export: bool, optional
        """        

        if depth_t is None:
            depth_t = self.depth_array
        
        if depth_p is None:
            depth_p = self.depth_array

        all_plot_points = [depth_t, depth_p]
        all_data        = [self.vertT_df,self.vertP_df]

        data = self.create_data_array2plot(all_plot_points, all_data)

        meta = {
            'title'       : 'p-T Distribution',
            'subtitle'    : Path(self.path).name,
            'is_export'   : is_export,
            'suffix'      : 'tp_vs_time',
            'xlabel'      : 'time'
        }

        fig = self.create_pT_plot(data, meta)

        return fig
    

    def calculate_axial_forces(self, meta_data:dict, T0:float = None, vectors=tuple, is_export:bool = False):
        '''
        Calculates resulting axial forces
        INPUT:
        meta_data: dictionary containing meta data.
        T0: Initial temperature for reference in delta_T
        vectors: tuple - (temperature, pressure) [K, MPa]
        is_export: true or false - as a xlsx file
        OUTPUT
        Dataframe
        '''

        t_vector = vectors[0]
        p_vector = vectors[1]

        if is_export:
            path = Path(self.path)
            file_path = path.parent.joinpath(path.stem + '_forces.xlsx')
        else:
            file_path = None

        if T0 is None:
            T0 = t_vector[0]

        df = calculate_forces(meta_data, t_vector, p_vector, self.t_total, self.t_etappe, self.i_etappen , T0 , file_path)

        self.forces_df = df

        return df
    

    def extract_max_force(self, i_etappe, mode, min_time:float = 0):
        '''
        Extracts min or max Fz_ges for a selected Stage.
        INPUT:
        i_etappe: int - Stage number
        mode: either 'min' or 'max'
        min_time: float - minimum time that has passed after the value is selected, put in +inf to select end of stage, 0 by default
        OUTPUT:
        filtered_df: pd.Dataframe containing relevant parameters
        df_index: int - index of total Dataframe df of respective class.
        '''

        assert mode in ['max', 'min'], 'Rechtschreibfehler!'

        filtered_df, df_index = filter_forces_fd(self.i_etappen, i_etappe, self.forces_df, mode, min_time)

        return filtered_df, df_index
    
    def plot_axial_forces(self, is_export:bool = False):
        '''
        Plots axial forces of forces_df.
        INPUT:
        is_export: bool - Export as png [optional]
        OUTPUT
        figure
        '''
        fig = plot_forces(self.forces_df, self.path, is_export)
        return fig
    

    def interpolate_pt(self, time_array):
        '''
        Interpolates pressure and temperature for a new time_array
        INPUT:
        time_array: list - new time array
        OUTPUT
        thermreg_temp_inter - interpolated temperature array
        thermreg_pres_inter - interpolated pressure array
        '''

        thermreg_temp_inter = np.zeros((time_array.shape[0], self.n_depths))
        thermreg_pres_inter = np.zeros_like(thermreg_temp_inter)

        for i in range(self.n_depths):

            f_temp = interpolate.interp1d(self.t_total,
                                        self.temp_array[:,i], fill_value='extrapolate' )
            f_press = interpolate.interp1d(self.t_total,
                                        self.press_array[:,i], fill_value='extrapolate' )
            
            thermreg_temp_inter[:,i] =  f_temp(time_array)
            thermreg_pres_inter[:,i] =  f_press(time_array)

        self.temp_array_inter  =  thermreg_temp_inter
        self.press_array_inter =  thermreg_pres_inter

        return thermreg_temp_inter, thermreg_pres_inter
    

    def plot_all_tempfields(self, radial_vector = None, x2_limit:float = None, is_export:bool = False):
        """_summary_

        :param depths: self.depths
        :type depths: _type_, optional
        :param radial_vector: _description_, defaults to None
        :type radial_vector: _type_, optional
        :param x2_limit: _description_, defaults to None
        :type x2_limit: float, optional
        :param is_export: _description_, defaults to False
        :type is_export: bool, optional
        """
        n_field_dephts = self.n_depths - 1
        n_field = int(self.temp_field.shape[0] / n_field_dephts)

        if self.depth_array is not None:
            depths = 0.5*(self.depth_array[:-1] - self.depth_array[1:]) 
            depths[0] = self.depth_array[0]
            depths[-1] = self.depth_array[-1]
        else:
            depths = np.linspace(0,1,n_field_dephts)

        if radial_vector is not None:
            radial_vector[0] = 0
            assert len(radial_vector) == self.temp_field.shape[1] 
            self.radial_vector = radial_vector
        else:
            radial_vector = np.linspace(0,1,self.temp_field.shape[1])

        if x2_limit is None:
            x2_limit = np.max(radial_vector)

        min_val = np.min(self.temp_field)
        max_val = np.max(self.temp_field)
        for iField in range(n_field):
            fig, ax = plt.subplots()
            fig.canvas.manager.set_window_title('Figure %d' %(iField)) 
            temp_data = self.temp_field[iField*n_field_dephts:(iField+1)*n_field_dephts,:] 

            X,Y = np.meshgrid(radial_vector, depths)
            # Z   = temp_data[:-1, :-1]
            Z = temp_data
            cm = ax.contourf(X,Y,Z, levels = 100, cmap = 'jet', vmin = min_val, vmax = max_val)
            ax.set(ylabel = 'z [m]' , xlim = [0, x2_limit])
            ax.invert_yaxis()
            cbar = plt.colorbar(cm, ax = ax) #, format = '%.1f K', label = 'Temperature')
            cbar.ax.set_title('T [°C]', loc='center')

            if is_export:
                save_path = Path(self.path).parent.joinpath(Path(self.path).stem + 'Tempfield%d.png' %(iField))
                fig.savefig(save_path)
                print('Exported %s' %(save_path))