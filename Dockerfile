# Start with your base image
FROM apache/airflow:2.10.2

# Set working directory
WORKDIR /opt/airflow

USER root
# Install Docker client
RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Create docker group if it doesn't exist
RUN groupadd -g 999 docker || true

# Add airflow user to docker group
RUN usermod -aG docker airflow
RUN usermod -aG docker root

# Set permissions for Docker socket
RUN chmod 666 /var/run/docker.sock || true

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir ./image-python ./load-csv ./summary-output ./data

COPY ./image-python/example.py /opt/airflow/image-python/example.py
COPY ./data /opt/airflow/data
COPY ./load-csv/load_to_db.py /opt/airflow/load-csv/load_to_db.py
COPY ./summary-output/summary_output.py /opt/airflow/summary-output/summary_output.py


RUN chmod -R 777 /opt/airflow && chown -R airflow:root /opt/airflow

USER airflow
# Make sure Python is available in PATH
ENV PATH="/usr/local/bin:${PATH}"
# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
