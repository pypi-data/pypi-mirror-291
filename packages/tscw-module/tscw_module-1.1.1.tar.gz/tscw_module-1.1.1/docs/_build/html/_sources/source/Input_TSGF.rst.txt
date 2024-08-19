TSCW TSGF - INPUT - Erstellung
=====


------------

Um eine Felddaten-Datei für das TSGF Modul zu erstellen, muss die Klasse ``TsgfFieldData`` erstellt und mit Daten belegt werden.


0. Importiere benötigte Module:
~~~~~~~~~~

.. code-block:: python
   :linenos:

   from tscw_module import TsgfFieldData
   import matplotlib.pyplot as plt
   import numpy as np

1. Initialisiere **TsgfFieldData**:
~~~~~~~~~~

Analog zu Schritt 1 in ``GacaFieldData``

.. code-block:: python
   :linenos:
   :lineno-start: 4

   n_fluid            = 2
   tvd_et             = 935.3                # Endteufe Bohrung
   delta_z            = tvd_et / 25          # 25 Schichten a 37.412 m
   medium_type_field  = 'GAS' 
   medium_id_cavern   = 'H2'                 # Definiertes Gasgemisch in der Stoffwerte-Bibliothek von TSCW

   # Initialisiere TsgfFieldData Class
   FieldData = TsgfFieldData(n_fluid, tvd_et, delta_z, medium_type_field, medium_id_field)


Schritt 2 - Defintion der Geometrie und Stoffwertematrizen
~~~~~~~~~~

Analog zu Schritt 2 + 3 (objektorientiert) in ``GacaFieldData``

Es wird mit der Definition der radialen Sützstellen für die Formation begonnen.

.. code-block:: python
   :lineno-start: 12

   ## Geologie
   formation_radial_vector = np.array([0.4, 0.5, 0.75, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 50.0 ])
   FieldData.initialise_formation(formation_radial_vector)

Anschließend kann eine Stoffwerteverzeichnis ``Md`` angelegt werden, welches die thermische Leitfähigkeit [W/(m*K)], Dichte [kg/m3] und spez. Wärmekapazität [J/kg*K] enthalten.
Damit kann die geologische Formation definiert werden.

.. code-block:: python
   :lineno-start: 15

   Md = {
               'cement': {'rho': 1900, 'cp': 850,'lambda': 0.80},
               'steel':  {'rho': 7850, 'cp': 460,'lambda': 48},
               'rrsf':  {'rho': 1000, 'cp': 4180,'lambda': 0.6},
               'quartar':  {'rho': 1800, 'cp': 950,'lambda': 2.3},
               'unt_buntsandstein':  {'rho': 2500, 'cp': 760,'lambda': 2.6},
               'muschelkalk':  {'rho': 2620, 'cp': 675,'lambda': 2.5},
               'hauptanhydrit':  {'rho': 2900, 'cp': 864,'lambda': 4.0},
               'stasfurt':  {'rho': 2160, 'cp': 860,'lambda': 5.91},
               'anhydrit':  {'rho': 3000, 'cp': 860,'lambda': 4.2},
               'leine': {'rho': 2160, 'cp': 860,'lambda': 5.23},
               'keuper': {'rho': 2600, 'cp': 731, 'lambda': 2.5},
         }


   FieldData.add_formation(0, 87, Md['keuper'], 'Keuper')
   FieldData.add_formation(87 + delta_z, 328, Md['muschelkalk'], 'Muschelkalk')
   FieldData.add_formation(328 + delta_z, 622 , Md['unt_buntsandstein'], 'Buntsandstein')
   FieldData.add_formation(622 + delta_z, 813 , Md['leine'], 'Leine Steinsalz')
   FieldData.add_formation(813 + delta_z, tvd_et , Md['stasfurt'], 'Stasfurt Steinsalz')



Nachdem die Geologie definiert worden ist, kann mit dem Hinzufügen von Installationselementen begonnen werden.

