import sys
import random

class Simulation:

    def __init__(self, max_x, max_y, seed):
        self.seed = seed
        self.max_x = max_x
        self.max_y = max_y
        self.entities = {}

        random.seed(seed)
    
    def do_cycles(self, num_moves, display=True):
        for i in range(0, num_moves):
            for location in self.entities.copy().keys():
                entity = self.entities[location]
                if type(entity) is Moid:
                    if entity.life_status == "alive":
                        entity.sense()

            if display:
                print("\nCurrent move: " + str(i))
                self.display()

                input()
    
    def add_entity(self, entity, x, y):
        entity.set_entities(self.entities)
        self.entities[(x,y)] = entity

    def display_moids_info(self):
        total_sense_distance = 0
        num_alive_moids = 0
        print("\nDisplaying Moid information:\n")

        for location in self.entities.copy().keys():
            entity = self.entities[location]

            if type(entity) is Moid:
                if entity.life_status == "alive":
                    total_sense_distance += entity.sense_distance
                    num_alive_moids += 1

                    print(entity.display_info())
        
        avg_sense_distance = total_sense_distance / num_alive_moids
        print("There are currently " + str(num_alive_moids) + " living Moids")
        print("The average sense distance is " + str(avg_sense_distance))

    def display(self):
        map_text = ""
        for y in range(1, self.max_y + 1):
            map_text += "\n"
            for x in range(1, self.max_x + 1):
                
                location = (x, y)

                if location in self.entities.keys():  
                    map_text += self.entities[location].get_symbol()     
                else:
                    map_text += " \033[94m_"
        print(map_text + "\033[0m")

class Entity:
    def set_entities(self, entities):
        self.entities = entities

    def get_symbol(self):
        pass

class Food(Entity):
    def __init__(self, energy):
        self.energy = energy
    
    def get_energy(self):
        return self.energy

    def get_symbol(self):
        return " \033[92mo"

class Moid(Entity):

    def __init__(self, id, x, y, energy, sense_distance):
        self.id = id
        self.x = x
        self.y = y
        self.energy = energy
        self.sense_distance = sense_distance
        self.nearest_food = ""
        self.total_moves = 0

        self.life_status = "alive"

        mutation_chance = random.random()
        if mutation_chance > 0.5:
            self.mutate()

    def get_symbol(self):
        return " \033[91m¦"        

    def display_info(self):
        info = ("Moid ID: " + str(self.id))
        info += (" | Energy: " + str(self.energy))
        info += (" | XY: " + "(" + str(self.x) + ", " + str(self.y) + ")")
        info += (" | Sense Distance: " + str(self.sense_distance))
        info += (" | Moves: " + str(self.total_moves))
        info += (" | Status: " + str(self.life_status))

        return info

    def get_random_next_cords(self, x, y):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        return x + dx, y + dy

    def move(self, directed = False): 
        new_x = self.x
        new_y = self.y

        if directed:
            if self.nearest_food[0] > self.x:
                new_x += 1
            elif self.nearest_food[0] < self.x:
                new_x -= 1
            elif self.nearest_food[1] > self.y:
                new_y += 1
            else:
                new_y -= 1
        else:
            new_x, new_y = self.get_random_next_cords(self.x, self.y)

            # TODO: Change to match max_y and max_x
            while not (0 < new_x <= 20 and 0 < new_y <= 20):
                new_x, new_y = self.get_random_next_cords(self.x, self.y)

        self.x = new_x
        self.y = new_y
        self.total_moves += 1

        self.energy -= 1

        if self.energy <= 0:
            self.die()
        elif self.energy >= 100:
            self.reproduce()
        
        if self.total_moves > 100:
            self.die()

        self.check_space(new_x, new_y)

    def check_space(self, new_x, new_y):
        new_location = (new_x, new_y)

        if new_location in self.entities:
            entity = self.entities[new_location]

            if type(entity) is Food: 
                self.eat(entity, new_location)

    def eat(self, food, location):
        self.energy += food.get_energy()
        
        self.entities.pop(location)

    def mutate(self):
        change = random.choice([-1, 1])
        if self.sense_distance + change >= 1:
            self.sense_distance += change

    def reproduce(self):
        stem_moid = str(self.id[0])
        #generation = str(self.id[1] + 1)
        generation = self.id[1] + 1
        new_id = (stem_moid, generation)

        if self.y < 50:
            spawn_y = self.y + 1
            spawn_x = self.x
        elif self.x < 50:
            spawn_x = self.x + 1
            spawn_y = self.y
        else: 
            spawn_x = self.x - 1
            spawn_y = self.y - 1
        
        # TODO: Check if location is occupied

        new_moid = Moid(new_id, spawn_x, spawn_y, 50, self.sense_distance)
        new_moid.set_entities(self.entities)

        self.entities[(spawn_x, spawn_y)] = new_moid

        self.energy -= 50

    def die(self):
        self.life_status = "dead"

    def get_nearest_food(self):
        lowest_dist = 100
        nearest_food = None

        for location in self.entities.keys():
            entity = self.entities[location]
            if type(entity) is Food:
                total_distance = get_distance(self.x, self.y, location[0], location[1])
                
                if total_distance < lowest_dist:
                    lowest_dist = total_distance
                    nearest_food = location
        
        return nearest_food

    def sense(self):
        self.nearest_food = self.get_nearest_food()
        distance_to_food = get_distance(self.x, self.y, self.nearest_food[0], self.nearest_food[1])

        old_location = (self.x, self.y)

        if distance_to_food <= self.sense_distance:
            self.move(True)
        else:
            self.move(False)

        self.entities.pop(old_location)

        if self.life_status == "alive":
            self.entities[(self.x, self.y)] = self 

