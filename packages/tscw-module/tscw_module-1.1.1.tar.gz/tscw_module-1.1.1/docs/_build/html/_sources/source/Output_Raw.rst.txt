TSCW - OUTPUT - Plots und Daten Export
=======


TBHC.txt
------------

Druck- und Temperaturergebnisse in Kaverne und im Strömungsraum i
Pro Zeitschritt werden hier die Druck- und Temperaturwerte in der Kaverne und für jeden
Strömungsraum pro Schicht ausgegeben. Der Index i steht für die Nummer des
Strömungsraumes (Tubing bzw. Ringraum), hochgezählt beginnend von der Bohrlochachse.
Die Struktur dieser Datei kann in drei Teile gegliedert werden, die durch \*\*\*
voneinander getrennt sind. Die ersten Zeilen sind im Folgenden exemplarisch dargestellt:



.. code-block:: python

    FLUID SPACE NO.:	               1
    MEDIUM:	Stage 1: GAS.Methan
    V_CAVERN:	488925.22
    ***	      
    STAGE	t_STAGE	t_TOTAL	T_CAVERN	p_CAVERN	T_BRINE_EQ	  T_WH	  p_WH	PRODUCT AMOUNT	FLOW_RATE	 w_MAX	***	  0.00	 25.00	 50.00	 75.00	100.00	125.00	150.00	175.00	200.00	225.00	250.00	275.00	300.00	325.00	350.00	375.00	400.00	425.00	450.00	475.00	500.00	525.00	550.00	575.00	600.00	625.00	650.00	675.00	700.00	725.00	750.00	775.00	800.00	825.00	850.00	875.00	900.00	925.00	950.00	975.00	1000.00	1100.00	***	  0.00	 25.00	 50.00	 75.00	100.00	125.00	150.00	175.00	200.00	225.00	250.00	275.00	300.00	325.00	350.00	375.00	400.00	425.00	450.00	475.00	500.00	525.00	550.00	575.00	600.00	625.00	650.00	675.00	700.00	725.00	750.00	775.00	800.00	825.00	850.00	875.00	900.00	925.00	950.00	975.00	1000.00	1100.00
    1	   0.00	   0.00	   24.26	   15.00	     24.26	 10.00	 13.05	   80400839.05	100000.00	 10.70	***	 10.00	 11.00	 12.00	 13.00	 14.00	 15.00	 16.00	 17.00	 18.00	 19.00	 20.00	 21.00	 22.00	 23.00	 24.00	 25.00	 26.00	 27.00	 28.00	 29.03	 30.00	 30.78	 31.50	 32.25	 33.00	 33.75	 34.50	 35.28	 36.00	 36.53	 37.00	 37.50	 38.00	 38.50	 39.00	 39.50	 40.00	 41.61	 41.00	 34.85	  24.26	  24.26	***	 13.05	 13.10	 13.15	 13.19	 13.24	 13.28	 13.33	 13.38	 13.42	 13.47	 13.51	 13.56	 13.61	 13.65	 13.70	 13.74	 13.79	 13.83	 13.88	 13.93	 13.97	 14.02	 14.06	 14.11	 14.15	 14.20	 14.25	 14.29	 14.34	 14.38	 14.43	 14.47	 14.52	 14.57	 14.61	 14.66	 14.70	 14.75	 14.79	 14.84	  14.88	  15.00
    1	   0.00	   0.00	   24.26	   15.00	     24.26	 10.59	 13.05	   80400709.24	100000.00	 10.71	***	 10.59	 11.60	 12.60	 13.60	 14.60	 15.60	 16.60	 17.60	 18.60	 19.60	 20.60	 21.60	 22.60	 23.60	 24.61	 25.61	 26.61	 27.62	 28.61	 29.55	 30.42	 31.19	 31.92	 32.67	 33.43	 34.19	 34.93	 35.61	 36.24	 36.76	 37.24	 37.74	 38.24	 38.74	 39.24	 40.15	 40.24	 38.19	 34.71	 30.10	  24.26	  24.26	***	 13.05	 13.10	 13.15	 13.19	 13.24	 13.28	 13.33	 13.38	 13.42	 13.47	 13.51	 13.56	 13.61	 13.65	 13.70	 13.74	 13.79	 13.83	 13.88	 13.93	 13.97	 14.02	 14.06	 14.11	 14.15	 14.20	 14.25	 14.29	 14.34	 14.38	 14.43	 14.47	 14.52	 14.56	 14.61	 14.66	 14.70	 14.75	 14.79	 14.84	  14.88	  15.00
    1	   0.00	   0.00	   24.26	   15.00	     24.26	 11.08	 13.05	   80400579.44	100000.00	 10.73	***	 11.08	 12.09	 13.09	 14.09	 15.09	 16.09	 17.09	 18.09	 19.09	 20.09	 21.09	 22.09	 23.10	 24.10	 25.10	 26.10	 27.10	 28.08	 29.03	 29.93	 30.77	 31.53	 32.27	 33.02	 33.77	 34.50	 35.20	 35.85	 36.44	 36.95	 37.44	 37.94	 38.44	 39.09	 39.44	 39.17	 38.02	 35.38	 31.95	 28.31	  24.26	  24.26	***	 13.05	 13.10	 13.15	 13.19	 13.24	 13.28	 13.33	 13.38	 13.42	 13.47	 13.51	 13.56	 13.61	 13.65	 13.70	 13.74	 13.79	 13.83	 13.88	 13.93	 13.97	 14.02	 14.06	 14.11	 14.15	 14.20	 14.25	 14.29	 14.34	 14.38	 14.43	 14.47	 14.52	 14.56	 14.61	 14.66	 14.70	 14.75	 14.79	 14.84	  14.88	  15.00
    1	   0.00	   0.00	   24.26	   15.00	     24.26	 11.51	 13.05	   80400449.63	100000.00	 10.74	***	 11.51	 12.51	 13.51	 14.52	 15.52	 16.52	 17.52	 18.52	 19.52	 20.52	 21.52	 22.52	 23.52	 24.53	 25.53	 26.52	 27.50	 28.46	 29.37	 30.24	 31.07	 31.83	 32.57	 33.31	 34.04	 34.75	 35.41	 36.03	 36.61	 37.12	 37.61	 38.16	 38.61	 38.89	 38.71	 37.74	 36.05	 33.49	 30.48	 27.45	  24.26	  24.26	***	 13.05	 13.10	 13.15	 13.19	 13.24	 13.28	 13.33	 13.38	 13.42	 13.47	 13.51	 13.56	 13.61	 13.65	 13.70	 13.74	 13.79	 13.83	 13.88	 13.93	 13.97	 14.02	 14.06	 14.11	 14.15	 14.20	 14.24	 14.29	 14.34	 14.38	 14.43	 14.47	 14.52	 14.56	 14.61	 14.66	 14.70	 14.75	 14.79	 14.84	  14.88	  15.00
    1	   0.01	   0.01	   24.26	   15.00	     24.26	 11.90	 13.05	   80400319.83	100000.00	 10.75	***	 11.90	 12.90	 13.91	 14.91	 15.91	 16.91	 17.91	 18.91	 19.91	 20.91	 21.91	 22.91	 23.91	 24.91	 25.91	 26.89	 27.85	 28.78	 29.68	 30.53	 31.34	 32.10	 32.83	 33.56	 34.27	 34.95	 35.60	 36.20	 36.76	 37.29	 37.76	 38.20	 38.43	 38.29	 37.68	 36.38	 34.55	 32.18	 29.54	 26.94	  24.26	  24.26	***	 13.05	 13.10	 13.15	 13.19	 13.24	 13.28	 13.33	 13.38	 13.42	 13.47	 13.51	 13.56	 13.61	 13.65	 13.70	 13.74	 13.79	 13.83	 13.88	 13.93	 13.97	 14.02	 14.06	 14.11	 14.15	 14.20	 14.24	 14.29	 14.34	 14.38	 14.43	 14.47	 14.52	 14.56	 14.61	 14.65	 14.70	 14.75	 14.79	 14.84	  14.88	  15.00
    1	   0.01	   0.01	   24.26	   15.00	     24.26	 12.27	 13.06	   80400190.02	100000.00	 10.76	***	 12.27	 13.27	 14.28	 15.28	 16.28	 17.28	 18.28	 19.28	 20.28	 21.28	 22.28	 23.28	 24.28	 25.27	 26.25	 27.22	 28.16	 29.08	 29.95	 30.79	 31.59	 32.34	 33.06	 33.78	 34.47	 35.14	 35.77	 36.36	 36.90	 37.40	 37.78	 38.03	 37.99	 37.54	 36.66	 35.22	 33.38	 31.21	 28.87	 26.58	  24.26	  24.26	***	 13.06	 13.10	 13.15	 13.19	 13.24	 13.28	 13.33	 13.38	 13.42	 13.47	 13.51	 13.56	 13.61	 13.65	 13.70	 13.74	 13.79	 13.83	 13.88	 13.93	 13.97	 14.02	 14.06	 14.11	 14.15	 14.20	 14.24	 14.29	 14.34	 14.38	 14.43	 14.47	 14.52	 14.56	 14.61	 14.65	 14.70	 14.75	 14.79	 14.84	  14.88	  15.00
    (weiter bis zum Simulationsende)

