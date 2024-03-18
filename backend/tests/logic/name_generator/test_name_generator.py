from src.logic.name_generator import *

async def test_planet_name_generation():
    name = generate_planet_name()
    assert isinstance(name, str)