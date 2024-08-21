from unittest.mock import ANY, MagicMock, call, patch

import cv2 as cv
import pytest
from dodal.devices.i24.pmac import PMAC
from dodal.devices.oav.oav_detector import OAV
from ophyd_async.core import get_mock_put

from mx_bluesky.i24.serial.fixed_target.i24ssx_moveonclick import (
    onMouse,
    update_ui,
    zoomcalibrator,
)


@pytest.mark.parametrize(
    "beam_position, expected_xmove, expected_ymove",
    [
        (
            (15, 10),
            "#1J:-" + str(15 * zoomcalibrator),
            "#2J:-" + str(10 * zoomcalibrator),
        ),
        (
            (475, 309),
            "#1J:-" + str(475 * zoomcalibrator),
            "#2J:-" + str(309 * zoomcalibrator),
        ),
        (
            (638, 392),
            "#1J:-" + str(638 * zoomcalibrator),
            "#2J:-" + str(392 * zoomcalibrator),
        ),
    ],
)
@patch("mx_bluesky.i24.serial.fixed_target.i24ssx_moveonclick._get_beam_centre")
def test_onMouse_gets_beam_position_and_sends_correct_str(
    fake_get_beam_pos: MagicMock,
    beam_position: tuple,
    expected_xmove: str,
    expected_ymove: str,
    pmac: PMAC,
    RE,
):
    fake_get_beam_pos.side_effect = [beam_position]
    fake_oav: OAV = MagicMock(spec=OAV)
    RE(onMouse(cv.EVENT_LBUTTONUP, 0, 0, "", param=[pmac, fake_oav]))
    mock_pmac_str = get_mock_put(pmac.pmac_string)
    mock_pmac_str.assert_has_calls(
        [
            call(expected_xmove, wait=True, timeout=10),
            call(expected_ymove, wait=True, timeout=10),
        ]
    )


@patch("mx_bluesky.i24.serial.fixed_target.i24ssx_moveonclick.cv")
@patch("mx_bluesky.i24.serial.fixed_target.i24ssx_moveonclick._get_beam_centre")
def test_update_ui_uses_correct_beam_centre_for_ellipse(fake_beam_pos, fake_cv):
    mock_frame = MagicMock()
    mock_oav = MagicMock()
    fake_beam_pos.side_effect = [(15, 10)]
    update_ui(mock_oav, mock_frame)
    fake_cv.ellipse.assert_called_once()
    fake_cv.ellipse.assert_has_calls(
        [call(ANY, (15, 10), (12, 8), 0.0, 0.0, 360, (0, 255, 255), thickness=2)]
    )
