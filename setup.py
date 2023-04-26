from setuptools import setup, find_packages

setup(
    name='fake-server',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fake-server = main:main',
        ],
    },
    install_requires=[
        'Flask==2.1.0',
        'flake8',
        'pandas==1.3.4',
        'psutil==5.8.0',
        'pyshark==0.4.3.0',
        'scapy==2.4.5',
        'Suricata==6.0.3',
        'tldextract==3.1.0',
    ],
)
