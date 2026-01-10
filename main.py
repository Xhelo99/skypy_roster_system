from src.data_loader import load_all_data
from src.scheduler import schedule_flights
from src.exporter import export_roster_to_json
import os

def main():
    # Load
    flights, crew = load_all_data("data/flights.csv", "data/crew.csv")

    # Schedule
    roster = schedule_flights(flights, crew)

    # Export
    os.makedirs("outputs", exist_ok=True)
    export_roster_to_json(roster, "outputs/roster_output.json")

if __name__ == "__main__":
    main()