__author__ = 'henningo'
import abc

class TireModelBase(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_model_info(self):
        """Return information about the model"""
        return

    @abc.abstractmethod
    def load(self, fname):
        """Retrieve data from the input source and return an object."""
        return

    @abc.abstractmethod
    def save(self, fname, data):
        """Save the data object to the output."""
        return

    @abc.abstractmethod
    def solve(self, state, mode=0):
        """Calculate steady state force"""
        return

    @abc.abstractmethod
    def get_parameters(self):
        """Return the parameters dictionary"""
        return

    @abc.abstractmethod
    def set_parameters(self, params):
        """Set the parameters"""
