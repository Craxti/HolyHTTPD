import os
import shutil
import logging
import threading
import subprocess
import scapy.all as scapy
import pyshark
import re


# Fake filesystem options
fake_fs_path = "/tmp/fake_fs"
fake_fs_files = {
    "secret_file.txt": "This is a secret file",
    "public_file.txt": "This is a public file",
}

# Block for DoS-attack
# subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-p', 'tcp', '--dport', '80', '-m', 'limit', '--limit', '10/second', '--limit-burst', '15', '-j', 'ACCEPT'])

# Class for working with a fake file system
class FakeFileSystem:
    def __init__(self, path, files):
        self.path = path
        self.files = files

    # Create a fake filesystem
    def create(self):
        os.makedirs(self.path, exist_ok=True)
        for filename, content in self.files.items():
            with open(os.path.join(self.path, filename), "w") as f:
                f.write(content)
        logging.info("Fake file system created")

    # Removing the fake file system
    def remove(self):
        shutil.rmtree(self.path)
        logging.info("Fake file system removed")


# Class for handling network packets with Scapy
class PacketSniffer:
    def __init__(self):
        self.running = False

    # Packet processing and attack detection
    def packet_callback(self, packet):
        logging.info("Packet received: %s", packet.summary())

    # scan nmap
    def scan_ports_callback(self, packet):
        payload = packet.payload.payload
        if payload and "nmap" in payload.lower():
            logging.warning("Port scanning detected: %s", payload)

    # Start the packet processing process in a separate thread
    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._sniff_packets).start()
            logging.info("Packet sniffer started")

    # Stop the packet processing process
    def stop(self):
        self.running = False
        logging.info("Packet sniffer stopped")

    # Handling network packets with Scapy
    def _sniff_packets(self):
        scapy.sniff(prn=self.packet_callback, filter="tcp port 80")


# Function to record a banner
def write_banner(path, content):
    with open(path, "w") as f:
        f.write(content)
    logging.info("Banner written to %s", path)


# Function to handle file transfer to honeypot
def handle_uploaded_file(file):
    with open(os.path.join("uploads", file.filename), "wb") as f:
        f.write(file.read())
    logging.info("File uploaded: %s", file.filename)


# Function to check the integrity of the file system
def check_filesystem_integrity(path):
    for filename, content in fake_fs_files.items():
        with open(os.path.join(path, filename), "r") as f:
            if f.read() != content:
                logging.warning("File %s has been tampered with", filename)


# Function to protect against SQL injection
def sanitize_sql_input(input_str):
    return input_str.replace("'", "''")


# Settings log
logging.basicConfig(filename="log.txt", level=logging.INFO)

# Create an instance of the class to work with
class Thread:
    def handle_uploaded_file(self, file):
        with open(os.path.join("uploads", file.filename), "wb") as f:
            f.write(file.read())
        logging.info("File uploaded: %s", file.filename)


class PortScanner:
    def __init__(self):
        self.running = False

    def scan_ports(self, host):
        command = f"nmap {host}"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        logging.info("Port scan results:\n%s", output.decode())

    def start(self, host):
        if not self.running:
            self.running = True
            threading.Thread(target=self.scan_ports, args=(host,)).start()
            logging.info("Port scanner started")

    def stop(self):
        self.running = False
        logging.info("Port scanner stopped")


# Command execution function
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        logging.info("Command executed: %s", command)
        return output
    except subprocess.CalledProcessError as e:
        logging.warning("Command failed: %s", command)
        return e.output


