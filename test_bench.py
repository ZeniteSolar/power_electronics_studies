"""
ref: https://d1d2qsbl8m0m72.cloudfront.net/en/products/databook/applinote/ic/power/switching_regulator/buck_converter_efficiency_app-e.pdf
"""
import unittest
from buck import Buck

class TestBuck(unittest.TestCase):
    class Example():
        v_in = 12  # Input Voltage
        v_out = 5  # Output Voltage
        i_out = 3  # Ouput Current
        r_ds_on_h = 100e-3  # High-side MOSFET on-resistance
        r_ds_on_l = 70e-3  # Low-side MOSFET on-resistance
        L = 7e-6  # Inductance value
        f_sw = 1e6  # Switching frequency
        tr_h = 4e-9  # High-side MOSFET rise time
        tf_h = 6e-9  # High-side MOSFET fall time
        tr_l = 2e-9  # Low-side MOSFET rise time
        tf_l = 2e-9  # Low-side MOSFET fall time
        v_d = 0.5  # Forward direction voltage of low-side MOSFET body diode
        i_rr = 0.3  # Peak vvalue of body diode revverse recovery current
        t_rr = 25e-9  # Body diode reverse recovery time
        c_ds_h = 40e-12  # High-side MOSFET drain-source capacitance
        c_gd_h = 40e-12  # High-side MOSFET gate-drain capacitance
        c_ds_l = 40e-12  # Low-side MOSFET drain-source capacitance
        c_gd_l = 40e-12  # Low-side MOSFET gate-drain capacitance
        t_d_r = 30e-9  # Dead time for rising
        t_d_f = 30e-9  # Dead time for falling
        q_g_h = 1e-9  # Gate charge of high-side MOSFET
        q_g_l = 1e-9  # Gate charge of low-side MOSFET
        c_gs_h = 200e-12  # Gate capacitance of high-side MOSFET
        c_gs_l = 200e-12  # Gate capacitance of low-side MOSFET
        v_gs = 5  # Gate drive voltage
        i_cc = 1e-3  # IC current consumption
        DCR = 80e-3  # Inductor direct current resistance
        esr_c_in = 3e-3  # Equivalent series resistance of inpuee capacitor
        esr_c_out = 1e-3  # Equivalent series resistance of output capacitor


    def test_p_on_high(self):
        a = Buck.p_on_high(self.Example)
        self.assertAlmostEqual(a, 376e-3, delta=1e-3)


    def test_p_on_low(self):
        a = Buck.p_on_low(self.Example)
        self.assertAlmostEqual(a, 369e-3, delta=1e-3)


    def test_p_sw_h(self):
        a = Buck.p_sw_h(self.Example)
        self.assertAlmostEqual(a, 180e-3, delta=1e-3)


    def test_p_sw_l(self):
        a = Buck.p_sw_l(self.Example)
        self.assertAlmostEqual(a, 3e-3, delta=1e-3)


    def test_p_diode(self):
        a = Buck.p_diode(self.Example)
        self.assertAlmostEqual(a, 45e-3, delta=1e-3)


    def test_p_c_oss(self):
        a = Buck.p_c_oss(self.Example)
        self.assertAlmostEqual(a, 11.5e-3, delta=1e-3)


    def test_p_dead(self):
        a = Buck.p_dead(self.Example)
        self.assertAlmostEqual(a, 90e-3, delta=1e-3)


    def test_p_gate(self):
        a = Buck.p_gate(self.Example)
        self.assertAlmostEqual(a, 10e-3, delta=1e-2)


    def test_p_gate_alt(self):
        a = Buck.p_gate_alt(self.Example)
        self.assertAlmostEqual(a, 10e-3, delta=1e-3)


    def test_p_driver(self):
        a = Buck.p_driver(self.Example)
        self.assertAlmostEqual(a, 12e-3, delta=1e-3)


    def test_p_inductor(self):
        a = Buck.p_inductor(self.Example)
        self.assertAlmostEqual(a, 723e-3, delta=4e-3)


    def test_p_input_capacitor(self):
        a = Buck.p_input_capacitor(self.Example)
        self.assertAlmostEqual(a, 6.6e-3, delta=1e-3)


    def test_p_output_capacitor(self):
        a = Buck.p_output_capacitor(self.Example)
        self.assertAlmostEqual(a, 0.5e-3, delta=1e-3)


if __name__ == '__main__':
    unittest.main()
