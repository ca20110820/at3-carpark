FROM python:slim-bullseye

WORKDIR /at3
COPY . /at3

# Install MQTT Mosquitto
RUN apt-get update && apt-get install -y mosquitto mosquitto-clients
# Run MQTT Mosquitto
EXPOSE 1883
CMD ["mosquitto", "-c", "/etc/mosquitto/mosquitto.conf", "&&"]

CMD ["python3", "/at3/setup.py", "install"]

RUN python3 smartpark
