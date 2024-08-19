TSCW - OUTPUT - Axialkraftberechnung
========

Das Ziel der Thermodynamischen Berechnungen besteht darin, die mittleren Drücke und Temperaturen in Abhängigkeit von Verrohrung und Raten zu ermitteln, um die Belastungsansätze Fz,max und Fz,min zu bestimmen.

Axialkraftberechnung - Theorie
---------------------

Die resultierende Axialkraft Fz,ges setzt sich aus der thermischen Belastung (1) und dem Ballooning (2) zusammen:

.. math::
    Fz_{ges} = \underbrace{F_{t}}_{(1)} + \underbrace{F_{p}}_{(2)}

Die Axialkräfte werden für die Bezugsteufe in der Bohrung :math:`z=z_m` berechnet.

Thermische Belastung (1)
''''''''''''''''''''''

Die thermische Belastung (1) ergibt sich aus:

.. math::
    F_{T}(z,t) = \alpha_S \Delta T(z,t) E A

wobei:

- :math:`\alpha_S`: Wärmeausdehnungskoeffizient (12.4 x 10^{-6} K^{-1})
- :math:`\Delta T`: Temperaturänderung zum Initialzustand :math:`\Delta T(z,t) = T_0 - T(z_m,t)`
- :math:`E`: Elastizitätsmodul (2.06 x 10^5 MPa)
- :math:`A`: Querschnittsfläche des Rohres

Ballooning (2)
''''''''''''''''''''''

Je nach Druckregime :math:`\Delta p = p(z_m,t) - p_0` kann zwischen Ballooning und Kontraballooning unterschieden werden:

.. math::
    F_{p_i}(z,t) = \frac{2\mu \Delta p(z,t) A}{ (R^2 - 1)} \quad \text{wenn} \quad \Delta p > 0

.. math::
    F_{p_a}(z,t) = \frac{2\mu \Delta p(z,t) A R^2}{ (R^2 - 1)} \quad \text{wenn} \quad \Delta p < 0

wobei:

- :math:`\mu`: Querdehnungszahl Stahl (0.3)
- :math:`\Delta p`: Druckänderung zum Initialzustand
- :math:`A`: Querschnittsfläche des Rohres
- :math:`R = D/d > 1`: Durchmesserverhältnis


Axialkraftberechnung in TSCW
---------------------

.. py:function:: calculate_axial_forces(meta_data, z_ref, T0:float = None, is_export:bool = False)

        :param meta_data:  Meta Daten.
        :type meta_data: dict
        :param z_ref: Bezugsteufe (= z_m)
        :type z_ref: _type_
        :param T0:  Die anfängliche Temperatur für die Referenz in delta_T (optional). Andernfalls entspricht sie dem ersten Element des Temperaturarrays.
        :type T0: float, optional
        :param is_export: Export der Ergebnisse im xlsx File, defaults to False
        :type is_export: bool, optional
        :return: pandas dataframe containing forces
        :rtype: pd.Dataframe


Die Variable ``meta_data`` enthält dabei folgende Struktur

+----------------+------------------------+-----------------------------------------------+------------+
| **Variable**   | **Wert (Beispiel)**    | **Beschreibung**                              | **Einheit**|
+================+========================+===============================================+============+
| mu             | 0.3                    | Querdehnungszahl                              | [-]        |
+----------------+------------------------+-----------------------------------------------+------------+
| alpha          | 0.0000124              | Wärmeausdehnungskoeffizient                   | 1/K        |
+----------------+------------------------+-----------------------------------------------+------------+
| e_modul_stahl  | 2.06E+11               | E-Modul Stahl                                 | Pa         |
+----------------+------------------------+-----------------------------------------------+------------+
| z_bezug        | 425                    | Bezugsteufe (i.d.R. Bohrlochmitte)            | m          |
+----------------+------------------------+-----------------------------------------------+------------+
| rho_rrsf       | 1200                   | Dichte Ringraumschutzflüssigkeit              | kg/m³      |
+----------------+------------------------+-----------------------------------------------+------------+
| wd             | 0.00984                | Wanddicke                                     | m          |
+----------------+------------------------+-----------------------------------------------+------------+
| d_a            | 0.219075               | Außendurchmesser                              | m          |
+----------------+------------------------+-----------------------------------------------+------------+



.. code-block:: python
    :linenos:

    from tscw_module import TSCW_TBHC

    tscw_data = TSCW_TBHC("Beispiel_1_pTBHC.TXT")

    meta_data = {'mu': 0.3,
                 'alpha': 1.24e-05,
                 'e_modul_stahl': 206000000000.0,
                 'z_bezug': 425.0,
                 'rho_rrsf': 1200.0,
                 'wd': 0.00984,
                 'd_a': 0.219075}

    T_0 = 15 # °C
    depth_ref = meta_data['z_bezug'] 

    tswc_data.calculate_axial_forces(meta_data, depth_ref, T_0)   
    tswc_data.plot_axial_forces()


.. image:: ../_static/BB_Gruppe1_Bb122_DetailedModel_1_Ausspeisung_1_pTBHC_forces.png
  :width: 700
  :alt: BB_Gruppe1_Bb122_DetailedModel_1_Ausspeisung_1_pTBHC_forces.png


Bestimmung von :math:`Fz_{max}` und :math:`Fz_{min}`
---------------------

Nachdem die Axialkräfte mit Hilfe von ``calculate_axial_forces()`` berechnet worden sind, können pro Etappe die enstsprechenden Parameter,
an denen entweder `Fz_{max}` oder :math:`Fz_{min}` wirken, extrahiert werden.

.. py:function:: extract_max_force(i_etappe:int, mode:str, min_time:float = 0)

    :param i_etappe: Etappen-Nummer
    :type i_etappe: int
    :param mode: entweder 'min' oder 'max' für :math:`Fz_{min}` oder `Fz_{max}`. 
    :type mode: str
    :param min_time: Die Zeitspanne, ab der nach der Suche nach den Extremwerten begonnen wird.
                    Um das Ende der Phase auszuwählen, wird der Wert auf ``+np.inf``.
                    Standardmäßig beträgt die Mindestzeit 0.
    :type min_time: float, optional
    :return: pd.Dataframe containing relevant parameters, respective index in self.df
    :rtype: _type_


Wenn bspw. für das vorherige Beispiel die enstprechenden Werte für  :math:`Fz_{max}` in Etappe 2 beginnend ab 2h extrahiert werden sollen, kann dies mit folgendem Befehl erreicht werden.

.. code-block:: python
    :linenos:
    :lineno-start: 18

    i_etappe = 2
    mode = 'max'
    min_time = 2

    filtered_df, df_index = tswc_data.extract_max_force(i_etappe, mode, min_time)

Die Ergebnisse für ``filtered_df`` und ``df_index`` sind:

.. code-block:: shell

    >>filtered_df
    STAGE          2.000000
    t_TOTAL       82.965351
    t_STAGE       55.274952
    p_m            6.549749
    T_m            7.234806
    delta_T        7.765194
    delta_p        4.048199
    Fz_t         128.298185
    Fz_p          75.845804
    Fz_ges       204.143989
    Fz_p_rr       23.706678
    Fz_ges_rr    152.004863
    Name: 181, dtype: float64

    >>df_index 
    181