Die ``*TBHC.txt`` Datei kann mit folgendem Befehl eingelesen werden:

.. code-block:: python
   :linenos:

    from tscw_module import TSCW_TBHC
    from pathlib import Path

    path = Path(r"DeinPfad/*TBHC.txt")
    tscw_data = TSCW_TBHC(path) 

Die einzelnen Parameter können folgerndermaßen aufgerufen werden:

.. code-block:: python
   :linenos:

    # Sobald die TSCW_TBHC Klasse initiiert wurde, können einzelnen Parameter aufgerufen werden.

    tscw_data.df            # Übersicht aller eingeladenen Daten (pandas.DataFrame)
    tscw_data.sr_df         # pandas DataFrame von den Meta Daten 
    tscw_data.vertT_df      # pandas DataFrame von den Temperatur daten
    tscw_data.vertP_df      # pandas DataFrame von den Druck daten

    tscw_data.t_total       # Numpy Array über Simulationszeit 
    tscw_data.t_etappe      # Numpy Array über jeweilige Etappenzeit
    tscw_data.stage_idx     # Numpy Array über Etappennummer
    tscw_data.depth_array   # Numpy Array über simulierter vertikale Stützpunkte


Excel/CSV Export
''''''''''''''''''''''

``Pandas Dataframe`` Formate können mühelos als csv oder xlsx Datei exportiert werden.
Falls beispielsweise die gesamte ``*TBHC.txt`` Datei in ein bearbeitbares Excel File konvertiert werden möchte, 
kann dies mit folgendem Befehl ausgeführt werden:

.. code-block:: python
   :linenos:

    import pandas as pd
    tscw_data.df.to_excel('Export.xlsx', header = True, index = False)

.. note:: Dies gilt analog für eingelesene TFC.txt und TFBH.txt Dateien.

Plots
^^^^^^^^^^

Temperatur und Druck vs Zeit
''''''''''''''''''''''

