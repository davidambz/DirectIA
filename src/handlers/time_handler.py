import time
import random

def human_sleep(min_seconds: float = 2.0, max_seconds: float = 5.0):
    duration = random.uniform(min_seconds, max_seconds)
    time.sleep(duration)