.. py:function:: add_element(top, bottom, heat_capacity, thermal_conductivity, name)

         :param top: (z0, x0) - coordinates of element at the top left corner.
         :type starting_coor: tuple
         :param  bottom: (z1, x1) - coordinates of element at the bottom right corner.
         :type end_coor: tuple
         :param heat_capacity_val: [MJ/(m3K)]
         :type heat_capacity_val: float
         :param thermal_conductivity_val: [W/(m K)]
         :type thermal_conductivity_val: float
         :param name: Name, defaults to None
         :type name: str, optional

.. code-block:: python
   :lineno-start: 35

   ### Innen- und Außendurchmesser der einzelenen Rohrtouren
   rt_data = {
      '21': {'OD': 21*0.0254, 'ID': 21*0.0254 - 2*10e-3},
      '14_34': {'OD': 14.75*0.0254, 'ID': 14.75*0.0254 - 2*11e-3},
      '11_34': {'OD': 11.75*0.0254, 'ID': 11.75*0.0254 - 2*11e-3},
      '8_58': {'OD': (8 + 5/8)*0.0254, 'ID': (8 + 5/8)*0.0254 - 2*10e-3},
      '6_58': {'OD': (6 + 5/8)*0.0254, 'ID': (6 + 5/8)*0.0254 - 2*10.6e-3}
   }

   for key in rt_data.keys(): # convert diameters to radii
      rt_data[key]['IR'] = 0.5* rt_data[key]['ID']
      rt_data[key]['OR'] = 0.5* rt_data[key]['OD']

   # Stahl
   FieldData.add_element((0, rt_data['6_58']['IR']), (tvd_et, rt_data['6_58']['OR']), Md['steel'], '6 5/8"')        
   FieldData.add_element((0, rt_data['8_58']['IR']), (tvd_et, rt_data['8_58']['OR']), Md['steel'], '8 5/8"')        
   FieldData.add_element((0, rt_data['11_34']['IR']), (483, rt_data['11_34']['OR']), Md['steel'], '11 3/4"')
   FieldData.add_element((0, rt_data['14_34']['IR']), (114, rt_data['14_34']['OR']), Md['steel'], '14 3/4"')

   # Zement
   FieldData.add_element((0, rt_data['14_34']['OR']), (114, rt_data['21']['IR']), Md['cement'])            
   FieldData.add_element((0, rt_data['11_34']['OR']), (483, rt_data['14_34']['IR']), Md['cement'])
   FieldData.add_element((0, rt_data['8_58']['OR']), (tvd_et, rt_data['11_34']['IR']), Md['cement'])                                       

Als letztes müssen in den Stoffwertematrizen die Spalten, welche die Strömunsgräume repräsentieren, mit Nullwerten belegt werden.
Nur so kann das Input File später von TSCW korrekt gelesen werden. In diesem Fall liegt der Strömungsraum an erster und dritter Stelle (in Python basiert auf einen 0-index)

.. code-block:: python
   :lineno-start: 20

   FieldData.define_fluid_space([0, 2])


Die Stoffwertematrizen sind nun Attribute der Klasse FieldData und können mit dem Befehl ``FieldData.heat_capacity`` oder ``FieldData.thermal_conductivity`` inspiziert werden.

4. Temperatur und Neigung des Bohrlochs
~~~~~~~~~~

.. code-block:: python
   :lineno-start: 32

   T_0                  = 8  # Tempertur an der Oberfläche
   T_end                = 32 # Tempertur am Rohrschuh
   vertical_temperature = np.linspace(T_0, T_end, num=FieldData.p_borehole) # interpoliere zwischen T_0 und T_end -> 1D Array [1 x P]
   temparature_bh       = np.transpose(np.tile(vertical_temperature,(FieldData.m_borehole, 1))) # Erweitere vertical_temperature - > 2D Array [M x P]
   FieldData.add_temperature(temparature_bh,'borehole')
   FieldData.add_boreholeInclination('vertical')

5. Reservoireigenschaften
~~~~~~~~~~

.. code-block:: python
   :linenos:
   :lineno-start: 36

   FieldData.add_reservoirCharacteristics(
      refdepth_reservoir = 0.5* (935.3 + 970), # m
      pressure_reservoir = 2,                  # MPa
      minsky_A=5.46e-5,                        # MPa*MPa/(m*m*m/h)
      minsky_B=8.10e-9                         # MPa*MPa/((m*m*m/h)*(m*m*m/h))
   )


