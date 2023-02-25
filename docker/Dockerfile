FROM python:3.8
LABEL maintainer="your_name"

RUN apt-get update && apt-get install -y tcpdump

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]