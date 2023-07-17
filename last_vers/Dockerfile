# Base image
FROM python:3.9-slim-buster

# Create a working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && \
    apt-get install -y libpcap-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y libpcap-dev && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Copy the source code
COPY . .

# Expose the port that the app will run on
EXPOSE 5000

# Run the app
CMD [ "python", "server.py" ]
