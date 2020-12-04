"""
ref: https://d1d2qsbl8m0m72.cloudfront.net/en/products/databook/applinote/ic/power/switching_regulator/Buck_converter_efficiency_app-e.pdf
https://application-notes.digchip.com/070/70-41484.pdf
"""
from buck import Buck


# IXFN420N10T
class IXFN420N10T():
    name = "IXFN420N10T"
    v_in = 30.3  # Input Voltage
    v_out = 14.5  # Output Voltage
    i_out = 74.6  # Ouput Current
    r_ds_on_h = 2.3e-3  # High-side MOSFET on-resistance
    r_ds_on_l = 2.3e-3  # Low-side MOSFET on-resistance
    L = 28e-6  # Inductance value
    f_sw = 12.5e3  # Switching frequency
    tr_h = 155e-9  # High-side MOSFET rise time
    tf_h = 255e-9  # High-side MOSFET fall time
    tr_l = 155e-9  # Low-side MOSFET rise time
    tf_l = 255e-9  # Low-side MOSFET fall time
    v_d = 1.2  # Forward direction voltage of low-side MOSFET body diode
    i_rr = 7  # Peak value of body diode revverse recovery current
    t_rr = 140e-9  # Body diode reverse recovery time
    c_ds_h = 3.86e-09  # High-side MOSFET drain-source capacitance
    c_gd_h = 530e-12  # High-side MOSFET gate-drain capacitance
    c_ds_l = 3.86e-09  # Low-side MOSFET drain-source capacitance
    c_gd_l = 530e-12  # Low-side MOSFET gate-drain capacitance
    t_d_r = 162e-9  # Dead time for rising
    t_d_f = 162e-9  # Dead time for falling
    q_g_h = 670e-9  # Gate charge of high-side MOSFET
    q_g_l = 670e-9  # Gate charge of low-side MOSFET
    c_gs_h = 46.47e-9  # Gate capacitance of high-side MOSFET
    c_gs_l = 46.47e-9  # Gate capacitance of low-side MOSFET
    v_gs = 15  # Gate drive voltage
    i_cc = 20e-3  # IC current consumption
    DCR = 35e-3  # Inductor direct current resistance
    esr_c_in = 3e-3  # Equivalent series resistance of inpuee capacitor
    esr_c_out = 1e-3  # Equivalent series resistance of output capacitor

#FDBL86062
class FDBL86062():
    name = "FDBL86062"
    v_in = 36  # Input Voltage
    v_out = 12  # Output Voltage
    i_out = 100  # Ouput Current
    r_ds_on_h = 2e-3  # High-side MOSFET on-resistance
    r_ds_on_l = 2e-3  # Low-side MOSFET on-resistance
    L = 20e-6    # Inductance value
    f_sw = 12.5e3  # Switching frequency
    tr_h = 40e-9  # High-side MOSFET rise time
    tf_h = 19e-9  # High-side MOSFET fall time
    tr_l = 40e-9  # Low-side MOSFET rise time
    tf_l = 19e-9  # Low-side MOSFET fall time
    v_d = 1.25  # Forward direction voltage of low-side MOSFET body diode
    i_rr = 2*(273/184)  # Peak value of body diode revverse recovery current
    t_rr = 184e-9  # Body diode reverse recovery time
    c_ds_h = 5489e-12  # High-side MOSFET drain-source capacitance
    c_gd_h = 41e-12  # High-side MOSFET gate-drain capacitance
    c_ds_l = 5489e-12  # Low-side MOSFET drain-source capacitance
    c_gd_l = 41e-12  # Low-side MOSFET gate-drain capacitance
    t_d_r = 108e-9  # Dead time for rising
    t_d_f = 108e-9  # Dead time for falling
    q_g_h = 133e-9  # Gate charge of high-side MOSFET
    q_g_l = 133e-9  # Gate charge of low-side MOSFET
    c_gs_h = 976e-12  # Gate capacitance of high-side MOSFET
    c_gs_l = 976e-12  # Gate capacitance of low-side MOSFET
    v_gs = 15  # Gate drive voltage
    i_cc = 200e-3  # IC current consumption
    DCR = 1e-6  # Inductor direct current resistance
    esr_c_in = 3e-3  # Equivalent series resistance of inpuee capacitor
    esr_c_out = 1e-3  # Equivalent series resistance of output capacitor


if __name__ == '__main__':
    Buck.compute_and_print_all(FDBL86062)
    Buck.compute_and_print_all(IXFN420N10T)
