import random


def get_random_number(count):
    sleeptime = (random.randint(7, 13) + random.random()) / count
    return sleeptime
