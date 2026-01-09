"""
Crew class for SkyPy Crew Rostering System.
Represents a crew member with their base location and qualifications.
"""

class Crew:
    """Represents a crew member who can be assigned to flights."""
    def __init__(self, crew_id: str, home_base: str, qualifications: str):
        """
        Initialize a Crew member.

        Args:
            crew_id: Unique identifier for the crew member (e.g., "C001")
            home_base: 3-letter airport code where crew is based (e.g., "JFK")
            qualifications: Semicolon-separated string of aircraft types (e.g., "B747;A320")
        """
        self.crew_id = crew_id
        self.home_base = home_base
        self.qualifications = self._parse_qualifications(qualifications)

    def _parse_qualifications(self, qualifications_str):
        """
        Parse semicolon-separated qualifications string into a list.

        Args:
            qualifications_str: String like "B747;A320;B737"

        Returns:
            List of aircraft type strings
        """
        if not qualifications_str:
            return []

        quals = [q.strip() for q in qualifications_str.split(';') if q.strip()]
        return quals


