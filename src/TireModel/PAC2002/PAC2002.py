__author__ = 'henningo'

import pandas as pd

from ...Core import TireState
from ..tiremodelbase import TireModelBase
from ..solvermode import SolverMode
import math
import numpy as np


class PAC2002(TireModelBase):
    def __init__(self):
        self.Name = 'PAC2002'
        self.Description = 'An implementation of Pacejka 2002 as described in the First Editions of Tire' \
                           ' and Vehicle Dynamics'

        # General Coefficients
        self.FNOMIN = 4850
        self.UNLOADED_RADIUS = 0.344
        self.LONGVL = 16.6

        # General Scaling Factors
        self.LFZ0 = 1.0
        self.LCZ = 1.0

        # Pure Longitudinal Scaling Factors
        self.LCX = 1.0
        self.LMUX = 1.0
        self.LEX = 1.0
        self.LKX = 1.0
        self.LHX = 1.0
        self.LVX = 1.0
        self.LGAX = 1.0

        # Pure Lateral Scaling Factors
        self.LCY = 1.0
        self.LMUY = 1.0
        self.LEY = 1.0
        self.LKY = 1.0
        self.LHY = 1.0
        self.LVY = 1.0
        self.LGAY = 1.0

        # Pure Aligning Moment Scaling Factors
        self.LTR = 1.0
        self.LRES = 1.0
        self.LGAZ = 1.0

        # Combined Scaling Factors
        self.LXAL = 1.0
        self.LYKA = 1.0
        self.LVYKA = 1.0
        self.LS = 1.0

        # Overturning Scaling Factors
        self.LMX = 1.0
        self.LVMX = 1.0

        # Rolling Resistance Factors
        self.LMY = 1.0

        # Relaxation Scaling Factors
        self.LSGKP = 1.0
        self.LSGAL = 1.0

        # Pure Lateral Coefficients
        self.PCY1 = 1.3507  #a0
        self.PDY1 = 1.0489  #a1
        self.PDY2 = -0.18033    #a2
        self.PDY3 = -2.8821     #a3
        self.PEY1 = -0.0074722  #a4
        self.PEY2 = -0.0063208  #a5
        self.PEY3 = -9.9935     #a6
        self.PEY4 = -760.14     #a7
        self.PKY1 = -21.92      #a8
        self.PKY2 = 2.0012      #a9
        self.PKY3 = -0.024778   #a10
        self.PHY1 = 0.0026747   #a11
        self.PHY2 = 8.9094e-005 #a12
        self.PHY3 = 0.031415    #a13
        self.PVY1 = 0.037318    #a14
        self.PVY2 = -0.010049   #a15
        self.PVY3 = -0.32931    #a16
        self.PVY4 = -0.69553    #a17

        # Combined Lateral Coefficients
        self.RBY1 = 7.1433
        self.RBY2 = 9.1916
        self.RBY3 = -0.027856
        self.RCY1 = 1.0719
        self.REY1 = -0.27572
        self.REY2 = 0.32802
        self.RHY1 = 5.7448e-006
        self.RHY2 = -3.1368e-005
        self.RVY1 = -0.027825
        self.RVY2 = 0.053604
        self.RVY3 = -0.27568
        self.RVY4 = 12.12
        self.RVY5 = 1.9
        self.RVY6 = -10.704

        # Pure Aligning Torque Coefficients
        self.QBZ1 = 10.904
        self.QBZ2 = -1.8412
        self.QBZ3 = -0.52041
        self.QBZ4 = 0.039211
        self.QBZ5 = 0.41511
        self.QBZ9 = 8.9846
        self.QBZ10 = 0.0
        self.QCZ1 = 1.2136
        self.QDZ1 = 0.093509
        self.QDZ2 = -0.009218
        self.QDZ3 = -0.057061
        self.QDZ4 = 0.73954
        self.QDZ6 = -0.0067783
        self.QDZ7 = 0.0052254
        self.QDZ8 = -0.18175
        self.QDZ9 = 0.029952
        self.QEZ1 = -1.5697
        self.QEZ2 = 0.33394
        self.QEZ3 = 0.0
        self.QEZ4 = 0.26711
        self.QEZ5 = -3.594
        self.QHZ1 = 0.0047326
        self.QHZ2 = 0.0026687
        self.QHZ3 = 0.11998
        self.QHZ4 = 0.059083

        # Combined Aligning Coefficients
        self.SSZ1 = 0.033372
        self.SSZ2 = 0.0043624
        self.SSZ3 = 0.56742
        self.SSZ4 = -0.24116

        # Pure longitudinal coefficients
        self.PCX1 = 1.6411
        self.PDX1 = 1.1739
        self.PDX2 = -0.16395
        self.PDX3 = 5.0
        self.PEX1 = 0.46403
        self.PEX2 = 0.25022
        self.PEX3 = 0.067842
        self.PEX4 = -3.7604e-005
        self.PKX1 = 22.303
        self.PKX2 = 0.48896
        self.PKX3 = 0.21253
        self.PHX1 = 0.0012297  # TODO: Something funky with these params. Should be zero? To have no offset at SR=0
        self.PHX2 = 0.0004318
        self.PVX1 = -8.8098e-006
        self.PVX2 = 1.862e-005

        # Combined longitudinal coefficients
        self.RBX1 = 13.276
        self.RBX2 = -13.778
        self.RCX1 = 1.2568
        self.REX1 = 0.65225
        self.REX2 = -0.24948
        self.RHX1 = 0.0050722

        # Overturning Moment Coefficients
        self.QSX1 = 2.3155e-04
        self.QSX2 = 0.51574
        self.QSX3 = 0.046399

        # Rolling Resistance Coefficients
        self.QSY1 = 0.01
        self.QSY2 = 0.0
        self.QSY3 = 0.0
        self.QSY4 = 0.0

        # Loaded Radius
        self.QV1 = 7.15073791e-005
        self.QV2 = 0.14892
        self.QFCX = 0
        self.QFCY = 0
        self.QFCG = -3.0
        self.QFZ1 = 28.0249
        self.QFZ2 = 29.2

        # Rolling Radius
        self.BREFF = 8.4
        self.DREFF = 0.27
        self.FREFF = 0.07

        # Lateral Relaxation
        self.PTY1 = 2.1439
        self.PTY2 = 1.9829

        # Longitudinal Relaxation
        self.PTX1 = 2.3657
        self.PTX2 = 1.4112
        self.PTX3 = 0.56626

        # Turn-slip and parking calculated values.
        # Note that turn slip isn't implemented yet
        # Therefore all these reduction factors are set to 1
        # For future versions these needs to be calcualted for every time
        self.ZETA0 = 1
        self.ZETA1 = 1
        self.ZETA2 = 1
        self.ZETA3 = 1
        self.ZETA4 = 1
        self.ZETA5 = 1
        self.ZETA6 = 1
        self.ZETA7 = 1
        self.ZETA8 = 1

    # Region "Pure Fy"
    def __calculate_gamma_y(self, gamma_star):
        # 32
        gamma_y = gamma_star * self.LGAY  # Lambda Gamma Y

        return gamma_y

    def __calculate_B_y(self, C_y, D_y, K_y):
        # Note: This method could call C_y, D_y and K_y internally, but for clarity they are sent as arguments

        # 39
        # We need to avoid division by zero
        if C_y * D_y == 0.0:
            print('Division by zero detected in B_Y calculation')
            B_y = K_y / 0.000000001
        else:
            B_y = K_y / (C_y * D_y)  # This could cause a divide by zero issue

        return B_y

    def __calculate_C_y(self):

        # 33
        C_y = self.PCY1 * self.LCY

        return C_y

    def __calculate_D_y(self, state, dfz, gamma_y, zeta1):

        # 34
        mu_y = self.__calculate_mu_y(dfz, gamma_y)
        D_y = mu_y * state.FZ * zeta1

        return D_y

    def __calculate_E_y(self, dfz, gamma_y, alpha_y):


        # 36
        # TODO: Sign function difference between Python and equations?
        # Note: First virsion had math.copysign, but it acts as an abs(), causing issues. Switched this to np.sign()
        E_y = (self.PEY1 + self.PEY2 * dfz) * (1 - (self.PEY3 + self.PEY4 * gamma_y)*np.sign(alpha_y)) * self.LEY
        if E_y > 1.0:
            E_y = 1.0

        return E_y

    def __calculate_K_y(self, state, gamma_y, zeta3):

        # 37
        denom = (self.PKY2 * self.FNOMIN * self.LFZ0)
        if denom == 0.0:
            print('Division by zero detected in K_Y calculation')
            denom = 0.000000001

        K_y0 = self.PKY1 * self.FNOMIN * math.sin(2.0 * math.atan(state.FZ / denom)) * self.LFZ0 * self.LKY

        # 38
        K_y = K_y0 * (1-self.PKY3 * abs(gamma_y)) * zeta3

        return K_y

    def __calculate_mu_y(self, dfz, gamma_y):

        # 35
        mu_y = (self.PDY1 + self.PDY2 * dfz) * (1 - self.PDY3 * gamma_y * gamma_y) * self.LMUY  # Performance is better with gamma_y * gamma_y instead of gamma_y**2

        return mu_y

    def __calculate_S_Hy(self, dfz, gamma_y, zeta0, zeta4):

        # 40
        S_Hy = (self.PHY1 + self.PHY2 * dfz) * self.LHY + self.PHY3 * gamma_y * zeta0 + zeta4 - 1

        return S_Hy

    def __calculate_S_Vy(self, state, dfz, gamma_y, zeta4):

        # 41 - Moved parenthesis to sit "behind" gamma_y
        S_Vy = state.FZ * ((self.PVY1 + self.PVY2 * dfz) * self.LVY + (self.PVY3 + self.PVY4 * dfz) * gamma_y) * self.LMUY * zeta4

        return S_Vy

    #Region "Combined Fy"
    def __calculate_B_yk(self, alpha):

        # 70
        B_yk = self.RBY1 * math.cos(math.atan(self.RBY2 * (alpha - self.RBY3))) * self.LYKA

        return B_yk

    def __calculate_C_yk(self):

        # 71
        C_yk = self.RCY1

        return C_yk

    def __calculate_E_yk(self, dfz):

        # 73
        E_yk = self.REY1 + self.REY2 * dfz
        if E_yk > 1.0:
            E_yk = 1.0
        return E_yk

    def __calculate_S_Hyk(self, dfz):

        # 74
        S_Hyk = self.RHY1 + self.RHY2 * dfz

        return S_Hyk

    def __calculate_D_Vyk(self, state, dfz, gamma_y, alpha, gamma):

        #TODO: Should this be here, or should we pass mu_y instead? What's cleaner?
        mu_y = self.__calculate_mu_y(dfz, gamma_y)

        # 76
        D_Vyk = mu_y * state.FZ * (self.RVY1 + self.RVY2 * dfz + self.RVY3 * gamma) * math.cos(math.atan(self.RVY4 * alpha))

        return D_Vyk

    def __calculate_S_Vyk(self, kappa, D_Vyk):

        # 75
        S_Vyk = D_Vyk * math.sin(self.RVY5 * math.atan(self.RVY6 * kappa)) * self.LVYKA

        return S_Vyk

    # Region "Pure Fx"

    def __calculate_B_x(self, C_x, D_x, K_x):

        # 26
        if (C_x * D_x) == 0.0:
            B_x = 0.0

        else:
            B_x = K_x / (C_x * D_x)

        return B_x

    def __calculate_C_x(self):

        # 21
        C_x = self.PCX1 * self.LCX

        return C_x

    def __calculate_D_x(self, state, dfz, gamma_star, zeta1):

        mu_x = self.__calculate_mu_x(dfz, gamma_star)

        # 22
        D_x = mu_x * state.FZ * zeta1

        return D_x

    def __calculate_E_x(self, dfz, kappa_x):

        # 24
        E_x = (self.PEX1 + self.PEX2 * dfz + self.PEX3 * dfz * dfz) * (1.0 - self.PEX4 * np.sign(kappa_x)) * self.LEX
        if E_x > 1.0:
            E_x = 1.0

        return E_x

    def __calculate_K_x(self, state, dfz):

        # 25
        K_x = state.FZ * (self.PKX1 + self.PKX2 * dfz) * math.exp(self.PKX3 * dfz) * self.LKX
        # TODO: Check the "exp" function

        return K_x

    def __calculate_mu_x(self, dfz, gamma_star):

        # 20
        gamma_x = gamma_star * self.LGAX

        # 23
        mu_x = (self.PDX1 + self.PDX2 * dfz) * (1.0 - self.PDX3 * gamma_x ** 2.0) * self.LMUX # Note that it is using gamma_x here

        return mu_x

    def __calculate_S_Hx(self, dfz):

        # 27
        S_Hx = (self.PHX1 + self.PHX2 * dfz) * self.LHX

        return S_Hx

    def __calculate_S_Vx(self, state, dfz, zeta1):

        # 28
        S_Vx = state.FZ * (self.PVX1 + self.PVX2 * dfz) * self.LVX * self.LMUX * zeta1

        return S_Vx

    #Region "Combined Fx"
    def __calculate_S_Hxa(self):

        # 65
        S_Hxa = self.RHX1

        return S_Hxa

    def __calculate_B_xa(self, kappa):

        # 61
        B_xa = self.RBX1 * math.cos(math.atan(self.RBX2 * kappa)) * self.LXAL

        return B_xa

    def __calculate_C_xa(self):

        # 62
        C_xa = self.RCX1

        return C_xa

    def __calculate_E_xa(self, dfz):

        # 64
        E_xa = self.REX1 + self.REX2 * dfz
        if E_xa > 1.0:
            E_xa = 1.0

        return E_xa



    #Region "Pure Mz"

    def __calculate_gamma_z(self, gamma_star):

        # 49
        gamma_z = gamma_star * self.LGAZ

        return gamma_z

    #Trail Calcs

    def __calculate_B_t(self, dfz, gamma_z):

        # 50
        B_t = (self.QBZ1 + self.QBZ2 * dfz + self.QBZ3 * dfz ** 2) * (1 + self.QBZ4 * gamma_z + self.QBZ5 * abs(gamma_z)) * self.LKY / self.LMUY

        return B_t

    def __calculate_C_t(self):

        # 51
        C_t = self.QCZ1

        return C_t

    def __calculate_D_t(self, state, dfz, gamma_z, zeta5):

        # 52
        D_t = state.FZ * (self.QDZ1 + self.QDZ2 * dfz) * (1 + self.QDZ3 * gamma_z + self.QDZ4 * gamma_z ** 2) * self.UNLOADED_RADIUS / self.FNOMIN * self.LTR * zeta5

        return D_t

    def __calculate_E_t(self, dfz, gamma_z, alpha_t, B_t, C_t):

        # 53
        E_t = (self.QEZ1 + self.QEZ2 * dfz + self.QEZ3 * dfz ** 2) * (1 + (self.QEZ4 + self.QEZ5 * gamma_z) * ((2/math.pi) * math.atan(B_t * C_t * alpha_t)))
        if E_t > 1.0:
            E_t = 1.0

        return E_t

    def __calculate_S_Ht(self, dfz, gamma_z):

        # 54
        S_Ht = self.QHZ1 + self.QHZ2 * dfz + (self.QHZ3 + self.QHZ4 * dfz) * gamma_z

        return S_Ht

    def __calculate_t(self, B_t, C_t, D_t, E_t, alpha_t, alpha_star):

         # 44 - Trail
        t = D_t * math.cos(C_t * math.atan(B_t * alpha_t - E_t * (B_t * alpha_t - math.atan(B_t * alpha_t)))) * math.cos(alpha_star)

        return t

    #Residual Moment Calcs

    def __calculate_B_r(self, B_y, C_y, zeta6):

        # 55
        B_r = (self.QBZ9 * self.LKY / self.LMUY + self.QBZ10 * B_y * C_y) * zeta6

        return B_r

    def __calculate_C_r(self, zeta7):

        # after 55
        C_r = zeta7

        return C_r

    def __calculate_D_r(self, state, dfz, gamma_z, zeta8):

        # 56
        D_r = state.FZ * ((self.QDZ6 + self.QDZ7 * dfz) * self.LRES + (self.QDZ8 + self.QDZ9 * dfz) * gamma_z) * self.UNLOADED_RADIUS * self.LMUY + zeta8 - 1.0

        return D_r

    def __calculate_S_Hf(self, S_Hy, S_Vy, K_y):

        # 48
        S_Hf = S_Hy + S_Vy / K_y

        return S_Hf

    def __calculate_M_zr(self, B_r, C_r, D_r, alpha_r, alpha_star ):

        # 46 - Residual Moment
        M_zr = D_r * math.cos(C_r * math.atan(B_r * alpha_r)) * math.cos(alpha_star)

        return M_zr



    def save(self, fname, data):
        return 'saving'

    def load(self, fname):
        return 'loading'

    def solve(self, input_state, mode=SolverMode.All):
        state = TireState()
        states = TireState(FX=[], FY=[], FZ=[], MX=[], MY=[], MZ=[], SA=[], SR=[], IA=[], V=[], P=[])
        state_table = TireState(FX=[], FY=[], FZ=[], MX=[], MY=[], MZ=[], SA=[], SR=[], IA=[], V=[], P=[])

        for load in input_state.FZ:
            for camber in input_state.IA:
                for speed in input_state.V:
                    for pressure in input_state.P:
                        for slip_ratio in input_state.SR:
                            for slip_angle in input_state.SA:
                                state_table.FZ.append(load)
                                state_table.SA.append(slip_angle)
                                state_table.IA.append(camber)
                                state_table.SR.append(slip_ratio)
                                state_table.V.append(speed)
                                state_table.P.append(pressure)

        for fz, ia, sr, sa, v, p in zip(state_table.FZ, state_table.IA, state_table.SR, state_table.SA, state_table.V, state_table.P):
            state.FZ = fz
            state.IA = ia
            state.SR = sr
            state.SA = sa
            state.V = v
            state.P = p

            if (mode is SolverMode.PureFy) or (mode is SolverMode.PureMz):
                state.FY = self.calculate_pure_fy(state)

            if mode is SolverMode.Fy or mode is SolverMode.All:
                state.FY = self.calculate_fy(state)

            if mode is SolverMode.PureFx:
                state.FX = self.calculate_pure_fx(state)

            if mode is SolverMode.Fx or mode is SolverMode.All:
                state.FX = self.calculate_fx(state)

            if mode is SolverMode.PureMz:
                state.MZ = self.calculate_pure_mz(state)

            if mode is SolverMode.Mz or mode is SolverMode.All:
                state.MZ = self.calculate_mz(state)

            if mode is SolverMode.Mx or mode is SolverMode.All:
                state.MX = self.calculate_mx(state)

            if mode is SolverMode.Mz or mode is SolverMode.All:
                state.MY = self.calculate_my(state)

            if mode is SolverMode.Radius or mode is SolverMode.All:
                state.RL, state.RE = self.calculate_radius(state)

            if mode is SolverMode.Relaxation or mode is SolverMode.All:
                state.SIGMA_ALPHA = self.calculate_lateral_relaxation_length(state)
                state.SIGMA_KAPPA = self.calculate_longitudinal_relaxation_length(state)

            states.FX.append(state.FX)
            states.FY.append(state.FY)
            states.FZ.append(state.FZ)
            states.MX.append(state.MX)
            states.MY.append(state.MY)
            states.MZ.append(state.MZ)
            states.SA.append(state.SA)
            states.SR.append(state.SR)
            states.IA.append(state.IA)
            states.V.append(state.V)
            states.P.append(state.P)


        states = pd.DataFrame({'FX': states.FX,
                               'FY': states.FY,
                               'FZ': states.FZ,
                               'MX': states.MX,
                               'MY': states.MY,
                               'MZ': states.MZ,
                               'SA': states.SA,
                               'SR': states.SR,
                               'IA': states.IA,
                               'V': states.V,
                               'P': states.P,
        })
        return states

    def get_parameters(self):
        return 0

    def set_parameters(self, params):
        #TODO: Must check that params keys actually match the models coefs.
        pass

        return True  # should return False if the parameter structure doesn't match required one

    def get_model_info(self):
        return [self.Name, self.Description]

    ###Private properties

    def calculate_common_values(self, state):
        # First we calculate some standard values used in multiple locations
        dfz = (state.FZ - self.FNOMIN / self.FNOMIN)
        alpha_star = math.tan(state.SA) * np.sign(state.V)
        gamma_star = math.sin(state.IA)
        kappa = state.SR

        return dfz, alpha_star, gamma_star, kappa

    def calculate_fx(self, state):

        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)


        F_x0 = self.calculate_pure_fx(state)

        S_Hxa = self.__calculate_S_Hxa()

        #60
        alpha_s = alpha_star + S_Hxa

        B_xa = self.__calculate_B_xa(kappa)
        C_xa = self.__calculate_C_xa()
        E_xa = self.__calculate_E_xa(dfz)

        # 66
        G_xa_numerator = math.cos(C_xa * math.atan(B_xa * alpha_s - E_xa * (B_xa * alpha_s - math.atan(B_xa * alpha_s))))
        G_xa_denominator = math.cos(C_xa * math.atan(B_xa * S_Hxa - E_xa * (B_xa * S_Hxa - math.atan(B_xa * S_Hxa))))
        G_xa = G_xa_numerator / G_xa_denominator

        return F_x0 * G_xa

    def calculate_pure_fx(self, state):
        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        C_x = self.__calculate_C_x()
        D_x = self.__calculate_D_x(state, dfz, gamma_star, self.ZETA1)
        S_Hx = self.__calculate_S_Hx(dfz)

        # 19
        kappa_x = kappa + S_Hx

        E_x = self.__calculate_E_x(dfz, kappa_x)
        K_x = self.__calculate_K_x(state, dfz)
        B_x = self.__calculate_B_x(C_x, D_x, K_x)
        S_Vx = self.__calculate_S_Vx(state, dfz, self.ZETA1)

        # 18
        fx_pure = D_x * math.sin((C_x * math.atan(B_x * kappa_x - E_x * (B_x * kappa_x - math.atan(B_x * kappa_x))))) + S_Vx

        return fx_pure

    def calculate_fy(self, state):
        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        F_y0 = self.calculate_pure_fy(state)

        gamma_y = self.__calculate_gamma_y(gamma_star)
        B_yk = self.__calculate_B_yk(alpha_star)
        C_yk = self.__calculate_C_yk()
        E_yk = self.__calculate_E_yk(dfz)

        D_Vyk = self.__calculate_D_Vyk(state, dfz, gamma_y, alpha_star, gamma_star)
        S_Vyk = self.__calculate_S_Vyk(kappa, D_Vyk)

        # 69
        S_Hyk = self.__calculate_S_Hyk(dfz)
        kappa_s = kappa + S_Hyk

        # 77
        G_yk_numerator = math.cos(C_yk * math.atan(B_yk * kappa_s - E_yk * (B_yk * kappa_s - math.atan(B_yk * kappa_s))))
        G_yk_denominator = math.cos(C_yk * math.atan(B_yk * S_Hyk - E_yk * (B_yk * S_Hyk - math.atan(B_yk * S_Hyk))))
        G_yk = G_yk_numerator/G_yk_denominator

        return G_yk * F_y0 + S_Vyk

    def calculate_pure_fy(self, state):
        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        gamma_y = self.__calculate_gamma_y(gamma_star)

        C_y = self.__calculate_C_y()
        D_y = self.__calculate_D_y(state, dfz, gamma_y, self.ZETA1)
        S_Hy = self.__calculate_S_Hy(dfz, gamma_y, self.ZETA0, self.ZETA4)

        # 31
        alpha_y = alpha_star + S_Hy

        E_y = self.__calculate_E_y(dfz, gamma_y, alpha_y)
        K_y = self.__calculate_K_y(state, gamma_y, self.ZETA3)
        B_y = self.__calculate_B_y(C_y, D_y, K_y)
        S_Vy = self.__calculate_S_Vy(state, dfz, gamma_y, self.ZETA4)

        # 30
        fy_pure = D_y * math.sin(C_y * math.atan(B_y * alpha_y - E_y * (B_y * alpha_y - math.atan(B_y * alpha_y)))) + S_Vy

        return fy_pure

    def calculate_mz(self, state):
        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        # 32
        gamma_y = self.__calculate_gamma_y(gamma_star)
        gamma_z = self.__calculate_gamma_z(gamma_star)

        # Combined Trail Calcs
        S_Ht = self.__calculate_S_Ht(dfz, gamma_z)

        # 47
        alpha_t = alpha_star + S_Ht
        K_x = self.__calculate_K_x(state, dfz)
        K_y = self.__calculate_K_y(state, gamma_y, self.ZETA3)

        # 84
        alpha_teq = math.atan(math.sqrt(math.tan(alpha_t)**2 + (K_x/K_y)**2 * kappa**2) * np.sign(alpha_t))
        B_t = self.__calculate_B_t(dfz, gamma_z)
        C_t = self.__calculate_C_t()
        D_t = self.__calculate_D_t(state, dfz, gamma_z, self.ZETA5)
        E_t = self.__calculate_E_t(dfz, gamma_z, alpha_t, B_t, C_t)

        # Combined Trail Calc, here we are using alpha_teq instead of alpha_t
        t = self.__calculate_t(B_t, C_t, D_t, E_t, alpha_teq, alpha_star)

        # Combined Residual Torque Calcs
        S_Hy = self.__calculate_S_Hy(dfz, gamma_y, self.ZETA0, self.ZETA4)
        S_Vy = self.__calculate_S_Vy(state, dfz, gamma_y, self.ZETA4)
        K_y = self.__calculate_K_y(state, gamma_y, self.ZETA3)
        S_Hf = self.__calculate_S_Hf(S_Hy, S_Vy, K_y)

        # 47
        alpha_r = alpha_star + S_Hf

        # 85
        alpha_req = math.atan(math.sqrt(math.tan(alpha_r)**2 + (K_x/K_y)**2 * kappa**2) * np.sign(alpha_r))

        C_y = self.__calculate_C_y()
        D_y = self.__calculate_D_y(state, dfz, gamma_y, self.ZETA1)
        B_y = self.__calculate_B_y(C_y, D_y, K_y)
        B_r = self.__calculate_B_r(B_y, C_y, self.ZETA6)
        C_r = self.__calculate_C_r(self.ZETA7)
        D_r = self.__calculate_D_r(state, dfz, gamma_z, self.ZETA8)

        M_zr = self.__calculate_M_zr(B_r, C_r, D_r, alpha_req, alpha_star)

        # FY Prime Calcs
        D_Vyk = self.__calculate_D_Vyk(state, dfz, gamma_y, alpha_star, gamma_star)
        S_Vyk = self.__calculate_S_Vyk(kappa, D_Vyk)

        Fy_prime = state.FY - S_Vyk  # This is the combined lateral force without Fx induced Fy

        # Pneumatic scrub (s) calcs
        s = self.UNLOADED_RADIUS * (self.SSZ1 + self.SSZ2 * (state.FY / (self.FNOMIN * self.LFZ0)) + (self.SSZ3 + self.SSZ4 * dfz) * gamma_star) * self.LS

        M_prime = -t * Fy_prime + M_zr + s * state.FX

        return M_prime

    def calculate_pure_mz(self, state):
        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        gamma_z = self.__calculate_gamma_z(gamma_star)
        gamma_y = self.__calculate_gamma_y(gamma_star)

        # Trail calculations (D_t, C_t, B_t, E_t)
        S_Ht = self.__calculate_S_Ht(dfz, gamma_z)

        # 47
        alpha_t = alpha_star + S_Ht

        B_t = self.__calculate_B_t(dfz, gamma_z)
        C_t = self.__calculate_C_t()
        D_t = self.__calculate_D_t(state, dfz, gamma_z, self.ZETA5)
        E_t = self.__calculate_E_t(dfz, gamma_z, alpha_t, B_t, C_t)

        # Trail Calculation
        t = self.__calculate_t(B_t, C_t, D_t, E_t, alpha_t, alpha_star)

        # Residual Moment Calculations (C_r, D_r, B_r)
        # These calcs uses Pure Fy calculations, so they are repeated here (such as K_y and D_y)
        S_Hy = self.__calculate_S_Hy(dfz, gamma_y, self.ZETA0, self.ZETA4)
        S_Vy = self.__calculate_S_Vy(state, dfz, gamma_y, self.ZETA4)
        K_y = self.__calculate_K_y(state, gamma_y, self.ZETA3)
        C_y = self.__calculate_C_y()
        D_y = self.__calculate_D_y(state, dfz, gamma_y, self.ZETA1)
        B_y = self.__calculate_B_y(C_y, D_y, K_y)

        B_r = self.__calculate_B_r(B_y, C_y, self.ZETA6)
        C_r = self.__calculate_C_r(self.ZETA7)
        D_r = self.__calculate_D_r(state, dfz, gamma_z, self.ZETA8)
        S_Hf = self.__calculate_S_Hf(S_Hy, S_Vy, K_y)

        # 47
        alpha_r = alpha_star + S_Hf

        # Residual Moment Calculation
        M_zr = self.__calculate_M_zr(B_r, C_r, D_r, alpha_r, alpha_star)

        fy_pure = state.FY  # This requires that FY have been calculated already

        mz_pure = -t * fy_pure + M_zr

        return mz_pure

    def calculate_mx(self, state):

        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        # 86
        M_x = self.UNLOADED_RADIUS * state.FZ * (self.QSX1 * self.LVMX - self.QSX2 * gamma_star + self.QSX3 * state.FY / self.FNOMIN) * self.LMX

        return M_x

    def calculate_my(self, state):

        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        # 87
        M_y = self.UNLOADED_RADIUS * state.FZ * (self.QSY1 + self.QSY2 * state.FX/self.FNOMIN + self.QSY3 * abs(state.V / self.LONGVL) + self.QSY4 * (state.V / self.LONGVL)**4) * self.LMY

        return M_y

    def calculate_radius(self, state):

        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        # If we don't have omega, we use an approximation
        omega = state.V / (self.UNLOADED_RADIUS * 0.98)

        # First we solve for dynamic displacement
        # External Effects
        speed_effect = self.QV2 * abs(omega) * self.UNLOADED_RADIUS / self.LONGVL
        fx_effect = (self.QFCX * state.FX / self.FNOMIN)**2
        fy_effect = (self.QFCY * state.FY / self.FNOMIN)**2
        camber_effect = self.QFCG * gamma_star**2
        external_effects = 1.0 + speed_effect - fx_effect - fy_effect + camber_effect

        # Fz/(external_effects * Fz0) = a*x2 + b*x
        # 0 = a*x2 + b*x + c

        a = (self.QFZ2 / self.UNLOADED_RADIUS)**2
        b = self.QFZ1 / self.UNLOADED_RADIUS
        c = -(state.FZ / (external_effects * self.FNOMIN))

        if b**2 - 4*a*c > 0:
            rho = (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a)
        else:
            rho = 999999

        # Then we calculate free-spinning radius
        R_omega = self.UNLOADED_RADIUS + self.QV1 * self.UNLOADED_RADIUS * (omega * self.UNLOADED_RADIUS / self.LONGVL)**2

        # The loaded radius is the free-spinning radius minus the deflection
        R_l = R_omega - rho

        # Effective Rolling Radius

        # Nominal stiffness
        C_z0 = self.FNOMIN / self.UNLOADED_RADIUS * math.sqrt(self.QFZ1**2 + 4.0 * self.QFZ2)
        if C_z0 == 0.0:
            return 0.0, 0.0

        # Eff. Roll. Radius #This is a newer version
        R_e_old = R_omega - (self.FNOMIN / C_z0) * (self.DREFF * math.atan(self.BREFF * state.FZ / self.FNOMIN) + self.FREFF * state.FZ / self.FNOMIN)


        # Eff. Roll. Radius Pac 2002
        C_z = self.QFZ1 * self.FNOMIN / self.UNLOADED_RADIUS
        rho_Fz0 = self.FNOMIN / (C_z0 * self.LCZ)
        rho_d = rho/rho_Fz0

        R_e = R_omega - rho_Fz0 * (self.DREFF * math.atan(self.BREFF * rho_d) + self.FREFF * rho_d)

        return R_l, R_e

    def calculate_lateral_relaxation_length(self, state):


        

        if self.PTY2 == 0:
            return 0

        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)
        gamma_y = self.__calculate_gamma_y(gamma_star)

        # 93
        sigma_alpha = self.PTY1 * math.sin(2.0 * math.atan(state.FZ / (self.PTY2 * self.FNOMIN * self.LFZ0))) * (1 - self.PKY3 * abs(gamma_y)) * self.UNLOADED_RADIUS * self.LFZ0 * self.LSGAL

        return sigma_alpha

    def calculate_longitudinal_relaxation_length(self, state):

        
        dfz, alpha_star, gamma_star, kappa = self.calculate_common_values(state)

        # 92
        sigma_kappa = state.FZ * (self.PTX1 + self.PTX2 * dfz) * math.exp(-self.PTX3 * dfz) * (self.UNLOADED_RADIUS / self.FNOMIN) * self.LSGKP

        return sigma_kappa
