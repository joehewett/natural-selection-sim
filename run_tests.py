import json
from os import walk, path
from nss import Simulation, add_food, create_moids

def run_test(name, test):
    simulation_settings = test['simulation_settings']
    entities_cycles = test['entities_cycles']

    print(f'Running test {name} with {len(entities_cycles)} cycles.')

    simulation = Simulation(**simulation_settings)
    add_food(100, 20, simulation)
    create_moids(5, simulation)

    for i in range(len(entities_cycles)):
        simulation.do_cycles(1, False)

        assert verify_cycle(simulation.entities, entities_cycles[i]), f'\033[91mFailed cycle in test {name}!\033[0m'
    
    print(f'Code passed test {name}!')

def verify_cycle(entities, test_cycle):
    passed = False

    for location, entity in entities.items():
        passed = {
            'x': location[0],
            'y': location[1],
            'type': str(type(entity))
        } in test_cycle

    return len(entities) == len(test_cycle) and passed

def read_test(file_path):
    data = None

    with open(file_path) as file:
        data = json.load(file)

    return data

def run_tests():
    print('Running tests...')

    for root, dirs, files in walk('tests/'):
        test_files = list(filter(lambda name: name.endswith('.json'), files))
        total = len(test_files)

        print(f'Found {total} test(s)')

        for file_name in test_files:
            file_path = path.join(root, file_name)

            run_test(file_name, read_test(file_path))

    print()
    print(25 * '=')
    print('\033[92mAll tests passed successfully\033[0m')
        
if __name__ == '__main__':
    run_tests()