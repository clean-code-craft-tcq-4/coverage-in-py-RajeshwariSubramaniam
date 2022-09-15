import io
import sys
import unittest
from unittest.mock import patch, MagicMock

from src.typewise_alert import (
    classify_temperature_breach,
    check_and_alert,
    send_to_controller,
    send_to_email
)


class TypeWiseAlertTest(unittest.TestCase):

    def test_classify_temperature_and_infer_breach(self):
        self.assertEqual('TOO_HIGH', classify_temperature_breach('PASSIVE_COOLING', 40))
        self.assertEqual('TOO_LOW', classify_temperature_breach('HI_ACTIVE_COOLING', -1))
        self.assertEqual('NORMAL', classify_temperature_breach('MED_ACTIVE_COOLING', 35))

    def test_check_and_alert(self):
        with patch("src.typewise_alert.classify_temperature_breach", retrun_value='TOO_LOW'):
            with patch("src.typewise_alert.send_to_controller") as mock_to_controller:
                check_and_alert('TO_CONTROLLER', MagicMock(), -15)
            mock_to_controller.assert_called()
            with patch("src.typewise_alert.send_to_email") as mock_to_email:
                check_and_alert('TO_EMAIL', MagicMock(), -15)
            mock_to_email.assert_called()

    def test_send_to_controller(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        send_to_controller('TOO_LOW')
        console_output = capturedOutput.getvalue()
        self.assertTrue(console_output.index('TOO_LOW'))

    def test_send_to_email(self):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        send_to_email('TOO_HIGH')
        console_output = capturedOutput.getvalue()
        self.assertTrue(console_output.index('the temperature is too high'))
        send_to_email('TOO_LOW')
        console_output = capturedOutput.getvalue()
        self.assertTrue(console_output.index('the temperature is too low'))


if __name__ == '__main__':
    unittest.main()