# Honeypot command shell
class CommandShell:
    def __init__(self):
        self.prompt = "honeypot$ "

    # Command processing function
    def process_command(self, command):
        if command == "help":
            return (
                "Available commands:\n"
                "help - show this help\n"
                "ls - show contents of the current directory\n"
                "cd [directory] - change the current directory\n"
                "cat [file] - show the contents of a file\n"
                "rm [file] - delete a file\n"
                "rmdir [directory] - delete a directory\n"
                "ps - show running processes\n"
                "kill [pid] - kill a process\n"
                "ifconfig - show network interfaces\n"
                "ping [host] - ping a host\n"
                "curl [url] - download a file from a URL\n"
            )
        elif command == "ls":
            return "\n".join(os.listdir(os.getcwd()))
        elif command.startswith("cd "):
            directory = command[3:]
            if os.path.isdir(directory):
                os.chdir(directory)
                return ""
            else:
                return "cd: %s: No such file or directory" % directory
        elif command.startswith("cat "):
            filename = command[4:]
            if os.path.isfile(filename):
                with open(filename, "r") as f:
                    return f.read()
            else:
                return "cat: %s: No such file or directory" % filename
        elif command.startswith("rm "):
            filename = command[3:]
            if os.path.isfile(filename):
                os.remove(filename)
                return ""
            else:
                return "rm: %s: No such file or directory" % filename
        elif command.startswith("rmdir "):
            directory = command[6:]
            if os.path.isdir(directory):
                shutil.rmtree(directory)
                return ""
            else:
                return "rmdir: %s: No such file or directory" % directory
        elif command == "ps":
            return str(subprocess.check_output("ps aux", shell=True), "utf-8")
        elif command.startswith("kill "):
            pid = command[5:]
            execute_command("kill -9 %s" % pid)
            return ""
        elif command == "ifconfig":
            return str(subprocess.check_output("ifconfig", shell=True), "utf-8")
        elif command.startswith("ping "):
            host = command[5:]
            return execute_command("ping -c 4 %s" % host)
        elif command.startswith("curl "):
            url = command[5:]
            return execute_command("curl %s" % url)
        else:
            return "%s: command not found" % command

    # Honeypot command shell loop
    def shell_loop(self):
        while True:
            command = input(self.prompt)
            output = self.process_command(command.strip())
            print(output)


class LogMonitor:
    def __init__(self, path):
        self.path = path
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.monitor_logs).start()
            logging.info("Log monitor started")

    def stop(self):
        self.running = False
        logging.info("Log monitor stopped")


class LogHandler:
    def process_IN_MODIFY(self, event):
        with open(event.pathname, "r") as f:
            content = f.read()
            if "root" in content:
                logging.warning("Root user accessed %s", event.pathname)
                subprocess.Popen(
                    [
                        "mail",
                        "-s",
                        "Warning: Root user activity detected",
                        "admin@example.com",
                    ],
                    stdin=subprocess.PIPE,
                ).communicate(content.encode())


class WebServer:
    def __init__(self, port):
        self.port = port
        self.running = False

    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self._start_server).start()
            logging.info("Web server started on port %d", self.port)

    def stop(self):
        self.running = False
        logging.info("Web server stopped")

    def _start_server(self):
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import cgi

        class RequestHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        "REQUEST_METHOD": "POST",
                        "CONTENT_TYPE": self.headers["Content-Type"],
                    },
                )

                # Processing the uploaded file
                if "file" in form:
                    thread = Thread()
                    thread.handle_uploaded_file(form["file"])

                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()

                    self.wfile.write(
                        bytes(
                            "<html><body><h1>File uploaded successfully</h1></body></html>",
                            "utf-8",
                        )
                    )
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()

                    self.wfile.write(
                        bytes(
                            "<html><body><h1>Bad request: file not uploaded</h1></body></html>",
                            "utf-8",
                        )
                    )

        httpd = HTTPServer(("", self.port), RequestHandler)
        httpd.serve_forever()


if __name__ == "__main__":
    # init logs
    logging.basicConfig(
        filename="app.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )

    # Creating a Fake File System
    fs = FakeFileSystem(fake_fs_path, fake_fs_files)
    fs.create()
    logging.info("Fake file system created")

    # write banner
    write_banner(os.path.join(fake_fs_path, "banner.txt"), "Welcome to the website!")
    write_banner(
        os.path.join("uploads", "banner.txt"), "This banner was uploaded by a user"
    )
    logging.info("Banners written")

    # run web server
    server = WebServer(8000)
    server.start()
    logging.info("Web server started")

    # Starting a packet sniffing thread
    sniffer = PacketSniffer()
    sniffer.start()
    logging.info("Packet sniffer started")

    # Stopping the web server, sniffer and deleting the fake file system
    server.stop()
    sniffer.stop()
    fs.remove()
    logging.info("Fake file system removed")

    # closed app
    logging.info("Application finished")
