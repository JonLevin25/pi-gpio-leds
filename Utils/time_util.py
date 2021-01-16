import time


class Time:
    @classmethod
    def bpm_to_secs_per_beat(cls, bpm):
        return 60 / bpm

    @classmethod
    def now(cls):
        return time.time()