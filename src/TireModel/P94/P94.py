from copy import deepcopy

from .aligning_moment import AligningMoment
from .pure_lateral import PureLateral
from .pure_longitudinal import PureLongitudinal
from ...Core.tirestate import TireState
from ..tiremodelbase import TireModelBase
from ..solvermode import SolverMode


class Pacejka94(TireModelBase, PureLateral, PureLongitudinal, AligningMoment):
    def __init__(self):
        PureLateral.__init__(self)
        PureLongitudinal.__init__(self)
        AligningMoment.__init__(self)
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
