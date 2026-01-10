"""
Scheduler for SkyPy Crew Rostering System.
Automatically assigns flights to crew members while using the validator.
"""

from roster import Roster
from validator import validate_roster


def schedule_flights_minimal(flights, crew_list):
    """
    Automatically assign flights to crew members.

    Algorithm:
    1. Sort all flights chronologically by departure time
    2. For each flight in sorted order:
        a. Try to assign it to each crew member (in order given)
        b. Use validator logic to check if assignment is legal
        c. If valid → assign and move to next flight
        d. If no crew can take it → mark as unassigned

    Args:
        flights: List of Flight objects to assign
        crew_list: List of Crew objects available

    Returns:
        Roster object with assignments and unassigned flights
    """

    sorted_flights = sorted(flights, key=lambda f: f.departure)
    roster = Roster()
    crew_dict = {crew.crew_id: crew for crew in crew_list}

    for flight in sorted_flights:
        assigned = False

        for crew in crew_list:
            if flight.aircraft not in crew.qualifications:
                continue

            roster.assign(crew.crew_id, flight)
            is_valid, _ = validate_roster(roster, crew_dict)

            if is_valid:
                assigned = True
                break
            else:
                roster.schedule[crew.crew_id].pop()

        if not assigned:
            roster.unassigned_flights.append(flight)

    return roster
