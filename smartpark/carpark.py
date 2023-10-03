from datetime import datetime

import mqtt_device
import paho.mqtt.client as paho
from paho.mqtt.client import MQTTMessage


class CarPark(mqtt_device.MqttDevice):
    """Creates a carpark object to store the state of cars in the lot"""

    def __init__(self, config):
        super().__init__(config)
        self.total_spaces = config['total-spaces']
        self.total_cars = config['total-cars']
        self.client.on_message = self.on_message
        self.client.subscribe('sensor')
        self.client.loop_forever()
        self._temperature = None

    @property
    def available_spaces(self):
        available = self.total_spaces - self.total_cars
        return max(available, 0)

    @property
    def temperature(self):
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        self._temperature = value
        
    def _publish_event(self):
        readable_time = datetime.now().strftime('%H:%M:%S')
        print(
            (
                f"TIME: {readable_time}, "
                + f"SPACES: {self.available_spaces}, "
                + f"TEMPC: {self.temperature}"
            )
        )
        message = (
            f"TIME: {readable_time}, "
            + f"SPACES: {self.available_spaces}, "
            + f"TEMPC: {self.temperature}"
        )

        # msg_str = f"{readable_time};{self.available_spaces};{self.temperature}"  # "<time>;<spaces>;<temperature>"
        msg_str = f"{self.available_spaces};{self.temperature};{readable_time}"  # "<spaces>;<temperature>;<time>"

        self.client.publish('display', msg_str)

    def on_car_entry(self):
        self.total_cars += 1

        if self.total_cars >= self.total_spaces:
            self.total_cars = self.total_spaces

        self._publish_event()

    def on_car_exit(self):
        self.total_cars -= 1

        if self.total_cars < 0:
            self.total_cars = 0

        self._publish_event()

    def on_message(self, client, userdata, msg: MQTTMessage):
        payload = msg.payload.decode()
        # TODO: Extract temperature from payload
        # self.temperature = ... # Extracted value
        entry_or_exit = payload.split(",")[0]
        self.temperature = payload.split(",")[1]
        if entry_or_exit == "Entry":
            self.on_car_entry()
        elif entry_or_exit == "Exit":
            self.on_car_exit()
        else:
            exit()  # To close carpark.py as a background process (daemon thread)


if __name__ == '__main__':
    config = {'name': "raf-park",
              'total-spaces': 130,
              'total-cars': 0,
              'location': 'L306',
              'topic-root': "lot",
              'broker': 'localhost',
              'port': 1883,
              'topic-qualifier': 'entry',
              'is_stuff': False
              }
    # TODO: Read config from file
    car_park = CarPark(config)
    print("Carpark initialized")
    print("Carpark initialized")
