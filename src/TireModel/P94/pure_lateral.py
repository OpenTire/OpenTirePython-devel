from copy import deepcopy
from math import sin, atan, copysign


class PureLateral():
    def __init__(self,
                 a0=1,
                 a1=0,
                 a2=0,
                 a3=1,
                 a4=1,
                 a5=0,
                 a6=0,
                 a7=0,
                 a8=0,
                 a9=0,
                 a10=0,
                 a11=0,
                 a12=0,
                 a13=0,
                 a14=0,
                 a15=0,
                 a16=0,
                 a17=0):

        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.a5 = a5
        self.a6 = a6
        self.a7 = a7
        self.a8 = a8
        self.a9 = a9
        self.a10 = a10
        self.a11 = a11
        self.a12 = a12
        self.a13 = a13
        self.a14 = a14
        self.a15 = a15
        self.a16 = a16
        self.a17 = a17


    def __calculate_C(self):
        return self.a0

    def __calculate_BCD(self, state):
        BCD = self.a3 * sin(atan((state.FZ) / self.a4) * 2) * (1 - self.a5 * abs(state.IA))
        return BCD

    def __calculate_D(self, state):
        return state.FZ * (self.a1 * state.FZ + self.a2) * (1 - self.a15 * state.IA * state.IA)

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
        copy_state.FZ = copy_state.FZ
        copy_state.SR = copy_state.SR*100
        copy_state.SA = copy_state.SA
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
