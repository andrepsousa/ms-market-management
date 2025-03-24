FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    gcc \
    iputils-ping \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
