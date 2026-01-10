"""
Data loader for SkyPy Crew Rostering System.
Loads CSV files into Flight and Crew objects.
"""

import csv
from typing import List, Tuple
from src.flight import Flight
from src.crew import Crew


def load_flights(csv_path: str) -> List[Flight]:
    """
    Load flights from CSV file.

    CSV format:
    flight_id,origin,destination,departure,arrival,aircraft

    Args:
        csv_path: Path to flights.csv

    Returns:
        List of Flight objects

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV data is invalid
    """
    flights = []

    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=1):
            try:
                flight = Flight(
                    flight_id=row['flight_id'].strip(),
                    origin=row['origin'].strip(),
                    destination=row['destination'].strip(),
                    departure=row['departure'].strip(),
                    arrival=row['arrival'].strip(),
                    aircraft=row['aircraft'].strip()
                )
                flights.append(flight)

            except KeyError as e:
                raise ValueError(f"Missing column in CSV row {row_num}: {e}")
            except ValueError as e:
                raise ValueError(f"Invalid data in CSV row {row_num}: {e}")

    return flights


def load_crew(csv_path: str) -> List[Crew]:
    """
    Load crew from CSV file.

    CSV format:
    crew_id,home_base,qualifications

    Args:
        csv_path: Path to crew.csv

    Returns:
        List of Crew objects

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV data is invalid
    """
    crew_list = []

    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row_num, row in enumerate(reader, start=1):
            try:
                crew = Crew(
                    crew_id=row['crew_id'].strip(),
                    home_base=row['home_base'].strip(),
                    qualifications=row['qualifications'].strip()
                )
                crew_list.append(crew)

            except KeyError as e:
                raise ValueError(f"Missing column in CSV row {row_num}: {e}")
            except Exception as e:
                raise ValueError(f"Invalid data in CSV row {row_num}: {e}")

    return crew_list


def load_all_data(flights_path: str, crew_path: str) -> Tuple[List[Flight], List[Crew]]:
    """
    Load both flights and crew data.

    Args:
        flights_path: Path to flights.csv
        crew_path: Path to crew.csv

    Returns:
        Tuple of (flights_list, crew_list)
    """
    flights = load_flights(flights_path)
    crew = load_crew(crew_path)

    return flights, crew
