@echo off

rem Install required packages
pip install -r requirements.txt

rem Download Suricata rules
suricata-update enable-source oisf/trafficid
suricata-update enable-source sslbl/ja3-fingerprints
suricata-update enable-source tgreen/hunting
suricata-update

rem Create directories for storing pcap files and alerts
mkdir queue\pcap
mkdir queue\alerts
