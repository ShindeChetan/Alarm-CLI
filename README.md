# Python CLI Alarm Clock

A simple, robust Python Command Line Interface (CLI) application for setting alarms. Designed as part of a 30-minute build exercise.

## Features
- **Absolute Time Alarms**: Set an alarm for a specific time (e.g., `15:30`).
- **Relative Time Alarms**: Set an alarm to trigger in a certain amount of time (e.g., `10s`, `5m`, `1h`).
- **Custom Messages**: Add custom messages to display when the alarm triggers.
- **Cross-Platform Sound**: Plays a system beep/sound when the alarm goes off (falls back to terminal bell if not on Windows).
- **Zero Dependencies**: Uses only the Python Standard Library (`argparse`, `datetime`, `time`, `threading`).

## Requirements
- Python 3.6 or higher.

## Usage

### 1. Set an Absolute Alarm
Set an alarm for a specific time using the 24-hour format `HH:MM`.

```bash
python main.py set 15:30
```
With a custom message:
```bash
python main.py set 15:30 -m "Time for a meeting!"
```

### 2. Set a Relative Alarm
Set an alarm to trigger in a given duration (`s` for seconds, `m` for minutes, `h` for hours).

```bash
python main.py in 10s
```
With a custom message:
```bash
python main.py in 5m -m "Tea is ready!"
```

## Running Tests
To verify the application logic, run the included unit tests:

```bash
python test_alarm.py
```

## Architecture & Code Flow

The application is structured into three distinct modules to separate concerns and ensure maintainability:

1. **`main.py` (Presentation & Routing)**
   - Acts as the entry point.
   - Sets up the `argparse` CLI interface.
   - Routes the parsed commands to the appropriate utilities to determine the target time.
   - Instantiates the `Alarm` object and triggers the waiting process.

2. **`utils.py` (Business Logic & Parsing)**
   - Contains pure functions for parsing user input strings.
   - `parse_absolute_time()`: Converts strings like "15:30" into a concrete `datetime` object for the future.
   - `parse_relative_time()`: Converts strings like "10s" into a `timedelta` object.

3. **`alarm.py` (Domain Model & Execution)**
   - Defines the `Alarm` class which encapsulates the target time and message.
   - Handles the blocking execution loop (`wait_and_trigger()`), which sleeps in small intervals until the target time is reached.
   - Manages cross-platform notifications (printing to stdout and playing system sounds via `winsound` or terminal bell).

### Code Flow Example: `python main.py in 10s -m "Hello"`
1. **User Input:** The user executes the command in the terminal.
2. **Parsing:** `main.py` parses `in`, `10s`, and `-m "Hello"`.
3. **Time Calculation:** `main.py` calls `parse_relative_time("10s")` from `utils.py`, returning a 10-second `timedelta`. It adds this to the current time to get the exact target `datetime`.
4. **Alarm Instantiation:** An `Alarm(target_time, message="Hello")` object is created.
5. **Waiting Phase:** `alarm.wait_and_trigger()` is called. The thread blocks, waking up briefly every second to check if the target time has passed, ensuring it can respond to `Ctrl+C` interrupts.
6. **Notification:** Once the time expires, `alarm.trigger()` executes, printing the message and playing the alert sound. The application then exits successfully.
