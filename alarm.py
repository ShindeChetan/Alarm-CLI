import time
import datetime
import sys
import os

def play_sound():
    """
    Attempts to play a sound based on the operating system.
    Falls back to a terminal bell if specific OS sounds are unavailable.
    """
    if os.name == 'nt':
        try:
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
            # Or play a frequency: winsound.Beep(1000, 1000)
        except ImportError:
            sys.stdout.write('\a')
            sys.stdout.flush()
    else:
        # Mac/Linux fallback to terminal bell
        sys.stdout.write('\a')
        sys.stdout.flush()

class Alarm:
    def __init__(self, target_time: datetime.datetime, message: str = "Alarm!"):
        self.target_time = target_time
        self.message = message

    def time_remaining(self) -> datetime.timedelta:
        return self.target_time - datetime.datetime.now()

    def wait_and_trigger(self):
        """
        Blocks the current thread until the target time is reached, then triggers.
        """
        while True:
            remaining = self.time_remaining()
            if remaining.total_seconds() <= 0:
                break
            
            # Sleep in small increments to allow for interruption (e.g. KeyboardInterrupt)
            sleep_duration = min(remaining.total_seconds(), 1.0)
            time.sleep(sleep_duration)

        self.trigger()

    def trigger(self):
        """
        Executes the alarm notification.
        """
        print(f"\n[ALARM] {self.message}")
        play_sound()