6. Export 
~~~~~~~~~~

.. code-block:: python
   :linenos:
   :lineno-start: 66

   FieldData.export_fieldData(save_folder,project_name, True)

Die exportierte Felddaten-Datei ist:

.. code-block:: shell

   N_FLUID	2
   M_BOREHOLE	19	# (M)
   P_BOREHOLE	25	# (P)
   DL	37.4120	# [m]

   MEDIUM_TYPE_RESERVOIR	GAS

   MEDIUM_ID_RESERVOIR	Methan

   DEPTH_RESERVOIR	952.65	# Referenztiefe fuer Druck

   RADIAL_VECTOR_BOREHOLE # [m]
   0.0735	0.0841	0.0995	0.1095	0.1382	0.1492	0.1763	0.1873	0.2567	0.4000	0.5000	0.7500	1.0000	2.0000	4.0000	8.0000	16.0000	32.0000	50.0000

   COLUMN_CHARACTER_BOREHOLE # [/] der Radialelemente um die Bohrung (M Werte)
   FLUID	SOLID	FLUID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID	SOLID

   HEAT_CAPACITY_BOREHOLE # [MJ/(K*m3)]  Dichte * spez. Waermekapazitaet der Radialelemente um die Bohrung (P*M Werte)
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	3.611	1.615	1.901	1.901	1.901	1.901	1.901	1.901	1.901	1.901	1.901	1.901	# UK 37.41m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	3.611	1.615	1.901	1.901	1.901	1.901	1.901	1.901	1.901	1.901	1.901	1.901	# UK 74.82m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 112.24m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 149.65m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 187.06m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 224.47m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 261.88m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 299.30m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	1.768	# UK 336.71m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 374.12m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 411.53m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 448.94m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 486.36m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	3.611	0.000	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 523.77m - Buntsandstein_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 561.18m - Buntsandstein_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 598.59m - Buntsandstein_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	1.900	# UK 636.00m - Buntsandstein_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 673.42m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 710.83m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 748.24m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 785.65m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 823.06m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 860.48m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 897.89m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   0.000	3.611	0.000	3.611	1.615	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	1.858	# UK 935.30m - Stasfurt Steinsalz_6 5/8"_8 5/8"


   THERMAL_CONDUCTIVITY_BOREHOLE # [W/(m*K)]  Waermeleitfaehigkeit der Radialelemente um die Bohrung (P*M Werte)
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 37.41m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 74.82m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 112.24m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 149.65m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 187.06m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 224.47m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 261.88m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 299.30m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	2.500	# UK 336.71m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 374.12m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 411.53m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 448.94m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 486.36m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	48.000	0.000	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 523.77m - Buntsandstein_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 561.18m - Buntsandstein_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 598.59m - Buntsandstein_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	2.600	# UK 636.00m - Buntsandstein_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	# UK 673.42m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	# UK 710.83m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	# UK 748.24m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	# UK 785.65m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	5.230	# UK 823.06m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	# UK 860.48m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	# UK 897.89m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   0.000	48.000	0.000	48.000	0.800	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	5.910	# UK 935.30m - Stasfurt Steinsalz_6 5/8"_8 5/8"


   TEMPERATURE_BOREHOLE  # [deg C] Temperatur der Radialelemente um die Bohrung (P*M Werte)
   8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	8.000	# UK 37.41m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	9.000	# UK 74.82m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	10.000	# UK 112.24m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	11.000	# UK 149.65m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	12.000	# UK 187.06m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	13.000	# UK 224.47m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	14.000	# UK 261.88m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	15.000	# UK 299.30m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	16.000	# UK 336.71m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	17.000	# UK 374.12m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	18.000	# UK 411.53m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	19.000	# UK 448.94m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	20.000	# UK 486.36m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	21.000	# UK 523.77m - Buntsandstein_6 5/8"_8 5/8"
   22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	22.000	# UK 561.18m - Buntsandstein_6 5/8"_8 5/8"
   23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	23.000	# UK 598.59m - Buntsandstein_6 5/8"_8 5/8"
   24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	24.000	# UK 636.00m - Buntsandstein_6 5/8"_8 5/8"
   25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	25.000	# UK 673.42m - Leine Steinsalz_6 5/8"_8 5/8"
   26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	26.000	# UK 710.83m - Leine Steinsalz_6 5/8"_8 5/8"
   27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	27.000	# UK 748.24m - Leine Steinsalz_6 5/8"_8 5/8"
   28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	28.000	# UK 785.65m - Leine Steinsalz_6 5/8"_8 5/8"
   29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	29.000	# UK 823.06m - Leine Steinsalz_6 5/8"_8 5/8"
   30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	30.000	# UK 860.48m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	31.000	# UK 897.89m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	32.000	# UK 935.30m - Stasfurt Steinsalz_6 5/8"_8 5/8"


   WELL_VERTICALITY  # [deg] Winkel zwischen Bohrlochachse und Bohrung (P Werte)
   0.000	# UK 37.41m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	# UK 74.82m - Keuper_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	# UK 112.24m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"_14 3/4"
   0.000	# UK 149.65m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 187.06m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 224.47m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 261.88m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 299.30m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 336.71m - Muschelkalk_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 374.12m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 411.53m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 448.94m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 486.36m - Buntsandstein_6 5/8"_8 5/8"_11 3/4"
   0.000	# UK 523.77m - Buntsandstein_6 5/8"_8 5/8"
   0.000	# UK 561.18m - Buntsandstein_6 5/8"_8 5/8"
   0.000	# UK 598.59m - Buntsandstein_6 5/8"_8 5/8"
   0.000	# UK 636.00m - Buntsandstein_6 5/8"_8 5/8"
   0.000	# UK 673.42m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 710.83m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 748.24m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 785.65m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 823.06m - Leine Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 860.48m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 897.89m - Stasfurt Steinsalz_6 5/8"_8 5/8"
   0.000	# UK 935.30m - Stasfurt Steinsalz_6 5/8"_8 5/8"


   TEMPERATURE_RESERVOIR	32.45	#[deg C]
   PRESSURE_RESERVOIR	2.00	#[MPa]
   FILTRATION_COEFFICIENT_A	5.46e-05	#[MPa2/(Nm3/h)]
   FILTRATION_COEFFICIENT_B	8.10e-09	#[MPa2/(Nm3/h)2]

