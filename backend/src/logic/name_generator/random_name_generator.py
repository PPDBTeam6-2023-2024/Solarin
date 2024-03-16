import random

# credits to https://github.com/dgoldstein0/GLST/blob/master/planet%20names.txt for the list of planet names
def generate_planet_name():
    planet_names = open("planet_names.txt", "r")
    lines = planet_names.readlines()
    random_line = random.choice(lines)
    print(random_line)


