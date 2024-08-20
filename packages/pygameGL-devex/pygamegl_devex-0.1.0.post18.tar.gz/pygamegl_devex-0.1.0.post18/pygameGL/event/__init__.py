SOGL=None

def should_quit(win) -> bool:
    return SOGL.sgShouldQuit(win) == 1

def poll_events() -> None:
    SOGL.sgPollEvents()

