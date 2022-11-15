"""Module containing models representing patients and their data.

The Model layer is responsible for the 'business logic' part of the software.

Patients' data is held in an inflammation table (2D array) where each row contains
inflammation data for a single patient taken over a number of days
and each column represents a single day across all patients.
"""

import numpy as np
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Observation(Base):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key = True)
    day = Column(Integer)
    value = Column(Integer)
    patient_id = Column(Integer, ForeignKey('patients.id'))

    patient = relationship('Patient', back_populates = 'observations')


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key = True)
    name = Column(String)

    observations = relationship('Observation', order_by = Observation.day, back_populates = 'patient')

    @property
    def values(self):
        last_day = self.observations[-1].day
        values = np.zeros(last_day + 1)

        for observation in self.observations:
            values[observation.day] = observation.value

        return values

# class Observation:
#     def __init__(self, day, value):
#         self.day = day
#         self.value = value

#     def __str__(self):
#         return str(self.value)


class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# class Patient(Person):
#     __tablename__ = 'patients'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         self.observations = []
#         if 'observations' in kwargs:
#             self.observations = kwargs['observations']

#     @property
#     def last_observation(self):
#         return self.observations[-1]
    
#     def add_observation(self, value, day=None):
#         if day is None:
#             try:
#                 day = self.observations[-1].day + 1
#             except IndexError:
#                 day = 0

#         new_observation = Observation(day, value)
#         self.observations.append(new_observation)
#         return new_observation


class Doctor(Person):
    def __init__(self, name):
        super().__init__(name)
        self.patients = []

    def add_patient(self, new_patient):
        for patient in self.patients:
            if patient.name == new_patient.name:
                return

        self.patients.append(new_patient)


def load_csv(filename):
    """Load a Numpy array from a CSV

    :param filename: Filename of CSV to load
    """
    return np.loadtxt(fname=filename, delimiter=',')


def daily_mean(data):
    """Calculate the daily mean of a 2D inflammation data array.

    :param data:
    :returns: mean
    """
    return np.mean(data, axis=0)


def daily_max(data):
    """Calculate the daily max of a 2D inflammation data array.

    :param data:
    :returns: max
    """
    return np.max(data, axis=0)


def daily_min(data):
    """Calculate the daily min of a 2D inflammation data array.

    :param data:
    :returns: min
    """
    return np.min(data, axis=0)


def patient_normalise(data):
    """Normalise patient data from 2D array of inflammation data"""
    if np.any(data < 0):
        raise ValueError('Inflammation values should not be negative')
    maxes = np.nanmax(data, axis=1)
    with np.errstate(invalid='ignore', divide='ignore'):
        normalised = data /maxes[:, np.newaxis]
    normalised[np.isnan(normalised)] = 0
    normalised[normalised < 0] = 0
    return normalised


def daily_std_dev(data):
    """Calculate the daily standard deviation of a 2D inflammation data array.
    
    :param data:
    :returns: std
    """
    return np.std(data, axis=0)