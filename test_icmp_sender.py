import unittest
from unittest.mock import Mock, MagicMock
from icmp_sender import validate_inputs, send_probes

class ProbeTests(unittest.TestCase):
    def test_valid_inputs(self):
        self.assertEqual(validate_inputs('192.0.2.1', '192.0.2.2', '2')[2], 2)

    def test_rejects_invalid_addresses(self):
        for address in ('bad', '::1', '224.0.0.1', '0.0.0.0'):
            with self.subTest(address=address), self.assertRaises(ValueError):
                validate_inputs(address, '192.0.2.2', 1)

    def test_rejects_unbounded_count(self):
        for count in (0, -1, 11, 1000000):
            with self.subTest(count=count), self.assertRaises(ValueError):
                validate_inputs('192.0.2.1', '192.0.2.2', count)

    def test_timeout_and_spacing(self):
        send = Mock(return_value=None)
        pause = Mock()
        ip, icmp = MagicMock(), MagicMock()
        self.assertEqual(send_probes('192.0.2.1', '192.0.2.2', 2, send, ip, icmp, pause), 0)
        self.assertEqual(send.call_count, 2)
        self.assertEqual(send.call_args.kwargs['timeout'], 2)
        pause.assert_called_once_with(1)

    def test_invalid_input_sends_nothing(self):
        send = Mock()
        with self.assertRaises(ValueError):
            send_probes('192.0.2.1', '192.0.2.2', 100, send, Mock(), Mock())
        send.assert_not_called()