6. Geometrie QC 
~~~~~~~~~~

.. note::

   Es empfiehlt sich, vor dem Starten der Simulation die erstellte txt-Datei zu kontrollieren.
   Somit können viele Fehlerquellen vor Starten der Simulation eliminiert werden!
   Außerdem kann die Geometrie mit folgendem Befehl geplottet werden:

.. code-block:: python
   :linenos:

      FieldData.plot_geometry([0, 1.5]) # radial range
      plt.show()

.. image:: ../_static/Kh_48Geometry_HeatCapactiyRho.png
  :width: 700
  :alt: Kh_48Geometry_HeatCapactiyRho.png


.. image:: ../_static/Kh_48Geometry_ThermalConductivity.png
  :width: 700
  :alt: Kh_48Geometry_ThermalConductivity.png



Prozessdaten
----------------


Für die Prozessdaten wird die Klasse  ``ProcessData`` erstellt und mit Daten belegt.

1. Initialisierung 
~~~~~~~~~~

.. code-block:: python
   :linenos:

   coupled_annuli  = [1, 2]
   medium_type     = ['GAS', 'BRINE']
   medium_id       = [medium_id_field, 316]   # 316 kg/m3 Mineralisation bei rho = 1200 kg/m3 und T = 20°C
   description     = 'Beispiel'
   Process_Data    = ProcessData(description, coupled_annuli, medium_type, medium_id, 'tsgf') # die Flag tsgf ist wichtig!

2. Hinzufügen von Etappen
~~~~~~~~~~

