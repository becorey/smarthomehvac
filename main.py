
from pprint import pprint
from controller import Controller
from home import Home
from hvac import HVAC
from occupant import Occupant


def main():
    home = Home()
    print ("test")
    pprint(home.__dict__)

if __name__ == '__main__':
    main()
