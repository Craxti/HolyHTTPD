import json
import logging
import threading
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Read config file
with open("config.json") as f:
    config = json.load(f)

# Settings logs
logging.basicConfig(filename="logs/alerts.log", level=logging.INFO)

# Очередь для обработки алертов
alert_queue = config["alert_queue"]
alert_threads_num = config["alert_threads_num"]


def alert_handler(alert_file):
    # handler alert
    with open(alert_file) as file_l:
        alert = json.load(file_l)

    alert_id = alert["id"]
    alert_time = datetime.fromtimestamp(alert["timestamp"]).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    alert_msg = alert["message"]
    alert_src_ip = alert["src_ip"]
    alert_dst_ip = alert["dst_ip"]
    alert_protocol = alert["protocol"]
    alert_port = alert["port"]

    # Format message for log file
    log_msg = (
        f"ALERT ID: {alert_id}\n"
        f"TIME: {alert_time}\n"
        f"MESSAGE: {alert_msg}\n"
        f"SOURCE IP: {alert_src_ip}\n"
        f"DESTINATION IP: {alert_dst_ip}\n"
        f"PROTOCOL: {alert_protocol}\n"
        f"PORT: {alert_port}\n"
    )

    logging.info(log_msg)

    # Обработка алерта может занять длительное время,
    # поэтому запускаем ее в отдельном потоке
    t = threading.Thread(target=process_alert, args=(alert,))
    t.start()


import smtplib
from email.mime.text import MIMEText

def process_alert(alert):
    email_subject = "ALERT: {id}".format(id=alert["id"])
    email_body = """
        Alert ID: {id}
        Time: {time}
        Message: {message}
        Source IP: {src_ip}
        Destination IP: {dst_ip}
        Protocol: {protocol}
        Port: {port}
    """.format(
        id=alert["id"],
        time=datetime.fromtimestamp(alert["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
        message=alert["message"],
        src_ip=alert["src_ip"],
        dst_ip=alert["dst_ip"],
        protocol=alert["protocol"],
        port=alert["port"],
    )

    smtp_server = "your_smtp_server"
    smtp_port = 587
    smtp_username = "your_username"
    smtp_password = "your_password"
    sender_email = "sender@example.com"
    recipient_email = "recipient@example.com"

    try:
        # Создаем объект MIMEText с телом письма
        message = MIMEText(email_body)
        message["Subject"] = email_subject
        message["From"] = sender_email
        message["To"] = recipient_email

        # Отправляем письмо через SMTP сервер
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)

        # alery add db
        # database.insert(alert)
    except Exception as e:
        logging.warning("Error processing alert: %s", str(e))



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
