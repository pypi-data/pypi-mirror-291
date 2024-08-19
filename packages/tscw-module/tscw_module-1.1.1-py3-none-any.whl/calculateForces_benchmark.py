from tscw_module import calculate_forces
import numpy as np
from pathlib import Path
import pandas as pd
import unittest

'''
Unit Test for calculating axial forces.
Benchmark data from BB122 - Ausspeisung
"L:\Projekte\SG-UBT\40_Thermodynamik\Berichte\berechnungenbbg_rev2_2011.xls"
'''

def check_list(list1, list2):
    tolerance_digits = 3
    for val1, val2 in zip(list1, list2):
        if np.round(val1, tolerance_digits) != np.round(val2, tolerance_digits):
            return False
    return True

class ForcesBenchmark(unittest.TestCase):
    def test_axial_forces(self):
        # Validation with Excel from 2011 - BB122
        T0 = 15 #
        t_vector = np.array([15.0, 18.3, 18.1, 17.8, 17.2,]) # T
        p_vector = np.array([91.000, 90.850, 90.250, 89.350, 88.200])/10 # MPa
        t_total  = t_stage = np.array([ 0, 1, 2, 4, 7 ]) # h
        i_etappe = len(t_total) * [1]

        meta_data = {'mu'          : 0.3,
                    'alpha'        : 1.24e-05,
                    'e_modul_stahl': 2.06e11,
                    'z_bezug'      : 425 * 0.5,
                    'rho_rrsf'     : 1200,
                    'wd'           : 0.00984,
                    'd_a'          : 0.219075,
                    }

        df = calculate_forces(meta_data, t_vector, p_vector, t_total, t_stage, i_etappe, T0, 3)
        expected_Fz_ges = [123.626504,   68.822167,   71.002468,   74.272920,   82.031644]
        self.assertTrue(check_list(df.Fz_ges, expected_Fz_ges))


if __name__ == '__main__':
    unittest.main()
