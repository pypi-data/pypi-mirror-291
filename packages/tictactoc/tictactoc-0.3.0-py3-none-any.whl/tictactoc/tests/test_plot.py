import pytest
from tictactoc import plot
import numpy as np


def test_info():
    q80_value = 0.796
    result = {
        "name": "test",
        "total": 13.2000,
        "steps": [
            0.8960,
            0.8782,
            0.7933,
            0.4228,
            0.6587,
            0.6564,
            0.7064,
            0.0001,
            0.2365,
            0.6697,
            0.8004,
            0.3373,
            0.1883,
            0.3643,
            0.2317,
            0.5605,
            0.9343,
            0.6843,
            0.7609,
            0.8216,
            0.0789,
            0.5299,
            0.5985,
            0.3911,
        ],
    }

    result_plot = plot.info(result)

    assert result_plot["quantile_value"] == pytest.approx(q80_value, 0.01)
    assert np.sum(~np.isnan(result_plot["steps_over_quantile"])) == 5
    assert result_plot["graphic"].count("!") == 5
