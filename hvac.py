class HVAC(object):
    def __init__(self):
        self.blower = Blower()
        self.coil = Coil()
        self.staticPressure = 0.0 # Pa
        return

class Blower(object):
    # performance curves
    #  static pressure vs CFM
    #  brake horsepower vs CFM
    def __init__(self):
        return

class Coil(object):
    # different behavior in heating vs cooling
    # PID to maintain setpoint? or simplified
    def __init__(self):
        self.setpoint = 25
        self.temperature = 25
        return
