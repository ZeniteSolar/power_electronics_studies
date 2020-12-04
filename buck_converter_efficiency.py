"""
ref: https://d1d2qsbl8m0m72.cloudfront.net/en/products/databook/applinote/ic/power/switching_regulator/Buck_converter_efficiency_app-e.pdf
"""
from buck import Buck


# IXFN420N10T
class IXFN420N10T():
    v_in = 50  # Input Voltage
    v_out = 50  # Output Voltage
    i_out = 150  # Ouput Current
    r_ds_on_h = 2.3e-3  # High-side MOSFET on-resistance
    r_ds_on_l = 2.3e-3  # Low-side MOSFET on-resistance
    """ TODO:
    #L = 7e-6  # Inductance value
    f_sw = 12e3  # Switching frequency
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
    """

if __name__ == '__main__':
    Buck.compute_and_print_all(IXFN420N10T)
