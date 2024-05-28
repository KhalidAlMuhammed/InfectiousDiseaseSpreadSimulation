import random
import math
from matplotlib import pyplot as plt
import numpy as np
import csv
def normpdf(x, mean, sd):
    """
    Return the value of the normal distribution
    with the specified mean and standard deviation (sd) at
    position x.
    You do not have to understand how this function works exactly.
    """
    var = float(sd)**2
    denom = (2*math.pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom
def pdeath(x, mean, sd):
    start = x-0.5
    end = x+0.5
    step =0.01
    integral = 0.0
    while start<=end:
        integral += step * (normpdf(start,mean,sd) + normpdf(start+step,mean,sd)) / 2
        start += step
    return integral

recovery_time = 4
virality = 0.2
class Cell(object):

    def __init__(self,x, y):
        self.x = x
        self.y = y
        self.state = "S"
        self.time = 0

    def infect(self):
        self.state = "I"
        self.time = 0

    def die(self):
        self.state = "R"


    def process(self, adjacent_cells, virality, recovery_time, mean_death_time, stdev_death_time, consider_death, consider_recovery):
        if self.state == "I":
            if consider_recovery and self.time >= recovery_time:
                self.state = "S"
                self.time = 0
            else:
                if consider_death:
                    death_probability = pdeath(self.time, mean_death_time, stdev_death_time)
                    if random.random() <= death_probability:
                        self.die()
                if self.state == "I":
                    for neighbor in adjacent_cells:
                        if neighbor.state == "S" and random.random() <= virality:
                            neighbor.infect()
                    self.time += 1
        elif self.state == "S":
            self.time = 0
class Map(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = {}

    def add_cell(self, cell):
        self.cells[(cell.x, cell.y)] = cell

    def display(self):
      image = np.zeros((self.height, self.width, 3))
      for (x, y), cell in self.cells.items():
          if cell.state == 'S':
              color = [0, 1, 0]
          elif cell.state == 'I':
              color = [1, 0, 0]
          elif cell.state == 'R':
              color = [0.5, 0.5, 0.5]
          else:
              color = [0, 0, 0]
          image[cell.x, cell.y] = color
      plt.imshow(image)
      plt.show()


    def adjacent_cells(self, x,y):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.cells.get((nx, ny))
                if neighbor:
                    neighbors.append(neighbor)
        return neighbors

    def time_step(self, virality, recovery_time, mean_death_time, stdev_death_time, consider_death, consider_recovery):
        for cell in list(self.cells.values()):
            adjacent = self.adjacent_cells(cell.x, cell.y)
            cell.process(adjacent, virality, recovery_time, mean_death_time, stdev_death_time, consider_death, consider_recovery)
        self.display()
def image_example():
    '''should produce red,purple,green squares
    on the diagonal, over a black background'''
    red,green,blue = range(3)
    img = np.zeros((150,150,3))
    for x in range(50):
        for y in range(50):
            img[x,y,red] = 1.0
            img[x+50, y+50,:] = (.5,.0,.5)
            img[x+100,y+100,green] = 1.0
    plt.imshow(img)
def read_map(filename):
    map_instance = Map(150, 150)
    with open(filename, newline='') as csvfile:
        map_reader = csv.reader(csvfile, delimiter=',')
        for row in map_reader:
            x, y = int(row[0]), int(row[1])
            cell = Cell(x, y)
            map_instance.add_cell(cell)
    return map_instance
m = read_map('nyc_map.csv')
m.cells[(39, 82)].infect()
consider_death = input("Should the simulation consider death? (yes/no): ").lower() == 'yes'
consider_recovery = input("Should the simulation consider recovery? (yes/no): ").lower() == 'yes'
virality = 0.2
recovery_time = 4
mean_death_time = 3
stdev_death_time = 1

customize = input("""The default perameters are the following:

virality = 0.2
recovery_time = 4 
mean_death_time = 3
stdev_death_time = 1 

Do you want to customize the simulation parameters? (yes/no): """).lower() == 'yes'

if customize:
    virality = float(input("Please enter the virality of the infection (0 to 1): "))
    recovery_time = int(input("Please enter the recovery time of the infection (in time steps): "))
    if consider_death:
        mean_death_time = int(input("Please enter the mean death time of the infection (in time steps): "))
        stdev_death_time = float(input("Please enter the standard deviation time of the infection (in time steps): "))

for _ in range(25):
    m.time_step(virality, recovery_time, mean_death_time, stdev_death_time, consider_death, consider_recovery)