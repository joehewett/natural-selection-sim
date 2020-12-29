import sys
import random

random.seed(3)

class MoidMap:

    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
    
    def display(self, locations = {}):
        map_text = ""
        for y in range(1, self.max_y + 1):
            map_text += "\n"
            for x in range(1, self.max_x + 1):
                
                key = (x, y)

                if key in locations.keys():
                    if locations[key] == "food":
                        map_text += " o"
                    if locations[key] == "moid":
                        map_text += " ¦"        
                else:
                    map_text += " _"
        print(map_text)


class Moid:

    def __init__(self, id, x, y, energy, sense_distance):
        self.id = id
        self.x = x
        self.y = y
        self.energy = energy
        self.sense_distance = sense_distance
        self.nearest_food = ""
        self.total_moves = 0

        self.life_status = "alive"
        

    def display_info(self):

        info = ("Moid ID: " + str(self.id))
        info += (" | Energy: " + str(self.energy))
        info += (" | XY: " + "(" + str(self.x) + ", " + str(self.y) + ")")
        info += (" | Sense Distance: " + str(self.sense_distance))
        info += (" | Moves: " + str(self.total_moves))
        info += (" | Status: " + str(self.life_status))
        return info

    def move(self, directed = False): 
        
        new_x = self.x
        new_y = self.y
        if directed:
            if self.nearest_food[0] > self.x:
                new_x = self.x + 1
            elif self.nearest_food[0] < self.x:
                new_x = self.x - 1
            elif self.nearest_food[1] > self.y:
                new_y = self.y + 1
            else:
                new_y = self.y - 1
            self.x = new_x
            self.y = new_y
            self.total_moves += 1
        else:
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            new_x = self.x + dx
            new_y = self.y + dy
            if (0 < new_x <= 50) and (0 < new_y <= 50):
                self.x = new_x
                self.y = new_y
                self.total_moves += 1
            else:
                self.move(False)

        self.energy -= 1

        if self.energy <= 0:
            self.die()
        elif self.energy >= 100:
            self.reproduce()
        
        if self.total_moves > 100:
            self.die()

        self.check_space(food)

    def check_space(self, food):
        current_location = (self.x, self.y)
        if current_location in food: 
            self.eat()
            add_food(1)

    def eat(self):
        self.energy += 10
        food.remove((self.x, self.y))

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
        
        create_moid(new_id, spawn_x, spawn_y, 50, self.sense_distance)

        self.energy -= 50

    def die(self):
        self.life_status = "dead"

    def sense(self, locations = {}):
        nearest_food = get_nearest_food(self.x, self.y, locations)
        self.nearest_food = nearest_food
        
        distance_to_food = get_distance(self.x, self.y, self.nearest_food[0], self.nearest_food[1])
        if distance_to_food <= self.sense_distance:
            self.move(True)
        else:
            self.move(False)
        
def get_nearest_food(x, y, locations = {}):
    lowest_dist = 100
    nearest_food = ""
    for cords,entity_type in locations.items():            
        if entity_type == "food":
            total_distance = get_distance(x, y, cords[0], cords[1])
            
            if total_distance < lowest_dist:
                lowest_dist = total_distance
                nearest_food = cords
    return nearest_food

def get_distance(current_x, current_y, desired_x, desired_y):
    distance_x = abs(desired_x - current_x)
    distance_y = abs(desired_y - current_y)
    total_distance = distance_x + distance_y
    return total_distance

def add_food(num_food):
    i = 0
    while i < num_food:
        x, y = random.randint(1,20), random.randint(1,20)
        if (x, y) not in food:
            food.append((x, y))       
            i += 1

# create some moids
def create_initial_moids(num_moids):
    for i in range(1, num_moids + 1):
        create_moid((i, 0), random.randint(1,20), random.randint(1,20), 30, 3)
    print("Creating " + str(num_moids) + " Moids")


def create_moid(id, x, y, energy, sense_distance):
    baby_moid = Moid(id, x, y, energy, sense_distance)
    mutation_chance = random.random()
    if mutation_chance > 0.5:
        baby_moid.mutate()
    moids.append(baby_moid)


# display moid information
def display_moid_info():
    total_sense_distance = 0
    num_alive_moids = 0
    print("\nDisplaying Moid information:\n")
    
    for i in range (0, moids.__len__()):
        if moids[i].life_status == "alive":
            total_sense_distance += moids[i].sense_distance
            num_alive_moids += 1
            print(moids[i].display_info())
    avg_sense_distance = total_sense_distance / num_alive_moids
    print("There are currently " + str(num_alive_moids) + " living Moids")
    print("The average sense distance is " + str(avg_sense_distance))

# Begin a cycle of evolution for all currently living moids
def begin_evolution_cycle(num_moves):
    for i in range(0, num_moves):
        locations = get_current_locations()
        for e in range(0, moids.__len__()):
            if moids[e].life_status == "alive":
                moids[e].sense(locations)
               # print(moids[e].display_info())

        print("\nCurrent move: " + str(i))
        
        locations = get_current_locations()
        new_map.display(locations)

        input()
    print("DONE")

# Creates a dictionary of locations for all food and moids that can then be printed
def get_current_locations():
    list_locations = {}
    for i in range(0, food.__len__()):
        list_locations[food[i]] = 'food'

    for i in range(0, moids.__len__()):
        if moids[i].life_status == "alive":
            list_locations[(moids[i].x, moids[i].y)] = 'moid'

    return list_locations


print("\nMoid Natural Selection Simulation\n")

# list of moid objects
moids = []
create_initial_moids(10)

# list of food x,y tuples
food = []
add_food(20)

locations = {}
locations = get_current_locations()

new_map = MoidMap(20, 20)


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
        create_initial_moids(1)
    elif val == "2":
        add_food(10)
        print("There is now " + str(food.__len__()) + " food on the map")
    elif val == "3":
        display_moid_info()      
    elif val == "4":
        locations = get_current_locations()
        new_map.display(locations)
    elif val == "x":
        print("Beginning evolution cycle")
        begin_evolution_cycle(100)
    elif val == "0":
        locations = get_current_locations()
        moids[0].sense(locations)
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
