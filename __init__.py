from . import src
from .src.TireModel import PAC2002, Pacejka94
from .src.Core.tirestate import TireState

def tire(model_name):
    if model_name == 'Harty':
        print('Harty not implemented')
        return None

    elif model_name == 'PAC2002':
        return PAC2002()

    elif model_name == 'Pacejka94':
        return Pacejka94()

    else:
        return None  # Of we cam
