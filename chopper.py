"""
ref: https://application-notes.digchip.com/070/70-41484.pdf
"""

from math import sqrt, exp
from pprint import pprint


class mosfet():
    Rds_on = None
    Cgd1 = None
    Cgd2 = None
    Rg_on = None
    Rg_off = None
    Udr = None
    Uplateau = None
    tri = None
    tfi = None
    tru = None
    tfu = None
    Pc = None
    Psw = None
    Pl = None
    Qrr = None

    def tfu(this, ):
        def tfu1():
            return (this.converter.Udd - (this.Rds_on * this.converter.Id_on)) * this.Rg_on * this.Cgd1 / (this.Udr - this.Uplateau)

        def tfu2():
            return (this.converter.Udd - (this.Rds_on * this.converter.Id_on)) * this.Rg_on * this.Cgd2 / (this.Udr - this.Uplateau)
        
        return (tfu1() + tfu2() ) / 2


    def tru(this, ):
        def tru1():
            return (this.converter.Udd - (this.Rds_on * this.converter.Id_on)) * this.Rg_off * this.Cgd1 / (this.Uplateau)

        def tru2():
            return (this.converter.Udd - (this.Rds_on * this.converter.Id_on)) * this.Rg_off * this.Cgd2 / (this.Uplateau)
        
        return (tru1() + tru2() ) / 2


    def Pc(this, ) -> float:
        """ Pc = Rds_on * Id² """
        return this.Rds_on * this.converter.Id_rms**2


    def Eon_M(this, ) -> float:
        """ Eon_M = Udd * ((Id_on * (tri + tfu) / 2) + Qrr) """
        return this.converter.Udd * ((this.converter.Id_on * (this.tri + this.tfu) / 2) + this.Qrr)


    def Eoff_M(this, ) -> float:
        """ Eoff_M = Udd * Id_off * (tru + tfi) / 2 """
        return this.converter.Udd * this.converter.Id_off * (this.tru + this.tfi) / 2


    def Eon_D(this, ) -> float:
        """ Eon_D = Qrr * Udrr / 4, Udrr≃Udd """
        return this.Qrr * this.converter.Udd / 4


    def Psw(this, ) -> float:
        """
        Psw_M = (Eon_M + Eoff_M) * fsw  -> mosfet
        Psw_D = (Eon_D + Eoff_D) * fsw ≃ Eon_D * fsw  -> body diode
        Psw = Psw_M + Psw_D
        """
        Psw_M = (this.Eon_M() + this.Eoff_M()) * this.converter.fsw
        Psw_D = this.Eon_D() * this.converter.fsw

        return Psw_M + Psw_D


    def Pl(this, ) -> dict:
        """ Pl = Pc + Psw + Pb ≈ Pc + Psw """
        return this.Pc + this.Psw


    def as_dict(this) -> dict:
        return this.__dict__


    def print(this):
        pprint(this.as_dict())


    def __init__(this, Rds_on, Cgd1, Cgd2, Rg_on, Rg_off, Qrr, Udr, Uplateau, tri, tfi, converter):
        this.Rds_on = Rds_on

        this.Cgd1 = Cgd1
        this.Cgd2 = Cgd2
        
        this.Rg_on = Rg_on
        this.Rg_off = Rg_off

        this.Udr = Udr
        this.Qrr = Qrr
        this.Uplateau = Uplateau
        
        this.converter = converter

        this.tri = tri
        this.tfi = tfi
        this.tru = this.tru()

        this.tfu = this.tfu()

        this.Pc = this.Pc()
        this.Psw = this.Psw()
        this.Pl = this.Pl()


class chopper:
    Po = None  # output power
    Uo = None  # output voltage
    Udd = None  # input voltage
    L = None  # motor inductance
    R = None  # motor resistance
    E = None  # motor back-emf voltage
    fsw = None  # switching frequency

    D = None  # duty cycle
    Io = None
    Io_min = None
    Io_max = None
    dIo = None

    Id = None
    Id_on = None
    Id_off = None
    Id_rms = None
    If_av = None
    If_rms = None


    def io_min(this):
        e1 = (1 - exp( this.D / (this.fsw * this.L / this.R) ))
        e2 = (1 - exp( 1 / (this.fsw * this.L / this.R) ))

        this.Io_min = ((this.Udd / this.R) * (e1 / e2)) - (this.E / this.R)
        return this.Io_min


    def io_max(this):
        e1 = (1 - exp( - this.D / (this.fsw * this.L / this.R) ))
        e2 = (1 - exp( - 1 / (this.fsw * this.L / this.R) ))

        this.Io_max = ((this.Udd / this.R) * (e1 / e2)) - (this.E / this.R)
        return this.Io_max


    def as_dict(this) -> dict:
        return this.__dict__


    def print(this):
        pprint(this.as_dict())


    def __init__(this, Po, Uo, Udd, L, R, E, fsw):
        this.Po = Po
        this.Uo = Uo
        this.Udd = Udd
        this.L = L
        this.R = R
        this.E = E
        this.fsw = fsw

        this.D = Uo/Udd
        this.Io = Po/Uo
        this.Io_min = this.io_min()
        this.Io_max = this.io_max()
        this.dIo = this.Io_max - this.Io_min

        this.Id_on = this.Io - (this.dIo/2)
        this.Id_off = this.Io + (this.dIo/2)
        this.Id = this.Id_on
        this.Id_rms = sqrt(this.D) * this.Io
        this.If_av = (1 - this.D) * this.Io
        this.If_rms = sqrt(1 - this.D) * this.Io



if __name__ == '__main__':


    # Conversor no teste
    Vo = 9.6
    Io = 98.6
    Po = Vo * Io
    Pi = 1216
    Eff = Po/Pi
    Vi = 22.1
    fsw = 12.55e3

    # Motor no teste
    # Ea = kv * wa
    Ra = 35e-3
    La = 23e-6
    Ea = Vo - Io * Ra
    kv = 0.0107  # RPM / V
    wa = Ea / kv


    c = chopper(
        Po=Po,
        Uo=Vo,
        Udd=Vi,
        L=La,
        R=Ra,
        E=Ea,
        fsw=fsw,
    )

    ixfn420n10t = mosfet(
        Cgd1 = 0.55e-9,
        Cgd2 = 7.9e-9,
        Uplateau = 4.8,
        Rg_on = 10+1.4,
        Rg_off = 3.14+1.4,
        Udr = 15,
        tri = 350e-9,
        tfi = 300e-9,
        Qrr = 0.38e-6,
        Rds_on = 2.3e-3*1.2*1,
        converter = c
    )

    pprint(c.as_dict())
    print("==>ixfn420n10t<==")
    pprint(ixfn420n10t.as_dict())

    _Po = Pi-(2*ixfn420n10t.Pl)

    _Psw = 2 * Io * Vo * fsw * (291.9 + 595.8) * 1e-9 / 2
    print(f'_Psw = {_Psw}')
    print(f'Eff: {Po/Pi}, {_Po/Pi}, {_Po-Po}')
