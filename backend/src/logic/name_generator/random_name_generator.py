import os
import random

# credits to https://github.com/dgoldstein0/GLST/blob/master/planet%20names.txt for the list of planet names


def generate_planet_name():
    """
    Take a random name as planet name
    """
    dirname = os.path.dirname(os.path.abspath(__file__))
    planet_names = open(f"{dirname}/planet_names.txt", "r")
    lines = planet_names.readlines()
    random_line = random.choice(lines)
    return str(random_line)
