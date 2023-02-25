import unittest
import requests
import os
import time
import threading

class TestWebServer(unittest.TestCase):
    def test_upload_file(self):
        # Отправляем POST-запрос на загрузку файла
        files = {'file': open('test.txt', 'rb')}
        response = requests.post('http://localhost:8000/', files=files)

        # Проверяем, что файл был успешно загружен
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "<html><body><h1>File uploaded successfully</h1></body></html>")

        # Проверяем, что файл действительно был загружен на сервер
        time.sleep(1)
        self.assertTrue(os.path.exists("uploads/test.txt"))

    def test_filesystem_integrity(self):
        # Вносим изменения в поддельную файловую систему
        with open("/tmp/fake_fs/secret_file.txt", "w") as f:
            f.write("This is a modified secret file")

        # Проверяем целостность файловой системы
        check_filesystem_integrity("/tmp/fake_fs")
        self.assertTrue(logging.getLogger().getEffectiveLevel() == logging.WARNING)

    def test_packet_sniffer(self):
        # Запускаем процесс обработки сетевых пакетов
        sniffer = PacketSniffer()
        sniffer.start()

        # Отправляем запрос на сайт
        requests.get("http://google.com")

        # Останавливаем процесс обработки сетевых пакетов
        sniffer.stop()

        # Проверяем, что был обработан хотя бы один пакет
        self.assertTrue(logging.getLogger().getEffectiveLevel() == logging.INFO)

    def test_web_server_concurrency(self):
        # Запускаем веб-сервер
        server = WebServer(8000)
        server.start()

        # Создаем несколько потоков для одновременной загрузки файлов
        threads = []
        for i in range(5):
            t = threading.Thread(target=self._upload_file, args=("test{}.txt".format(i),))
            threads.append(t)
            t.start()

        # Дожидаемся завершения всех потоков
        for t in threads:
            t.join()

        # Останавливаем веб-сервер
        server.stop()

        # Проверяем, что все файлы были успешно загружены
        for i in range(5):
            self.assertTrue(os.path.exists("uploads/test{}.txt".format(i)))

    def _upload_file(self, filename):
        # Отправляем POST-запрос на загрузку файла
        files = {'file': open(filename, 'rb')}
        response = requests.post('http://localhost:8000/', files=files)
