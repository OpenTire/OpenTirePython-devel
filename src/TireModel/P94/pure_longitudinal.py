from copy import deepcopy
from math import sin, atan, copysign, exp


class PureLongitudinal():
    def __init__(self):
        self.b0 = 1.4
        self.b1 = 0
        self.b2 = 1100
        self.b3 = 1100
        self.b4 = 10
        self.b5 = 0
        self.b6 = 0
        self.b7 = -2
        self.b8 = 0
        self.b9 = 0
        self.b10 = 1
        self.b11 = 0
        self.b12 = 0
        self.b13 = 0


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
        copy_state.FZ = copy_state.FZ / 1000  # The formula requires that Fz is in kN
        copy_state.SR = copy_state.SR * 100 # The formula requires that SR in percentage
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
