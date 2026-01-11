"""
Validator for SkyPy Crew Rostering System
Checks crew assignments against aviation rules.
"""


def validate_roster(roster, crew_dict):
    """
    Validate that all crew assignments in the roster are legal.

    Args:
        roster: Roster object with schedule dictionary
        crew_dict: {crew_id: Crew object} for qualification checks

    Returns:
        True if valid, False with error message if invalid
    """
    for crew_id, flights in roster.schedule.items():
        crew = crew_dict[crew_id]

        # Check aircraft qualifications for all flights
        for flight in flights:
            if flight.aircraft not in crew.qualifications:
                return False, f"Crew {crew_id} not qualified for {flight.aircraft}"

        # Check connections between flights
        for i in range(len(flights) - 1):
            current = flights[i]
            next_flight = flights[i + 1]

            # Location continuity check
            if current.destination != next_flight.origin:
                return False, (f"Illegal connection for Crew {crew_id}: {current.destination} " f"does not match {next_flight.origin}")

            # Minimum rest check (60 minutes)
            time_gap = (next_flight.departure - current.arrival).total_seconds() / 60
            if time_gap < 60:
                return False, f"Insufficient rest for Crew {crew_id}: only {int(time_gap)} minutes"

    return True, ""

