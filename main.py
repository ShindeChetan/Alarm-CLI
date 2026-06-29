import argparse
import datetime
import sys

from utils import parse_absolute_time, parse_relative_time
from alarm import Alarm

def setup_parser():
    parser = argparse.ArgumentParser(description="Python CLI Alarm Clock")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 'set' command for absolute time
    set_parser = subparsers.add_parser("set", help="Set an alarm for a specific time (HH:MM)")
    set_parser.add_argument("time", type=str, help="Time in HH:MM format (24-hour)")
    set_parser.add_argument("-m", "--message", type=str, default="Alarm!", help="Message to display when alarm triggers")
    
    # 'in' command for relative time
    in_parser = subparsers.add_parser("in", help="Set an alarm to trigger in a given amount of time (e.g., 10m, 5s, 1h)")
    in_parser.add_argument("duration", type=str, help="Duration (e.g., '10s', '5m', '1h')")
    in_parser.add_argument("-m", "--message", type=str, default="Alarm!", help="Message to display when alarm triggers")
    
    return parser

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    try:
        now = datetime.datetime.now()
        target_time = None
        
        if args.command == "set":
            target_time = parse_absolute_time(args.time, now)
            print(f"Alarm set for {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
        elif args.command == "in":
            delta = parse_relative_time(args.duration)
            target_time = now + delta
            print(f"Alarm set for {delta} from now ({target_time.strftime('%Y-%m-%d %H:%M:%S')})")
            
        if target_time:
            alarm = Alarm(target_time=target_time, message=args.message)
            print("Waiting for alarm to trigger... (Press Ctrl+C to cancel)")
            alarm.wait_and_trigger()
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")
        sys.exit(0)

if __name__ == "__main__":
    main()
