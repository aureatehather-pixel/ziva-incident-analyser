import sys
import csv
import datetime

def main():
    event_log = load_events()
    sorted_events = sort_events(event_log)
    print_timeline(sorted_events)
    
    stale_sensor_found = check_stale_sensors(sorted_events)
    print(stale_sensor_found)

    delayed_braking_found = check_delayed_braking(sorted_events)
    print(delayed_braking_found)

    missing_response_found = check_missing_response(sorted_events)
    print(missing_response_found)

    
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



def check_stale_sensors(events):

    latest_scan_time = None
    
    for event in events:
        if event["event_type"] == "sensor_scan":
            latest_scan_time = event["parsed_timestamp"]

        if event["event_type"] == "collision" and latest_scan_time is not None:
            gap = event["parsed_timestamp"] - latest_scan_time

            if gap > datetime.timedelta(seconds=2):
                return True

    return False


def check_delayed_braking(events):
    latest_obstacle_time = None

    for event in events:
        if event["event_type"] == "obstacle_detected":
            latest_obstacle_time = event["parsed_timestamp"]

        if event["event_type"] == "brake_command" and latest_obstacle_time is not None:
            gap = event["parsed_timestamp"] - latest_obstacle_time

            if gap > datetime.timedelta(seconds=2):
                return True

            latest_obstacle_time = None

    return False


def check_missing_response(events):
    awaiting_response = False

    for event in events:
        if event["event_type"] == "obstacle_detected":
            awaiting_response = True

        if event["event_type"] == "brake_command" and awaiting_response:
            awaiting_response = False

        if event["event_type"] == "collision" and awaiting_response:
            return True

    return False



if __name__ == "__main__":
    main()