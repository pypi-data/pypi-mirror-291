import pytest

from mx_bluesky.i24.serial.fixed_target.ft_utils import ChipType
from mx_bluesky.i24.serial.parameters import FixedTargetParameters, get_chip_format


@pytest.fixture
def dummy_params_without_pp():
    oxford_defaults = get_chip_format(ChipType.Oxford)
    params = {
        "visit": "foo",
        "directory": "bar",
        "filename": "chip",
        "exposure_time_s": 0.01,
        "detector_distance_mm": 100,
        "detector_name": "eiger",
        "num_exposures": 1,
        "chip": oxford_defaults.dict(),
        "map_type": 1,
        "pump_repeat": 0,
        "checker_pattern": False,
    }
    return FixedTargetParameters(**params)
