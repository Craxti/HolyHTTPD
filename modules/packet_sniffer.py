import logging
import queue
import threading
from pcap_parser import pcap_parser

from scapy.all import sniff

logging.basicConfig(filename='logs/packet_sniffer.log', level=logging.INFO)


class PacketSniffer:
    def __init__(self, pcap_queue, *args):
        self.pcap_queue = pcap_queue
        self.sniffing_thread = None

    def start_sniffing(self, interface=None, filter=None):
        if self.sniffing_thread is None or not self.sniffing_thread.is_alive():
            self.sniffing_thread = threading.Thread(
                target=self._sniff, args=(interface, filter))
            self.sniffing_thread.start()
            logging.info("Packet sniffing started")

    def start(self):
        # создать очередь
        pcap_queue = queue.Queue()

        # добавить элементы в очередь
        pcap_queue.put('pcap/capture.pcap')

        # передать очередь в config
        config = {'pcap_queue': pcap_queue}

        # получить элементы из очереди
        pcap_file = config['pcap_queue'].get()
        logging.info('Received pcap file %s', pcap_file)

        # Добавить обработку pcap-файла
        t = threading.Thread(target=pcap_parser, args=(pcap_file, pcap_queue,))
        t.start()

    def stop_sniffing(self):
        if self.sniffing_thread is not None and self.sniffing_thread.is_alive():
            self.sniffing_thread.do_run = False
            self.sniffing_thread.join()
            logging.info("Packet sniffing stopped")

    def _process_packet(self, packet):
        self.pcap_queue.put(packet)

    def _sniff(self, interface=None, filter=None):
        try:
            self.sniffing_thread.do_run = True
        except AttributeError:
            self.sniffing_thread = threading.currentThread()
            self.sniffing_thread.do_run = True

        sniff(iface=interface, filter=filter, prn=self._process_packet,
              stop_filter=lambda _: not self.sniffing_thread.do_run)
