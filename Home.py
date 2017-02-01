class Home(object):
    # Contains Rooms, Ducts, and HVAC
    def __init__(self):
        self.rooms = self.generateRooms()
        self.ducts = self.generateDucts()
        self.hvac = HVAC()
        return

    def generateRooms(self):
        rooms = []
        for i in range(0,4):
            rooms.append(Room())
        return rooms

    def generateDucts(self):
        ducts = []
        return ducts

class Room(object):
    # wall convention: start at top, clockwise
    #   0,1,2,3 = up,right,down,left
    def __init__(self):
        self.temperature = 24.0
        self.humidity = 0.4
        self.co2 = 0.0
        self.occupied = False
        self.vent = 1.0
        self.noise = 0.0

        # length is in the y direction, down to up
        self.length = 4.0 # m
        # width is in the x direction, left to right
        self.width = 3.5 # m
        self.height = 3.0 # m
        self.walls = self.generateWalls(self)
        # doors
        # windows
        return

    def generateWalls(self, room):
        walls = []
        for i in range(0,4):
            if i == 0 or i == 2:
                # up or down, use room width
                length = room.width
            else:
                # left or right, use room length
                length = room.length
            height = room.height
            walls.append(Wall(length, height))
        return walls

class Wall(object):
    def __init__(self, length, height):
        self.insulation = {'conductivity': 1.0, 'thickness': 0.025}
         # conductivity [W/m-C], thickness [m]
        self.length = length
        self.height = height
        return

class Duct(object):
    def __init__(self):
        self.connections = []
        self.diameter = .030 #meters
        self.area = math.pi * math.pow(self.diameter, 2) #m^2 cross sectional area
        self.length = 1.0 # m
        self.insulation.conductivity = 0.034 # W/m-C
        self.insulation.thickness = .025 # m
        self.leakage = 0.0 #m^3/hr
        return

class Environment(object):
    def __init__(self):
        self.temperature = 30.0 # C
        self.humidity = 0.5
        self.climate = "humid" # dry or humid
        self.solarIrradiance = 1.0 # W/m^2, time and date dependent
        return
