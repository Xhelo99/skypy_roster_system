"""
Exporter for SkyPy Crew Rostering System.
Exports roster to JSON format as specified in requirements.
"""

import json
from src.roster import Roster


def export_roster_to_json(roster: Roster, output_path: str) -> None:
    """
    Export roster to JSON file in the required format.

    Required JSON format:
    {
        "C001": ["FL001", "FL003"],
        "C002": ["FL002"],
        "unassigned": ["FL004", "FL005"]
    }

    Args:
        roster: Roster object to export
        output_path: Path to output JSON file
    """
    # Convert roster to JSON format
    json_data = _roster_to_dict(roster)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=2)

    print(f"✅ Roster exported to: {output_path}")


def _roster_to_dict(roster: Roster) -> dict:
    """
    Convert Roster object to dictionary matching JSON spec.

    Args:
        roster: Roster object

    Returns:
        Dictionary ready for JSON serialization
    """
    result = {}

    # Add crew assignments
    for crew_id, flights in roster.schedule.items():
        result[crew_id] = [flight.flight_id for flight in flights]

    # Add unassigned flights (if any)
    if hasattr(roster, 'unassigned_flights') and roster.unassigned_flights:
        result['unassigned'] = [flight.flight_id for flight in roster.unassigned_flights]

    return result