#!/bin/bash

# Install required packages
pip install -r requirements.txt

# Download Suricata rules
suricata-update enable-source oisf/trafficid
suricata-update enable-source sslbl/ja3-fingerprints
suricata-update enable-source tgreen/hunting
suricata-update

# Create directories for storing pcap files and alerts
mkdir -p queue/pcap
mkdir -p queue/alerts
