from copy import deepcopy
from math import sin, atan, copysign, exp


class PureLongitudinal():
    def __init__(self,
                 b0=1.5,
                 b1=0,
                 b2=1100,
                 b3=0,
                 b4=300,
                 b5=0,
                 b6=0,
                 b7=0,
                 b8=-2,
                 b9=0,
                 b10=0,
                 b11=0,
                 b12=0,
                 b13=0):

        self.b0 = b0
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        self.b4 = b4
        self.b5 = b5
        self.b6 = b6
        self.b7 = b7
        self.b8 = b8
        self.b9 = b9
        self.b10 = b10
        self.b11 = b11
        self.b12 = b12
        self.b13 = b13


    def __calculate_C(self):
        return self.b0

    def __calculate_BCD(self, state):
        return (self.b3 * state.FZ * state.FZ + self.b4*state.FZ) * exp(-self.b5 * state.FZ)

    def __calculate_D(self, state):
        return state.FZ * (self.b1 * state.FZ + self.b2)

    def __calculate_B(self, BCD, C, D):
        B = BCD / (C * D)
        return B

    def __calculate_H(self, state):
        return self.b9 * state.FZ + self.b10

    def __calculate_E(self, state, H):
        return (self.b6 * state.FZ * state.FZ + self.b7 * state.FZ + self.b8) * (1 - self.b13 * copysign(1, state.SR + H))

    def __calculate_V(self, state):
        return self.b11 * state.FZ + self.b12

    def __calculate_Bx1(self, state, B, H):
        return B * (state.SR + H)


    def calculate_pure_fx(self, state):
        copy_state = deepcopy(state)
        copy_state.FZ = copy_state.FZ/1000
        copy_state.SR = copy_state.SR*100

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
