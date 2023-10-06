FROM python:slim-bullseye

WORKDIR /at3
COPY . /at3

RUN python3 /at3/setup.py install

# Install MQTT Mosquitto
RUN apt-get update \
    && apt-get install -y mosquitto mosquitto-clients \
    && mosquitto -c /etc/mosquitto/mosquitto.conf &&

# Run MQTT Mosquitto
EXPOSE 1883

CMD ["python3", "/at3/smartpark"]
