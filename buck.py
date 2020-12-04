"""
ref: https://d1d2qsbl8m0m72.cloudfront.net/en/products/databook/applinote/ic/power/switching_regulator/Buck_converter_efficiency_app-e.pdf
"""
class Buck:
    def compute_and_print_all(device: dict):
        print('p_on_high:", self.p_on_high(device))
        print('p_on_low:", self.p_on_low(device))
        print('p_sw_h:", self.p_sw_h(device))
        print('p_sw_l:", self.p_sw_l(device))
        print('p_diode:", self.p_diode(device))
        print('p_c_oss:", self.p_c_oss(device))
        print('p_dead:", self.p_dead(device))
        print('p_gate:", self.p_gate(device))
        print('p_gate_alt:", self.p_gate_alt(device))
        print('p_driver:", self.p_driver(device))
        print('p_inductor:", self.p_inductor(device))
        print('p_input_capacitor:", self.p_input_capacitor(device))
        print('p_output_capacitor:", self.p_output_capacitor(device))


    def p_on_high(device:dict):
        """ Compute high-side mosfet conduction losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        v_out = device.v_out
        i_out = device.i_out
        f_sw = device.f_sw
        L = device.L
        r_ds_on_h = device.r_ds_on_h

        d_il = ((v_in - v_out) / (f_sw * L)) * (v_out / v_in)
        i_p = i_out + (d_il/2)
        i_v = i_out - (d_il/2)
        p = (i_out**2 + ((i_p - i_v)**2) / 12 ) * r_ds_on_h * (v_out / v_in)
        return p


    def p_on_low(device:dict):
        """ Compute high-side mosfet conduction losses for a syncrhonous rectifier topology """
        v_in = device. v_in
        v_out = device.v_out
        i_out = device.i_out
        f_sw = device.f_sw
        L = device.L
        r_ds_on_l = device.r_ds_on_l
        d_il = ((v_in - v_out) / (f_sw * L)) * (v_out / v_in)
        i_p = i_out + (d_il/2)
        i_v = i_out - (d_il/2)
        p = (i_out**2 + ((i_p - i_v)**2) / 12 ) * r_ds_on_l * (1 -(v_out / v_in))
        return p


    def p_sw_h(device:dict):
        """ Compute mosfet switching losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        i_out = device.i_out
        t_r = device.tr_h
        t_f = device.tf_h
        f_sw = device.f_sw
        p = 0.5 * v_in * i_out * (t_r + t_f) * f_sw
        return p


    def p_sw_l(device:dict):
        """ Compute mosfet switching losses for a syncrhonous rectifier topology """
        v_d = device.v_d
        i_out = device.i_out
        t_r = device.tr_l
        t_f = device.tf_l
        f_sw = device.f_sw
        p = 0.5 * v_d * i_out * (t_r + t_f) * f_sw
        return p


    def p_diode(device:dict):
        """ Compute mosfet's diode body losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        i_rr = device.i_rr
        t_rr = device.t_rr
        f_sw = device.f_sw
        p = 0.5 * v_in * i_rr * t_rr * f_sw
        return p


    def p_c_oss(device:dict):
        """ Compute mosfet output capacitance losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        f_sw = device.f_sw
        c_ds_h = device.c_ds_h
        c_ds_l = device.c_ds_l
        c_gd_h = device.c_gd_h
        c_gd_l = device.c_gd_l
        c_oss_l = c_ds_l + c_gd_l
        c_oss_h = c_ds_h + c_gd_h
        p = 0.5 * (c_oss_l + c_oss_h) * v_in**2 * f_sw
        return p


    def p_dead(device: dict ):
        """ Compute mosfet dead time losses for a syncrhonous rectifier topology """
        v_d = device.v_d
        i_out = device.i_out
        t_d_r = device.t_d_r
        t_d_f = device.t_d_f
        f_sw = device.f_sw
        p = v_d * i_out * (t_d_r + t_d_f) * f_sw
        return p


    def p_gate(device: dict ):
        """ Compute mosfet gate charge losses for a syncrhonous rectifier topology """
        c_gs_h = device.c_gs_h
        c_gs_l = device.c_gs_l
        v_gs = device.v_gs
        f_sw = device.f_sw
        p = (c_gs_h + c_gs_l) * v_gs**2 * f_sw
        return p


    def p_gate_alt(device: dict):
        """ Compute mosfet gate charge losses for a syncrhonous rectifier topology """
        q_g_h = device.q_g_h
        q_g_l = device.q_g_l
        v_gs = device.v_gs
        f_sw = device.f_sw
        p = (q_g_h + q_g_l) * v_gs * f_sw
        return p


    def p_driver(device: dict):
        """ Compute mosfet driver losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        i_cc = device.i_cc
        p = v_in * i_cc
        return p


    def p_inductor(device: dict):
        """ Compute inductor losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        v_out = device.v_out
        i_out = device.i_out
        i_cc = device.i_cc
        f_sw = device.f_sw
        L = device.L
        DCR = device.DCR

        d_il = ((v_in - v_out) / (f_sw * L)) * (v_out / v_in)
        i_p = i_out + (d_il/2)
        i_v = i_out - (d_il/2)

        p = (i_out**2 + (i_p - i_v)**2/12) * DCR
        return p


    def p_input_capacitor(device: dict):
        """ Compute input capacitor losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        v_out = device.v_out
        i_out = device.i_out
        esr_c_in = device.esr_c_in
        i_c_in_rms = i_out * ((v_in - v_out) * v_out)**(1/2) / v_in
        p = i_c_in_rms**2 * esr_c_in
        return p


    def p_output_capacitor(device: dict):
        """ Compute output capacitor losses for a syncrhonous rectifier topology """
        v_in = device.v_in
        v_out = device.v_out
        f_sw = device.f_sw
        L = device.L
        esr_c_out = device.esr_c_out
        d_il = ((v_in - v_out) / (f_sw * L)) * (v_out / v_in)
        i_c_out_rms = d_il/(2 * (3)**(1/2))
        p = i_c_out_rms**2 * esr_c_out
        return p
