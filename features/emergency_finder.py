 
# features/emergency_finder.py
from agent.tools import find_emergency_hospitals

def get_emergency_help(city: str):
    return find_emergency_hospitals(city)