def get_distance(current_x, current_y, desired_x, desired_y):
    distance_x = abs(desired_x - current_x)
    distance_y = abs(desired_y - current_y)
    total_distance = distance_x + distance_y
    return total_distance

def add_food(num_food, energy, simulation, verbose=False):
    i = 0
    while i < num_food:
        x, y = random.randint(1,20), random.randint(1,20)
        if (x, y) not in simulation.entities:
            simulation.add_entity(Food(10), x, y)
            i += 1
    
    if verbose:
        print("\nAdding " + str(num_food) + " food with energy " + str(energy))

# create some moids
def create_moids(num_moids, simulation, verbose=False):
    for i in range(1, num_moids + 1):
        x, y = random.randint(1,20), random.randint(1,20)
        baby_moid = Moid((i, 0), x, y, 30, 3)

        simulation.add_entity(baby_moid, x, y)
    
    if verbose:
        print("Creating " + str(num_moids) + " Moids")

if __name__ == '__main__':
    print("\nMoid Natural Selection Simulation\n")

    simulation = Simulation(20, 20, seed="WAI")
    add_food(100, 20, simulation)
    create_moids(5, simulation)

    # Begin menu display
    exit = False
    while not exit:
        print("\n=========================================")
        print("Press 1 to Add a Moid")
        print("Press 2 to Add Food")
        print("Press 3 to See Moid Info")
        print("Press 4 to View Map")
        print("Press x to Begin Evolution Cycle")
        print("=========================================\n")
        val = input("Press a key: ")    
        if val == "1": 
            create_moids(1, simulation, verbose=True)
        elif val == "2":
            add_food(10, 10, simulation, verbose=True)
        elif val == "3":
            simulation.display_moids_info()      
        elif val == "4":
            simulation.display()
        elif val == "x":
            print("Beginning evolution cycle")
            simulation.do_cycles(100)
        elif val == "q":
            print("Exiting")
            exit = True







     

# TO DO 

# Make moid to path to nearest food when food detected
# Make offspring mutate their sense distance up or down on birth
# Test and hopefully observe population sense distance change over time
# 



# DONE
# add a new moid attribute with states 0, 1, 2 (die, survive, reproduce)
# upon beginning a cycle, begin random walk 
# create a cycle routine that controls the cycles on key press
# add check to ensure moid doesn't leave boundaries
# Fix food map display
# Change cycle routine to step on key press
# each tick, check current location against the food map
# if there is a match, call a function that deletes food from list and increases energy of moid, and changes survival state of moid
# Create pathing algorithm 
