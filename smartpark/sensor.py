""""Demonstrates a simple implementation of an 'event' listener that triggers
a publication via mqtt"""
import random
import threading
import time
import tkinter as tk
from typing import Iterable
import mqtt_device


class Sensor(mqtt_device.MqttDevice):

    @property
    def temperature(self):
        """Returns the current temperature"""
        return random.randint(10, 35) 

    def on_detection(self, message):
        """Triggered when a detection occurs"""
        self.client.publish('sensor', message)

    def start_sensing(self):
        """ A blocking event loop that waits for detection events, in this
        case Enter presses"""
        while True:
            print("Press E when 🚗 entered!")
            print("Press X when 🚖 exited!")
            detection = input("E or X> ").upper()
            if detection == 'E':
                self.on_detection(f"entered, {self.temperature}")
            else:
                self.on_detection(f"exited, {self.temperature}")

class CarDetector:
    """Provides a couple of simple buttons that can be used to represent a sensor detecting a car. This is a skeleton only."""

    def __init__(self, config):
        self.root = tk.Tk()
        self.root.title("Car Detector ULTRA")

        self.btn_incoming_car = tk.Button(
            self.root, text='🚘 Incoming Car', font=('Arial', 50), cursor='right_side', command=self.incoming_car)
        self.btn_incoming_car.pack(padx=10, pady=5)
        self.btn_outgoing_car = tk.Button(
            self.root, text='Outgoing Car 🚘',  font=('Arial', 50), cursor='bottom_left_corner', command=self.outgoing_car)
        self.btn_outgoing_car.pack(padx=10, pady=5)

        self.sensor = Sensor(config)

        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        self.root.mainloop()

    def incoming_car(self):
        # implement this method to publish the detection via MQTT
        # TODO: Send message to CarPark subscriber
        message = (self.sensor.temperature, "Entry")
        self.sensor.on_detection(f"Entry,{self.sensor.temperature}")
        print("Car goes in")

    def on_window_close(self):
        self.sensor.on_detection(f"Quit,{self.sensor.temperature}")
        self.root.destroy()

    def outgoing_car(self):
        # implement this method to publish the detection via MQTT
        # TODO: Send message to CarPark subscriber
        message = (self.sensor.temperature, "Exit")
        self.sensor.on_detection(f"Exit,{self.sensor.temperature}")
        print("Car goes out")


if __name__ == '__main__':
    config1 = {'name': 'sensor',
              'location': 'moondalup',
              'topic-root': "lot",
              'topic-qualifier': "na",
              'broker': 'localhost',
              'port': 1883,
              }
    # # TODO: Read previous config from file instead of embedding
    #
    # sensor1 = Sensor(config1)
    # print("Sensor initialized")
    # sensor1.start_sensing()
    # sensor1.start_sensing()

    CarDetector(config1)