Die Druck- und Temperaturverteilung über die Zeit kann mit der Funktion ``plot_tp_vs_time()``
geplottet werden:

.. py:function:: plot_tp_vs_time(depth_t, depth_p, is_export)

    :param depth_t: Die Tiefenintervalle für Temperatur, standardmäßig alle
    :type depth_t: array, optional
    :param depth_p:  Die Tiefenintervalle für Druck, standardmäßig alle
    :type depth_p: array, optional
    :param is_export: standardmäßig False
    :type is_export: bool, optional

.. hint::
    
    Die Tiefenintervalle müssen nicht 1:1 mit den simulierten übereinstimmen. 
    Im Algorithmus wird nach dem nächst gelegenen Intervall gesucht.

Zum Beispiel liefert der Code:

.. code-block:: python
   :linenos:

   from tscw_module import TSCW_TBHC
   from pathlib import Path
   path = Path(r"DeinPfad/*TBHC.txt")
   tscw_data = TSCW_TBHC(path) 
   depths = [0.0,122.5,245.0,367.5,490.0]
   tscw_data.plot_tp_vs_time(depths,depths)

.. image:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_1_pTBHCtp_vs_time.png
  :width: 700
  :alt: BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_1_pTBHCtp_vs_time.png


Temperatur und Druck vs Tiefe
''''''''''''''''''''''

Analog können die Daten über die Tiefe geplotted werden.

Zum Beispiel liefert der Code:

.. code-block:: python
   :linenos:
   :lineno-start: 6

   times = np.array([0, 10, 100])
   tscw_data.plot_tp_vs_depth(time_t=depths, time_p=[])

.. hint::

    In diesem Beispiel wurde mit ``time_p=[]`` keine Druckdaten ausgewählt.
    Somit erscheinen im Plot nur Temperaturdaten für die ausgewählten Zeitpunkte.
    Analog ist dies auch in der Funktion ``plot_tp_vs_time`` mit den Tiefenintervallen möglich. 

.. image:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_1_pTBHCtp_vs_depth.png
  :width: 700
  :alt: BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_1_pTBHCtp_vs_depth.png











TFBH.txt
------------
Diese Datei beinhaltet das berechnete Temperaturfeld um die Bohrlochachse für jeden
Zeitschritt mit selbsterklärender Darstellung (analog zum 2. Teil der Datei *_i_
pTBHC.txt).

Die Datei kann folgendermaßen eingelesen werden:


.. code-block:: python
   :linenos:

    from tscw_module import TSCW_TBHC
    from pathlib import Path
    path = Path(r"DeinPfad/*TFBH.txt")
    tfbh_data = TSCW_TFBH(path)


Plots
^^^^^^^^^^

Die Temperaturverteilung entlang des Bohrlochs mit der Funktion ``plot_temp_distribution()``
dargestellt werden:

.. py:function::  plot_temp_distribution(times, depths, range_radial, is_colormap, is_export, field_data_picklePath:str = None)

        :param times: Zeitpunkte zum plotten in [h]
        :type times: list
        :param depths:  darzustellende Teufen, standartmäßig werden alle Stützpunkte dargestellt. 
        :type depths: list, optional
        :param range_radial:  [x0, x1] Grenzwerte der x-Achse in [m], defaults to None
        :type range_radial: list, optional
        :param is_colormap: Plot als a colormap oder line plot, defaults to True
        :type is_colormap: bool, optional
        :param is_export: export figure into parent folder of file, defaults to False
        :type is_export: bool, optional
        :param field_data_picklePath: Pfad zur (/*.pickle)-Datei der Klasse FieldData (falls sie exportiert wurde). Wenn geladen, wird die Geometrie im Hintergrund angezeigt. Standardmäßig ist dies auf None gesetzt.
        :type field_data_picklePath: str
        :rtype: figure


So liefern beispielsweise die Befehle:

.. code-block:: python
   :linenos:

    import matplotlib.pyplot as plt
    tfbh_data.plot_temp_distribution(times = [0, 10, 100], range_radial=[0, 0.5], is_colormap = True)
    tfbh_data.plot_temp_distribution(times = [0, 10, 100], depths = [0, 200, 400], range_radial=[0, 0.5], is_colormap = False)
    plt.show()

..
    |colormap-pic| |radial-pic|

    .. |colormap-pic| image:: BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH_colormap_16.png
    :width: 45%

    .. |radial-pic| image:: BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH_radial_3.png
    :width: 45%




.. list-table:: plot_temp_distribution\(\)
   :width: 100%
   :class: borderless

   * - isColormap = True

     - isColormap = False

   * - .. image:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH_colormap_16.png
          :width: 100%
         
     - .. image:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH_radial_3.png
          :width: 100%

Animation
^^^^^^^^^^

Der Temperaturverlauf kann ebenfalls als time lapse mit der Funktion ``create_movie()`` dargestellt werden
.

.. py:function::  create_movie(range_radial, is_export, n_levels, field_data_picklePath)

        :param range_radial: [x0, x1] Bereich des radialen Start- und Endpunktes (keine exakte Übereinstimmung erforderlich), Standardwert ist None
        :type range_radial: Liste, optional
        :param is_export: exportiert den Film als .mp4 in den gleichen Ordner wie die aktuelle Instanz, Standardwert ist False
        :type is_export: bool, optional
        :param n_levels: wie viele Ebenen für plt.contourf, Standardwert ist 100
        :type n_levels: int, optional
        :param field_data_picklePath: Pfad zu (/*.pickle) der FieldData-Klasse (wenn sie exportiert wurde). Wenn geladen, wird die Geometrie im Hintergrund angezeigt, Standardwert ist None
        :type field_data_picklePath: str, optional
        :return: Animation
        :rtype: animation.FuncAnimation

In unserem Beispiel kann mit folgendem Befehl der Zeitraffer exportiert werden.

.. code-block:: python

    # ohne Modellgeomtrie im Hintergrund
    tfbh_data.create_movie(range_radial = [0, 0.5], is_export = True)

    # mit Modellgeomtrie im Hintergrund
    geometry_path = Path(r"*.pickle")
    tfbh_data.create_movie(range_radial = [0, 0.5], is_export = True, field_data_picklePath = geometry_path)

    >>> Saving L:\Projekte\SG-UBT\40_Thermodynamik\TSWC_GACA_Bernburg\Gruppe1\BB_Gruppe1_Bb122\Ausspeisung_DruckKriterium\SaveFolder\BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH.mp4
    >>> 100%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| 1100/1100 [01:39<00:00, 11.07it/s] 


.. list-table::
    :width: 100%
    :class: borderless

    * - ``field_data_picklePath = None``

      - ``field_data_picklePath = geometry_path``

    * - .. video:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH.mp4
            :class: video-bordered
            :alt: Animation
            :width: 300

      - .. video:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFBH_geom.mp4
            :class: video-bordered
            :alt: Animation
            :width: 300



TFC.txt
------------
Diese Datei beinhaltet das berechnete Temperaturfeld um die Kaverne für jeden Zeitschritt
mit selbsterklärender Darstellung.


Analog zu der Methode in TFBH.txt kann mit ``plot_temp_distribution()`` der Temperaturverlauf in der Kaverne für verschiedene Zeitpunkte geplottet werden.

.. code-block:: python

    from tscw_module import TSCW_TFC
    from pathlib import Path
    import matplotlib.pyplot as plt

    tfc_data = TSCW_TFC(Path(r"deinPfad/*TFC.txt"))
    tfc_data.plot_temp_distribution(times = [0, 100, 200], range_radial = [30, 50])

    plt.show()

.. image:: ../_static/BB_Gruppe1_Bb122Ausspeisung_DruckKriterium_TFC_cavern_temp.png
    :width: 100%



Vergleich verschiedener Simulation
------------

Die Simulationsergebnisse verschiedener Varianten können folgender Methode verglichen werden: 

.. py:function:: plot_pt_difference(depths, save_folder:Path, xlimits, *args) 

        :param depths: zu plottende Teufen
        :type depths: list
        :param save_folder: Pfad zum Ordner
        :type save_folder: Path, bei None wird die Datei nicht gespeichert.
        :param xlimits: Min. und max. Limit der x-Achse (Zeit), wenn None angegeben wird, wird die Achsenlimits automatisch gewählt.
        :type xlimits: List (x1, x2)
        :param args: Liste mit anderen OIbjekten der Klasse TSWC_TBHC.
        :type args: list of TSWC_TBHC instances.

Beispiel:

.. code-block:: python

    from pathlib import Path
    import matplotlib.pyplot as plt
    from tscw_module import TSCW_TBHC

    path1 = Path(r'Kh48_CH4_pres1.00_A5.46e-05_B8.10e-09h952.6_T32.4rate_208.33__1_pTBHC.TXT')
    path2 = Path(r'Kh48_H2_pres1.00_A5.46e-05_B8.10e-09h952.6_T32.4rate_208.33__1_pTBHC.TXT')

    TbhcData_1 = TSCW_TBHC(path1)
    TbhcData_1.name = 'CH4 - 4999 Nm3/d - mit Minsky'
    TbhcData_2 = TSCW_TBHC(path2)
    TbhcData_2.name = 'H2 - 4999 Nm3/d - mit Minsky'

    TbhcData_1.plot_pt_difference([0, 467, 935], None, None, TbhcData[1:])
    plt.show()


.. image:: ../_static/Figure_1.png
    :width: 100%


Falls die Axialkraft für die jeweiligen Objekte ebenfalls berechnet worden ist, kann analog mit der Methode ``plot_forces_difference()`` die Axialkraftverteilung geplottet werden.


.. image:: ../_static/Figure_2.png
    :width: 100%