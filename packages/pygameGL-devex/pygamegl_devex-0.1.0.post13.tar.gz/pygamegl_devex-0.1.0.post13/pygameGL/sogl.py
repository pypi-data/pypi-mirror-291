import ctypes
from ctypes import c_void_p, POINTER, c_ubyte, c_int, c_char_p, c_uint32

SOGL_DLL:str = __file__.removesuffix('sogl.py')+"ext\\SoGL\\sogl64.dll"
GLFW_DLL:str = __file__.removesuffix('sogl.py')+"ext\\GL\\glfw3.dll"
GLEW_DLL:str = __file__.removesuffix('sogl.py')+"ext\\GL\\glew32.dll"

""" configure SoGL structures """
class SGcontext(ctypes.Structure):
    class Info(ctypes.Structure):
        _fields_ = [
            ("support_stereo_rendering", ctypes.c_uint),
            ("max_draw_buffers", ctypes.c_uint),
            ("max_texture_size", ctypes.c_uint),
            ("max_viewport_dims", ctypes.c_uint),
            ("max_vertex_attribs", ctypes.c_uint),
            ("max_component_passes", ctypes.c_uint),
            ("max_fragment_textures", ctypes.c_uint),
            ("max_vertex_uniforms", ctypes.c_uint),
            ("max_cubemap_texture_size", ctypes.c_uint),
            ("max_vertex_textures", ctypes.c_uint),
            ("max_shader_textures", ctypes.c_uint),
            ("max_fragment_uniforms", ctypes.c_uint),
            ("version", ctypes.c_char * 1024),
            ("renderer", ctypes.POINTER(ctypes.c_ubyte))
        ]
    _fields_ = [ ("info", Info) ]

def load_SoGL():
    lib = None
    if __import__('sys').platform == 'win32':
        lib = ctypes.CDLL(SOGL_DLL)

    # error loading SoGL library!
    if lib == None: return lib
    else:
        # configure SoGL functions
        lib['soglInit'].restype = c_void_p

        lib['sgContextDebug'].argtypes = [ POINTER(SGcontext) ]
        lib['sgContextDebug'].restype = c_void_p

        lib['sgPollEvents'].restype = c_void_p

        lib['sgShouldQuit'].restype = c_ubyte
        lib['sgShouldQuit'].argtypes = [ POINTER(c_void_p) ] 

        lib['sgSetWindowIcon'].restype = c_void_p
        lib['sgSetWindowIcon'].argtypes = [ c_void_p, c_void_p ]

        lib['sgSetWindowTitle'].restype = c_void_p
        lib['sgSetWindowTitle'].argtypes = [ c_void_p,  c_char_p ]

        lib['sgMakeWindow'].restype = c_void_p
        lib['sgMakeWindow'].argtypes = [ c_uint32, c_uint32, c_char_p ]

        lib['sgClearColor'].restype = c_void_p
        lib['sgClearColor'].argtypes = [ c_uint32, c_uint32, c_uint32, c_uint32 ]
        
        lib['sgBufferSwap'].restype = c_void_p
        lib['sgBufferSwap'].argtypes = [ c_void_p ]

    return lib


