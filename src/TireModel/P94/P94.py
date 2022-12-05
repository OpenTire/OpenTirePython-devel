from copy import deepcopy

from .aligning_moment import AligningMoment
from .pure_lateral import PureLateral
from .pure_longitudinal import PureLongitudinal
from ...Core.tirestate import TireState
from ..tiremodelbase import TireModelBase
from ..solvermode import SolverMode


class Pacejka94(TireModelBase, PureLateral, PureLongitudinal, AligningMoment):
    def __init__(self,
                 a0=30.4,
                 a1=0,
                 a2=1,
                 a3=10000,
                 a4=1000,
                 a5=0,
                 a6=0,
                 a7=-2,
                 a8=0,
                 a9=0,
                 a10=0,
                 a11=0,
                 a12=0,
                 a13=0,
                 a14=0,
                 a15=0,
                 a16=0,
                 a17=0,
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
                 b13=0,
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
                 c20=0
                 ):
        PureLateral.__init__(self,
                             a0=a0,
                 a1=a1,
                 a2=a2,
                 a3=a3,
                 a4=a4,
                 a5=a5,
                 a6=a6,
                 a7=a7,
                 a8=a8,
                 a9=a9,
                 a10=a10,
                 a11=a11,
                 a12=a12,
                 a13=a13,
                 a14=a14,
                 a15=a15,
                 a16=a16,
                 a17=a17)
        PureLongitudinal.__init__(self,
                                  b0=b0,
                                  b1=b1,
                                  b2=b2,
                                  b3=b3,
                                  b4=b4,
                                  b5=b5,
                                  b6=b6,
                                  b7=b7,
                                  b8=b8,
                                  b9=b9,
                                  b10=b10,
                                  b11=b11,
                                  b12=b12,
                                  b13=b13,
                                  )
        AligningMoment.__init__(self,
                                c0=c0,
                                c1=c1,
                                c2=c2,
                                c3=c3,
                                c4=c4,
                                c5=c5,
                                c6=c6,
                                c7=c7,
                                c8=c8,
                                c9=c9,
                                c10=c10,
                                c11=c11,
                                c12=c12,
                                c13=c13,
                                c14=c14,
                                c15=c15,
                                c16=c16,
                                c17=c17,
                                c18=c18,
                                c19=c19,
                                c20=c20
                                )
        self.Name = 'Pacejka94'
        self.Description = 'An implementation of Pacejka 94'

    def get_model_info(self):
        pass

    def get_parameters(self):
        pass

    def load(self, fname):
        pass

    def save(self, fname, data):
        pass

    def set_parameters(self, params):
        pass

    def solve(self, input_state, mode=SolverMode.All):
        state = TireState()
        states = TireState(FX=[], FY=[], FZ=[], MX=[], MY=[], MZ=[], SA=[], SR=[], IA=[], V=[], P=[])
        state_table = TireState(FX=[], FY=[], FZ=[], MX=[], MY=[], MZ=[], SA=[], SR=[], IA=[], V=[], P=[])
        state_table.FZ = input_state.FZ * len(input_state.SA) * len(input_state.SR)
        state_table.IA = input_state.IA * len(input_state.SA) * len(input_state.SR)
        state_table.SA = input_state.SA * len(input_state.SR)
        state_table.SR = len(input_state.SA) * input_state.SR


        for fz, ia, sr, sa in zip(state_table.FZ, state_table.IA, state_table.SR, state_table.SA):
            state.FZ = fz
            state.IA = ia
            state.SR = sr
            state.SA = sa

            if mode is SolverMode.PureFy or mode is SolverMode.All:
                state.FY = self.calculate_pure_fy(state)

            if mode is SolverMode.PureFx or mode is SolverMode.All:
                state.FX = self.calculate_pure_fx(state)

            if mode is SolverMode.PureMz or mode is SolverMode.All:
                state.MZ = self.calculate_pure_mz(state)

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

        return states
