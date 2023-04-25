import json
import logging
import threading
import pyshark
import queue

# Чтение конфигурационного файла
with open('config.json') as f:
    config = json.load(f)

# Настройка логгера
logging.basicConfig(filename='logs/pcap.log', level=logging.INFO)


def pcap_parser(pcap_queue):
    # Обработка файлов pcap
    while True:
        pcap_file = pcap_queue.get()
        logging.info('Received pcap file %s', pcap_file)
        # Добавить обработку pcap-файла
        t = threading.Thread(target=handle_pcap_file, args=(pcap_file,))
        t.start()



def handle_pcap_file(pcap_file):
    # Обработка pcap-файла
    try:
        # Использование PyShark для чтения pcap-файла
        cap = pyshark.FileCapture(pcap_file)
        for packet in cap:
            # Обработка захваченного пакета
            # Например, добавление пакета в базу данных
            logging.info('Processed packet from %s', packet.ip.src)
        cap.close()
        logging.info('Processed pcap file %s', pcap_file)
    except BaseException:
        logging.warning('Error processing pcap file %s', pcap_file)


t = threading.Thread(target=pcap_parser)
t.start()
