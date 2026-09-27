import sys
import csv
import datetime

def main():
    event_log = load_events()
    sorted_events = sort_events(event_log)
    print_timeline(sorted_events)
    


def load_events():
    events = []
    file_path = sys.argv[1]
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            events.append(parse_event(row))
    return events

            
def parse_event(row):

    row["parsed_timestamp"] = datetime.datetime.fromisoformat(row["timestamp"])
    return row

def sort_events(events):
    sorted_events = sorted(events, key=lambda event: event["parsed_timestamp"])
    return sorted_events
    
def print_timeline(events):
    print("Incident Timeline")
    print("-----------------")
    
    for event in events:
        print(f'{event["timestamp"]} | {event["source"]} | {event["event_type"]} | {event["details"]}')

if __name__ == "__main__":
    main()