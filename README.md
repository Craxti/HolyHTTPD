Fake Web Server

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

This is a simple web server implemented in Python that is designed to be used as a honeypot or a fake server to catch attackers or crawlers. It has the following features:

• It listens on port 80 for incoming HTTP requests.
• It serves a simple HTML page that displays a message when a request is made to the server.
• It writes information about the request to a log file.
• It can be configured to run on any port.
• It has a packet sniffer that can detect network attacks.


Installation

Clone the repository:

```git clone https://github.com/<username>/<repository>.git```

Install the dependencies:


```pip install -r requirements.txt`````

Start the fake file system:

```python main.py --create-fake-fs```

Start the packet sniffer:

```python main.py --start-packet-sniffer```

Start the fake web server:

```python main.py --start-web-server --port 80```


Configuration
The following configuration options are available:

• create-fake-fs: Creates a fake file system with the following parameters:
  fake_fs_path (default: /tmp/fake_fs): The path where the fake file system will be created.
  fake_fs_files (default: {"secret_file.txt": "This is a secret file", "public_file.txt": "This is a public file"}): The files that will be created in the fake file system.
• start-packet-sniffer: Starts the packet sniffer.
• start-web-server: Starts the web server with the following parameters:
•port (default: 80): The port on which the web server will listen.

License
 This project is licensed under the MIT License - see the LICENSE file for details.