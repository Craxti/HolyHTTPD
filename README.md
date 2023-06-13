**Fake Server**

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

This is a Python-based fake web server designed to be used as a honeypot or decoy server for catching attackers or search engine bots. The server listens on a user-defined port and logs all incoming requests to a CSV file.

You can install these packages using pip with the provided requirements.txt file.

`pip install -r requirements.txt`

**Usage**

To start the fake web server, run the following command:

`python main.py`

This will start the server on the default port 8080. If you want to use a different port, specify it as a command-line argument:

`python main.py --port 1234`

The server logs all incoming requests to a CSV file named access.log, which is located in the same directory as the main script. You can view the log file using any text editor or spreadsheet application.

In addition to logging requests, the server can also capture and analyze network traffic using Suricata and PyShark. To enable this feature, install Suricata and PyShark and set the ENABLE_NETWORK_CAPTURE configuration option to True in config.yaml.

**Configuration**

The server can be configured using the config.yaml file. Here are the available configuration options:

- `port`: The port number to listen on (default: 8080).

- `enable_logging`: Whether to enable logging of incoming requests (default: True).

- `log_file`: The name of the file to write access logs to (default: access.log).

- `alert_queue`: The name of the directory to store alert files in (default: queue/alerts).

- `pcap_queue`: The name of the directory to store pcap files in (default: queue/pcap).

- `enable_network_capture`: Whether to enable capturing and analyzing network traffic (default: False).

- `suricata_path`: The path to the Suricata binary (default: suricata).

- `suricata_rules_path`: The path to the directory containing Suricata rules (default: rules).

- `packet_capture_duration`: The duration of each packet capture (in seconds) (default: 10).
