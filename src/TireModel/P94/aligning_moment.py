from copy import deepcopy
from math import sin, atan, copysign, exp


class AligningMoment():
    def __init__(self,
                 c0=1.5,
                 c1=1000,
                 c2=1100,
                 c3=2,
                 c4=3,
                 c5=0,
                 c6=0,
                 c7=0,
                 c8=0,
                 c9=0,
                 c10=0,
                 c11=0,
                 c12=0,
                 c13=0,
                 c14=0,
                 c15=0,
                 c16=0,
                 c17=0,
                 c18=0,
                 c19=0,
                 c20=0,
                 ):

        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c5 = c5
        self.c6 = c6
        self.c7 = c7
        self.c8 = c8
        self.c9 = c9
        self.c10 = c10
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c14 = c14
        self.c15 = c15
        self.c16 = c16
        self.c17 = c17
        self.c18 = c18
        self.c19 = c19
        self.c20 = c20


    def __calculate_C(self):
        return self.c0

    def __calculate_BCD(self, state):
        return (self.c3 * state.FZ * state.FZ + self.c4*state.FZ) * (1 - self.c6*abs(state.IA)) * exp(-self.c5 * state.FZ)

    def __calculate_D(self, state):
        return state.FZ * (self.c1 * state.FZ + self.c2) * (1 - self.c18 * state.IA * state.IA)

    def __calculate_B(self, BCD, C, D):
        return BCD / (C * D)

    def __calculate_H(self, state):
        return self.c11 * state.IA + self.c12 + self.c13 * state.IA

    def __calculate_E(self, state, H):
        return ((self.c7 * state.FZ * state.FZ + self.c8 * state.FZ + self.c9) * (1 - ((self.c19 * state.IA + self.c20) * copysign(1, state.SA + H)))) / (1 - self.c10 * abs(state.IA))


    def __calculate_V(self, state):
        return self.c14 * state.FZ + self.c15 + (self.c16 * state.FZ + self.c17) * state.IA * state.FZ

    def __calculate_Bx1(self, state, B, H):
        return B * (state.SA + H)


    def calculate_pure_mz(self, state):
        copy_state = deepcopy(state)
        copy_state.FZ = copy_state.FZ/1000
        copy_state.SA = copy_state.SA*3.14/180
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
