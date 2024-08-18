import builtins
import numpy as np


def info(data: dict, quantile=80, add_marker="!"):
    steps = np.array(data["steps"])
    quantile_value = np.quantile(steps, quantile / 100)

    max_number_sign = 20
    steps_over_q80 = np.where(steps >= quantile_value, steps, np.nan)

    max_value = np.max(steps)
    normalized = (steps / max_value) * max_number_sign

    lines = []
    for i, value in enumerate(normalized):
        bar = "#" * int(value)
        marker = add_marker if steps[i] >= quantile_value else ""
        lines.append(f"{i: 2d} | {bar} {marker}")

    return {
        "quantile": quantile,
        "quantile_value": quantile_value,
        "steps_over_quantile": steps_over_q80,
        "graphic": "\n".join(lines),
    }


def print(data: dict, quantile=80, add_marker="!"):
    result = info(data, quantile, add_marker)
    builtins.print("==" * 20)
    builtins.print(data["name"])
    builtins.print("-" * 20)
    builtins.print(result["graphic"])
    builtins.print("-" * 20)
    builtins.print("quantile value: " + str(result["quantile_value"]))
    builtins.print("==" * 20)
    return result
