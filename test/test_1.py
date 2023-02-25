import unittest
import os
import shutil
import tempfile
import threading
import time
import subprocess
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from unittest.mock import patch, MagicMock

import scapy.all as scapy
import pyshark

import main

class TestFakeFileSystem(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.fs = main.FakeFileSystem(self.tempdir.name, main.fake_fs_files)

    def tearDown(self):
        self.fs.remove()
        self.tempdir.cleanup()

    def test_create(self):
        self.fs.create()
        for filename, content in main.fake_fs_files.items():
            with open(os.path.join(self.tempdir.name, filename), "r") as f:
                self.assertEqual(f.read(), content)

    def test_remove(self):
        self.fs.create()
        self.fs.remove()
        self.assertFalse(os.path.exists(self.tempdir.name))

class TestWebServer(unittest.TestCase):

    def setUp(self):
        self.port = 8080
        self.server = main.WebServer(self.port)

    def tearDown(self):
        self.server.stop()

    def test_start(self):
        self.server.start()
        self.assertTrue(self.server.running)
        # Wait for server to start listening
        time.sleep(1)
        response = requests.get(f"http://localhost:{self.port}")
        self.assertEqual(response.status_code, 404)

    def test_stop(self):
        self.server.start()
        self.server.stop()
        self.assertFalse(self.server.running)

class TestPacketSniffer(unittest.TestCase):

    def setUp(self):
        self.sniffer = main.PacketSniffer()

    def tearDown(self):
        self.sniffer.stop()

    @patch('main.logging.info')
    def test_packet_callback(self, mock_logging):
        packet = MagicMock()
        packet.summary.return_value = "This is a test packet"
        self.sniffer.packet_callback(packet)
        mock_logging.assert_called_once_with("Packet received: %s", "This is a test packet")

    def test_start(self):
        self.sniffer.start()
        self.assertTrue(self.sniffer.running)
        time.sleep(1)
        self.sniffer.stop()

    def test_stop(self):
        self.sniffer.start()
        self.sniffer.stop()
        self.assertFalse(self.sniffer.running)

if __name__ == '__main__':
    unittest.main()
