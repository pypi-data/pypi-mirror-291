import ctypes
from ctypes import c_void_p

def load_SoGL():
    lib = None
    if __import__('sys').platform == 'win32':
        lib = ctypes.CDLL('./ext/SoGL/sogl64.dll')

    # error loading SoGL library!
    if lib == None: return lib
    else:
        # configure SoGL functions
        lib['soglInit'].restype = c_void_p

    return lib

def load_SwarmECS():
    try:
        import swarm as swarmECS
    except ImportError as err:
        print(f"Error Importing Swarm-ECS: Please Install it with `pip install -U Swarm-ECS`\n{err}")
        return None
    
    return swarmECS

