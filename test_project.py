from project import check_stale_sensors, check_delayed_braking, check_missing_response
import datetime


def test_check_stale_sensors():
    event1 = [
        {
            "event_type": "sensor_scan",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 0),
        },
        {
            "event_type": "collision",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 6),
        },
    ]
    event2 = [
        {
            "event_type": "sensor_scan",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 5),
        },
        {
            "event_type": "collision",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 6),
        },
    ]

    assert check_stale_sensors(event1) is True
    assert check_stale_sensors(event2) is False


def test_check_delayed_braking():
    event1 = [
        {
            "event_type": "obstacle_detected",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 2),
        },
        {
            "event_type": "brake_command",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 5),
        },
    ]

    event2 = [
        {
            "event_type": "obstacle_detected",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 2),
        },
        {
            "event_type": "brake_command",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 3),
        },


    ]

    assert check_delayed_braking(event1) is True
    assert check_delayed_braking(event2) is False


def test_check_missing_response():
    event1 = [
        {
            "event_type": "obstacle_detected",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 2),
        },

        {
        "event_type": "brake_command",
        "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 3),
        },
        {
            "event_type": "collision",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 6),
        },

    ]

    event2 = [
        {
            "event_type": "obstacle_detected",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 2),
        },
        {
            "event_type": "collision",
            "parsed_timestamp": datetime.datetime(2026, 9, 27, 10, 0, 6),
        },
    ]

    assert check_missing_response(event1) is False
    assert check_missing_response(event2) is True