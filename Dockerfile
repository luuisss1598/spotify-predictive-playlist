# pull base image for airflow
FROM apache/airflow:2.10.5

# copy and install pacakages using requirements.txt for easier installation 
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt 

# copy setup files for local custom packages, create initial folder to install local packages
COPY setup.py /opt/airflow/
RUN mkdir -p /opt/airflow/src
RUN pip install -e .