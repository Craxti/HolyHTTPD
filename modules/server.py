import json
import logging
import threading
from flask import Flask, request

app = Flask(__name__)

# Чтение конфигурационного файла
with open('config.json') as f:
    config = json.load(f)

# Настройка логгера
logging.basicConfig(filename='logs/access.log', level=logging.INFO)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        logging.info('Received POST request from %s', request.remote_addr)
        # Обработка POST-запроса
        t = threading.Thread(target=handle_post_request, args=(request,))
        t.start()
        return 'OK', 200

    logging.warning('Received GET request from %s', request.remote_addr)
    # Обработка GET-запроса
    t = threading.Thread(target=handle_get_request, args=(request,))
    t.start()
    return '', 200


def handle_post_request(request):
    # Обработка POST-запроса
    try:
        data = request.get_json()
        # Добавить обработку полученных данных
        logging.info('Processed POST request from %s', request.remote_addr)
    except BaseException:
        logging.warning(
            'Error processing POST request from %s',
            request.remote_addr)


def handle_get_request(request):
    # Обработка GET-запроса
    try:
        # Добавить обработку полученных данных
        logging.info('Processed GET request from %s', request.remote_addr)
    except BaseException:
        logging.warning(
            'Error processing GET request from %s',
            request.remote_addr)


if __name__ == '__main__':
    app.run(debug=config['debug'], host=config['host'], port=config['port'])
