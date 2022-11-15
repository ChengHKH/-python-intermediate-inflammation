"""Tests for statistics functions within the Model layer."""

import numpy as np
import numpy.testing as npt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0], [0, 0], [0, 0]], [0, 0]),
        ([[1, 2], [3, 4], [5, 6]], [3, 4]),
    ]
)
def test_daily_mean(test, expected):
    """Test that mean function works for an array of zeros."""
    from inflammation.models import daily_mean

    # Need to use Numpy testing functions to compare arrays
    npt.assert_array_equal(daily_mean(test), expected)


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0, 0]),
        ([[4, 2, 5], [1, 6, 2], [4, 1, 9]], [4, 6, 9]),
        ([[4, -2, 5], [1, -6, 2], [-4, -1, 9]], [4, -1, 9]),
    ]
)
def test_daily_max(test, expected):
    """Test that max function works for an array of positive integers."""
    from inflammation.models import daily_max

    npt.assert_array_equal(daily_max(test), expected)


@pytest.mark.parametrize(
    "test, expected",
    [
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [0, 0, 0]),
        ([[4, 2, 5], [1, 6, 2], [4, 1, 9]], [1, 1, 2]),
        ([[4, -2, 5], [1, -6, 2], [-4, -1, 9]], [-4, -6, 2]),
    ]
)
def test_daily_min(test, expected):
    """Test that min function works for an array of positive and negative integers."""
    from inflammation.models import daily_min

    npt.assert_array_equal(daily_min(test), expected)


def test_daily_min_string():
    """Test for TypeError when we pass a string"""
    from inflammation.models import daily_min

    with pytest.raises(TypeError):
        error_expected = daily_min([['abd', 'ads'], ['asd', 'def']])


@pytest.mark.parametrize(
    "test, expected, expect_raises",
    [
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]], None),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 1, 1], [1, 1, 1], [1, 1, 1]], None),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], None),
        ([[-1, 2, 3], [4, 5, 6], [7, 8, 9]], [[0.33, 0.67, 1], [0.67, 0.83, 1], [0.78, 0.89, 1]], ValueError),
    ]
)
def test_patient_normalise(test, expected, expect_raises):
    """Test normalisation"""
    from inflammation.models import patient_normalise
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            npt.assert_almost_equal(patient_normalise(np.array(test)), np.array(expected), decimal=2)
    else:
        npt.assert_almost_equal(patient_normalise(np.array(test)), np.array(expected), decimal=2)


def test_sqlalchemy_patient_search():
    """Test that patient data can be saved to and retrieved from a database."""
    from inflammation.models import Base, Patient

    # Set up database connection
    # Database is stored in memory
    engine = create_engine('sqlite:///:memory:', echo = True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    test_patient = Patient(name='Alice')
    session.add(test_patient)

    queried_patient = session.query(Patient).filter_by(name='Alice').first()
    self.assertEqual(queried_patient.name, 'Alice')
    self.assertEqual(queried_patient.id, 1)

    Base.metadata.drop_all(engine)


def test_sqlalchemy_patient_observations():
    """Test that patient data can be saved to and retrieved from a database."""
    from inflammation.models import Base, Observation, Patient

    # Set up database connection
    # Database is stored in memory
    engine = create_engine('sqlite:///:memory:', echo = True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    test_patient = Patient(name='Alice')
    session.add(test_patient)

    test_observation = Observation(patient = test_patient, day = 0, value = 1)
    session.add(test_observation)

    queried_patient = session.query(Patient).filter_by(name='Alice').first()
    first_observation = queried_patient.observations[0]
    self.assertEqual(first_observation.patient, queried_patient)
    self.assertEqual(first_observation.day, 0)
    self.asserEqual(first_observation.value, 1)

    Base.metadata.drop_all(engine)