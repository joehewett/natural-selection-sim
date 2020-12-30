import json
import os
from nss import Simulation, add_food, create_moids

def generate_test_cli():
    name = input('Please enter the test name: ')
    seed = input('Please enter the test seed: ')
    max_x = input('Please enter the max_x: ')
    max_y = input('Please enter the max_y: ')

    simulation_settings = {'seed': seed, 'max_x': max_x, 'max_y': max_y}
    entities_cycles = []

    simulation = Simulation(**simulation_settings)

    add_food(100, 20, simulation)
    create_moids(5, simulation)

    for i in range(200):
        simulation.do_cycles(1, False)
        entities_cycles.append(serialize_entities(simulation.entities))

    test = {'simulation_settings': simulation_settings, 'entities_cycles': entities_cycles}
    save_test(name, test)

def serialize_entities(entities):
    serialized = []

    for location, entity in entities.items():
        serialized.append({
            'x': location[0],
            'y': location[1],
            'type': str(type(entity))
        })

    return serialized

def save_test(name, data):
    with open(os.path.join('tests/', f'{name}.json'), 'w') as file:
        json.dump(data, file)

if __name__ == '__main__':
    generate_test_cli()