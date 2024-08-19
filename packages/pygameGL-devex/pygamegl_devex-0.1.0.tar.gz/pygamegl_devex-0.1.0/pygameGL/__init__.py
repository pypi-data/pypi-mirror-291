from .deps import load_SoGL, load_SwarmECS

class _PYGL:
    class core:
        """ stats/info of core modules in PygameGL """
        ...

    class deps: 
        """ stats/info of core dependancies for PygameGL """
        sogl:bool=load_SoGL()
        swarm:bool=load_SwarmECS()

    class plugs:
        """ eventual plugin support for pipeline modification """
        ...
PYGL:_PYGL=_PYGL()

if __name__ == '__main__':
    print(f"PygameGL [ OpenGL 430 | GLFW 3.4 | GLEW 2.2.0 ]")
    load_SoGL()
    load_SwarmECS()

    def init() -> None:
        PYGL.deps.sogl.soglInit()

