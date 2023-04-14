import json
import logging
import os
import queue
import shutil
import subprocess
import threading
import time
import urllib.parse

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

import scapy.all as scapy
import pyshark

from modules.alert_handler import alert_handler
from modules.packet_sniffer import PacketSniffer
from modules.pcap_parser import pcap_parser


# Чтение конфигурационного файла
with open('config.json') as f:
    config = json.load(f)

# Настройка логгера
logging.basicConfig(filename='logs/main.log', level=logging.INFO)

# Очередь для обработки файлов pcap
pcap_queue = queue.Queue()

# Очередь для обработки алертов
alert_queue = queue.Queue()

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        logging.info('Received GET request from %s', self.client_address[0])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, World!')

        # Обработка GET-запроса
        t = threading.Thread(target=handle_get_request, args=(self.requestline,))
        t.start()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        logging.info('Received POST request from %s', self.client_address[0])
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST request received')

        # Обработка POST-запроса
        t = threading.Thread(target=handle_post_request, args=(body,))
        t.start()


def handle_get_request(request):
    # Обработка GET-запроса
    # Например, добавление данных в базу данных
    logging.info('Processed GET request: %s', request)


def handle_post_request(request):
    # Обработка POST-запроса
    # Например, сохранение данных в файл
    logging.info('Processed POST request: %s', request)


def start_server():
    # Запуск веб-сервера
    server = ThreadingSimpleServer(('', config['port']), RequestHandler)
    server.serve_forever()


def start_alert_handler():
    # Запуск обработчика алертов
    while True:
        alert_file = alert_queue.get()
        logging.info('Received alert file %s', alert_file)
        # Обработать алерт
        t = threading.Thread(target=alert_handler, args=(alert_file,))
        t.start()


def start_pcap_parser():
    # Запуск парсера pcap-файлов
    while True:
        pcap_file = pcap_queue.get()
        logging.info('Received pcap file %s', pcap_file)
        # Обработать pcap-файл
        t = threading.Thread(target=pcap_parser, args=(pcap_file,))
        t.start()


if __name__ == '__main__':
    # Создание директорий для логов и очередей
    os.makedirs('logs', exist_ok=True)
    os.makedirs('queue', exist_ok=True)

    # Запуск веб-сервера
    t_server = threading.Thread(target=start_server)

    # Запуск обработчика алертов
    t_alert_handler = threading.Thread(target=start_alert_handler)
    t_alert_handler.start()

    # Запуск парсера pcap-файлов
    t_pcap_parser = threading.Thread(target=start_pcap_parser)
    t_pcap_parser.start()

    # Запуск сниффера сетевых пакетов
    packet_sniffer = PacketSniffer(pcap_queue, alert_queue, True)
    packet_sniffer.start()

    # Бесконечный цикл для обработки файлов из директории очереди
    while True:
        # Получение списка файлов из директории очереди
        files = os.listdir('queue')
        for file in files:
            file_path = os.path.join('queue', file)
            # Определение типа файла (алерт или pcap)
            if file.endswith('.json'):
                config['alert_queue'].put(file_path)
            elif file.endswith('.pcap'):
                pcap_queue.put(file_path)
            # Удаление обработанного файла из очереди
            os.remove(file_path)
        time.sleep(1)