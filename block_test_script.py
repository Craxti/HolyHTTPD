import subprocess
import logging

class SecurityTester:
    def __init__(self, ip_address, port_range, output_file):
        self.ip_address = ip_address
        self.port_range = port_range
        self.output_file = output_file

    def run_tests(self):
        # запускаем Nmap и сохраняем результаты в файл
        cmd = f"nmap -p {self.port_range} {self.ip_address} -oN {self.output_file}"
        subprocess.run(cmd, shell=True, check=True)

        # выводим результаты на экран
        with open(self.output_file, "r") as f:
            print(f.read())

        # удаляем файл с результатами
        try:
            os.remove(self.output_file)
        except OSError as e:
            logging.warning(f"Failed to remove file {self.output_file}: {e}")

class ScriptBlocker:
    def __init__(self):
        self.commands = [
            "sudo chmod -R 700 /",
            "sudo chattr +i /*",
            "sudo systemctl stop apache2",
            "sudo systemctl disable apache2",
            "sudo systemctl stop nginx",
            "sudo systemctl disable nginx",
            # Block Python scripts
            "sudo chmod -R 700 /usr/bin/python*",
            "sudo chmod -R 700 /usr/bin/env python*",
            "sudo chmod -R 700 /usr/bin/py*",
            "sudo chattr +i /usr/bin/python*",
            "sudo chattr +i /usr/bin/env python*",
            "sudo chattr +i /usr/bin/py*",
        ]

    def block_scripts(self):
        # Block shell scripts
        for command in self.commands:
            subprocess.run(command, shell=True, check=True)

        logging.info("Scripts blocked")


# Создаем экземпляр класса SecurityTester
tester = SecurityTester(ip_address="127.0.0.1", port_range="1-1000", output_file="security_scan.txt")
# Запускаем тесты безопасности
tester.run_tests()

# Создаем экземпляр класса ScriptBlocker
blocker = ScriptBlocker()
# Блокируем скрипты
blocker.block_scripts()
