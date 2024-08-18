import time


__default = "__default"
__values = {}


def tic(name: str = __default) -> None:
    """First time"""
    time_seg = time.perf_counter()
    __values[name] = [time_seg]


def tac(name: str = __default) -> float:

    time_seg = time.perf_counter()

    __values[name].append(time_seg)
    return __values[name][-1] - __values[name][-2]


def toc(name: str = __default, skip_toc=False) -> dict:
    if not skip_toc:
        tac(name)
    steps = []
    for index in range(1, len(__values[name])):
        steps.append(__values[name][index] - __values[name][index - 1])
    total = __values[name][-1] - __values[name][0]
    del __values[name]
    return {"name": name, "total": total, "steps": steps}


def get_active_timers():
    return ", ".join(__values.keys())
