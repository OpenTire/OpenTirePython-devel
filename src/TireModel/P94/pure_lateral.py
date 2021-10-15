from copy import deepcopy
from math import sin, atan, copysign


class PureLateral():
    def __init__(self):
        self.a0 = 1.4
        self.a1 = 0
        self.a2 = 1100
        self.a3 = 1100
        self.a4 = 10
        self.a5 = 0
        self.a6 = 0
        self.a7 = -2
        self.a8 = 0
        self.a9 = 0
        self.a10 = 1
        self.a11 = 0
        self.a12 = 0
        self.a13 = 0
        self.a14 = 0
        self.a15 = 0
        self.a16 = 0
        self.a17 = 0


    def __calculate_C(self):
        C = self.a0
        return C

    def __calculate_BCD(self, state):
        BCD = self.a3 * sin(atan((state.FZ) / self.a4) * 2) * (1 - self.a5 * abs(state.IA))
        return BCD

    def __calculate_D(self, state):
        D = state.FZ * (self.a1 * state.FZ + self.a2) * (1 - self.a15 * state.IA * state.IA)
        return D

    def __calculate_B(self, BCD, C, D):
        B = BCD / (C * D)
        return B

    def __calculate_H(self, state):
        H = self.a8 * state.FZ + self.a9 + self.a10 * state.IA
        return H

    def __calculate_E(self, state, H):
        E = (self.a6 * state.FZ + self.a7) * (1 - (self.a16 * state.IA + self.a17)) * copysign(1, state.SA + H)
        return E

    def __calculate_V(self, state):
        V = self.a11 * state.FZ + self.a12 + (self.a13 * state.FZ + self.a14) * state.IA * state.FZ
        return V

    def __calculate_Bx1(self, state, B, H):
        Bx1 = B * (state.SA + H)
        return Bx1


    def calculate_pure_fy(self, state):
        copy_state = deepcopy(state)
        copy_state.FZ = copy_state.FZ / 1000  # The formula requires that Fz is in kN
        copy_state.SA = copy_state.SA * 180/3.14 # The formula requires that SA is in deg
        C = self.__calculate_C()
        BCD = self.__calculate_BCD(copy_state)
        D = self.__calculate_D(copy_state)
        B = self.__calculate_B(BCD, C, D)
        H = self.__calculate_H(copy_state)
        E = self.__calculate_E(copy_state, H)
        V = self.__calculate_V(copy_state)
        Bx1 = self.__calculate_Bx1(copy_state, B, H)

        F = D * sin(C * atan(Bx1 - E * (Bx1 - atan(Bx1)))) + V

        return F
