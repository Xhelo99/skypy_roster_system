"""
Flight class for SkyPy Crew Rostering System.
Represents a flight with timing, location, and aircraft information.
"""

from datetime import datetime


class Flight:
    def __init__(
        self,
        flight_id: str,
        origin: str,
        destination: str,
        departure: str,  # ISO 8601 string
        arrival: str,    # ISO 8601 string
        aircraft: str
    ):
        """
        Initialize a Flight.

        Args:
            flight_id: Unique flight identifier (e.g., "FL001")
            origin: 3-letter airport code (e.g., "JFK")
            destination: 3-letter airport code (e.g., "LHR")
            departure: ISO 8601 timestamp string (e.g., "2024-02-01T08:00:00Z")
            arrival: ISO 8601 timestamp string
            aircraft: Aircraft type (e.g., "B747")
        """

        self.flight_id = flight_id
        self.origin = origin
        self.destination = destination
        self.departure = self._parse_time(departure)
        self.arrival = self._parse_time(arrival)
        self.aircraft = aircraft
        self._validate_times()

    def _parse_time(self, time_str):
        # 'Z' means UTC. Used for time zone.
        if time_str.endswith('Z'):
            time_str = time_str[:-1]
        return datetime.fromisoformat(time_str)

    def _validate_times(self):
        if self.arrival <= self.departure:
            raise ValueError(f"Flight {self.flight_id}: Arrival must be after departure")

    @property
    def duration_minutes(self):
        delta = self.arrival - self.departure
        return int(delta.total_seconds() // 60)

