import json
import logging
import threading
from datetime import datetime

# Read config file
with open('config.json') as f:
    config = json.load(f)

# Settings logs
logging.basicConfig(filename='logs/alerts.log', level=logging.INFO)

# Очередь для обработки алертов
alert_queue = config['alert_queue']
alert_threads_num = config['alert_threads_num']


def alert_handler(alert_file):
    # handler alert
    with open(alert_file) as file_l:
        alert = json.load(file_l)

    alert_id = alert['id']
    alert_time = datetime.fromtimestamp(alert['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    alert_msg = alert['message']
    alert_src_ip = alert['src_ip']
    alert_dst_ip = alert['dst_ip']
    alert_protocol = alert['protocol']
    alert_port = alert['port']

    # Format message for log file
    log_msg = f"ALERT ID: {alert_id}\n" \
              f"TIME: {alert_time}\n" \
              f"MESSAGE: {alert_msg}\n" \
              f"SOURCE IP: {alert_src_ip}\n" \
              f"DESTINATION IP: {alert_dst_ip}\n" \
              f"PROTOCOL: {alert_protocol}\n" \
              f"PORT: {alert_port}\n"

    logging.info(log_msg)

    # Обработка алерта может занять длительное время,
    # поэтому запускаем ее в отдельном потоке
    t = threading.Thread(target=process_alert, args=(alert,))
    t.start()


def process_alert(alert):
    # Здесь происходит обработка алерта
    # Например, отправка уведомления на почту
    # Или добавление информации об алерте в базу данных
    pass


def start_alert_handlers():
    # run hendlers alert
    for i in range(alert_threads_num):
        t = threading.Thread(target=alert_handler_loop)
        t.start()


def alert_handler_loop():
    while True:
        alert_file = alert_queue.get()
        alert_handler(alert_file)
        alert_queue.task_done()