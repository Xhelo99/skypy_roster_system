# test_validator_pytest.py
import pytest
import sys
import os


from src.flight import Flight
from src.crew import Crew
from src.roster import Roster
from src.validator import validate_roster


@pytest.fixture
def test_setup():
    """Setup common test data."""
    # Create crew
    crew1 = Crew("C001", "JFK", "B747;A320")
    crew2 = Crew("C002", "LHR", "B747")

    crew_dict = {"C001": crew1, "C002": crew2}

    # Create test flights
    flight1 = Flight("FL001", "JFK", "LHR",
                     "2024-02-01T08:00:00Z", "2024-02-01T20:00:00Z", "B747")

    flight2 = Flight("FL002", "LHR", "CDG",
                     "2024-02-01T21:30:00Z", "2024-02-01T23:00:00Z", "B747")  # 90 min gap

    flight3 = Flight("FL003", "JFK", "CDG",
                     "2024-02-01T21:30:00Z", "2024-02-01T23:00:00Z", "B747")  # Wrong origin

    flight4 = Flight("FL004", "LHR", "CDG",
                     "2024-02-01T20:45:00Z", "2024-02-01T22:00:00Z", "B747")  # 45 min gap (invalid)

    roster = Roster()

    return {
        "crew_dict": crew_dict,
        "flight1": flight1,  # JFK->LHR
        "flight2": flight2,  # LHR->CDG (90 min gap)
        "flight3": flight3,  # JFK->CDG (wrong origin)
        "flight4": flight4,  # LHR->CDG (45 min gap)
        "roster": roster
    }


# TEST 1: Valid connection (JFK->LHR, LHR->CDG)
def test_valid_connection_jfk_lhr_lhr_cdg(test_setup):
    """
    Test a valid connection (JFK->LHR, LHR->CDG).
    """
    test_setup["roster"].assign("C001", test_setup["flight1"])  # JFK->LHR
    test_setup["roster"].assign("C001", test_setup["flight2"])  # LHR->CDG

    is_valid, error = validate_roster(test_setup["roster"], test_setup["crew_dict"])

    assert is_valid, f"Valid connection should pass. Error: {error}"
    assert error == "", f"Error should be empty for valid roster. Got: {error}"


# TEST 2: Invalid location connection (JFK->LHR, JFK->CDG)
def test_invalid_location_connection_jfk_lhr_jfk_cdg(test_setup):
    """
    Test an invalid location connection (JFK->LHR, JFK->CDG).
    """
    test_setup["roster"].assign("C001", test_setup["flight1"])  # JFK->LHR
    test_setup["roster"].assign("C001", test_setup["flight3"])  # JFK->CDG

    is_valid, error = validate_roster(test_setup["roster"], test_setup["crew_dict"])

    assert not is_valid, "Invalid location connection should fail"
    assert "does not match" in error, f"Error should mention location mismatch. Got: {error}"
    assert "JFK" in error or "LHR" in error, "Error should mention airport codes"


# TEST 3: Invalid rest period (< 60 minutes)
def test_invalid_rest_period_less_than_60_min(test_setup):
    """
    Test an invalid rest period (< 60 mins).
    """
    test_setup["roster"].assign("C001", test_setup["flight1"])  # JFK->LHR (arrives 20:00)
    test_setup["roster"].assign("C001", test_setup["flight4"])  # LHR->CDG (departs 20:45) - 45 min gap!

    is_valid, error = validate_roster(test_setup["roster"], test_setup["crew_dict"])

    assert not is_valid, "Insufficient rest period should fail"
    assert "minutes" in error, f"Error should mention minutes. Got: {error}"
    assert "60" in error or "insufficient" in error.lower(), "Error should mention minimum 60 minutes"



# Run with: python -m pytest
