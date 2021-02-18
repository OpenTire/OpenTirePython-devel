__author__ = 'henningo'

from .TireModel import *

def tire(model_name):
    if model_name == 'Harty':
        print('Harty not implemented')
        return None

    elif model_name == 'PAC2002':
        return PAC2002()

    else:
        return None  # Of we cam