Etappen können chronologisch hinzugefügt werden.
Dies hat den Vorteil, dass beispielsweise treppenstufige Aus- oder Einspeisungen in for-loops zu der Klasse hinzugefügt werden können (siehe unten).
Beim Export der Klasse werden die Etappen automatisch nummeriert und formatiert.
Wichtig ist dass die Parameter in einer 'dict' Klasse erstellt werden und die Schlüsselnamen den Parameternamen aus dem Handbuch entsprechen.
Siehe dafür die Dokumentation von :py:func:add_stage

.. code-block:: python
   :linenos:
   :lineno-start: 6

   Process_Data.add_stage({
      'TERMINATION_ID': 1,    # min p_cav
      'TERMINATION_QUANTITY': 2*24, #22 d
      'DT_MAX': 1,
      'FLOW_RATE': [0, 0]  ,
      'K_S': [0.15, 0.15] ,
      'P_BOUNDARY_CONDITION': ['RESERVOIR', 'WELLHEAD'],
      'BOUNDARY_PRESSURE': [0, 0.1],                          # 1 bar RR1 Druck
      'T_BOUNDARY_CONDITION':  ['NONE', 'NONE'],
      'BOUNDARY_TEMPERATURE': [0, 0],
   })

   Process_Data.add_stage({
      'TERMINATION_ID': 1,    # min p_cav
      'TERMINATION_QUANTITY': 500, #h
      'DT_MAX': 1,
      'FLOW_RATE': [5000, 0]  ,
      'K_S': [0.15, 0.15] ,
      'P_BOUNDARY_CONDITION': ['RESERVOIR', 'WELLHEAD'],
      'BOUNDARY_PRESSURE': [0, 0.1],                          # 1 bar RR1 Druck
      'T_BOUNDARY_CONDITION':  ['RESERVOIR', 'NONE'],
      'BOUNDARY_TEMPERATURE': [0, 0],
   })

2. Export
~~~~~~~~~~

.. code-block:: python
   :linenos:
   :lineno-start: 27

   Process_Data.export_processData(save_folder, project_name, subfolder='rate_%.2f' %(5000) )
   

Die entsprechende Prozessdatei hat folgende Gestalt:

.. code-block:: shell

   DESCRIPTION Beispiel
   N_FLUID	2
   NUMBER_OF_STAGES [/]	2

   MEDIUM_TYPE [/]
   GAS	BRINE

   MEDIUM_ID [/]
   Wasserstoff_100_Prozent	316

   COUPLED_ANNULI [integer required!]
   1	2



   # ++++++++++++++++++++++++++++++++
   STAGE	1
   # ++++++++++++++++++++++++++++++++

   TERMINATION_ID	1
   TERMINATION_QUANTITY	48
   DT_MAX	1
   FLOW_RATE
   0	0

   K_S
   0.15	0.15

   P_BOUNDARY_CONDITION
   RESERVOIR	WELLHEAD

   BOUNDARY_PRESSURE
   0	0.1

   T_BOUNDARY_CONDITION
   NONE	NONE

   BOUNDARY_TEMPERATURE
   0	0


   # ++++++++++++++++++++++++++++++++
   STAGE	2
   # ++++++++++++++++++++++++++++++++

   TERMINATION_ID	1
   TERMINATION_QUANTITY	500
   DT_MAX	1
   FLOW_RATE
   375.0	0

   K_S
   0.15	0.15

   P_BOUNDARY_CONDITION
   RESERVOIR	WELLHEAD

   BOUNDARY_PRESSURE
   0	0.1

   T_BOUNDARY_CONDITION
   RESERVOIR	NONE

   BOUNDARY_TEMPERATURE
   0	0





..    Creating recipes
.. ----------------

.. To retrieve a list of random ingredients,
.. you can use the ``lumache.get_random_ingredients()`` function:

.. .. py:function:: lumache.get_random_ingredients(kind=None)

..    Return a list of random ingredients as strings.

..    :param kind: Optional "kind" of ingredients.
..    :type kind: list[str] or None
..    :return: The ingredients list.
..    :rtype: list[str]


..    .. py:exception:: lumache.InvalidKindError

..    Raised if the kind is invalid.