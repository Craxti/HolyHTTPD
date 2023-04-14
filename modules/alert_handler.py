import json
import logging
import threading
import subprocess

# Чтение конфигурационного файла
with open('config.json') as f:
    config = json.load(f)

# Настройка логгера
logging.basicConfig(filename='logs/alerts.log', level=logging.INFO)


def alert_handler():
    # Обработка оповещений
    while True:
        alert = config['alert_queue'].get()
        logging.info('Received alert for IP %s', alert)
        # Добавить обработку оповещения
        t = threading.Thread(target=handle_alert, args=(alert,))
        t.start()


def handle_alert(alert):
    # Обработка оповещения
    try:
        # Добавить обработку оповещения
        # Например, запуск Suricata или Snort для дополнительного анализа
        subprocess.run(
            ['suricata', '-c', '/etc/suricata/suricata.yaml', '-r', alert])
        logging.info('Processed alert for IP %s', alert)
    except BaseException:
        logging.warning('Error processing alert for IP %s', alert)


if __name__ == '__main__':
    t = threading.Thread(target=alert_handler)
    t.start()
