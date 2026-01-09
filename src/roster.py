"""
Roster class for SkyPy Crew Rostering System.
Manages crew assignments to flights and maintains schedule integrity.
"""


class Roster:
    """
    Initialize an empty roster.

    The roster is a dictionary where:
    - Key: crew_id (string)
    - Value: List of Flight objects assigned to that crew, sorted chronologically
    """
    def __init__(self):
        self.schedule = {}

    def assign(self, crew_id, flight):
        if crew_id not in self.schedule:
            self.schedule[crew_id] = []
        self.schedule[crew_id].append(flight)
        self.schedule[crew_id].sort(key=lambda f: f.departure)

