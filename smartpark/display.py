import mqtt_device
import time

import random
import threading
import tkinter as tk
from typing import Iterable


class WindowedDisplay:
    """Displays values for a given set of fields as a simple GUI window. Use .show() to display the window; use .update() to update the values displayed.
    """

    DISPLAY_INIT = '– – –'
    SEP = ':'  # field name separator

    def __init__(self, title: str, display_fields: Iterable[str]):
        """Creates a Windowed (tkinter) display to replace sense_hat display. To show the display (blocking) call .show() on the returned object.

        Parameters
        ----------
        title : str
            The title of the window (usually the name of your carpark from the config)
        display_fields : Iterable
            An iterable (usually a list) of field names for the UI. Updates to values must be presented in a dictionary with these values as keys.
        """
        self.window = tk.Tk()
        self.window.title(f'{title}: Parking')
        self.window.geometry('800x400')
        self.window.resizable(False, False)
        self.display_fields = display_fields

        self.gui_elements = {}
        for i, field in enumerate(self.display_fields):

            # create the elements
            self.gui_elements[f'lbl_field_{i}'] = tk.Label(
                self.window, text=field+self.SEP, font=('Arial', 50))
            self.gui_elements[f'lbl_value_{i}'] = tk.Label(
                self.window, text=self.DISPLAY_INIT, font=('Arial', 50))

            # position the elements
            self.gui_elements[f'lbl_field_{i}'].grid(
                row=i, column=0, sticky=tk.E, padx=5, pady=5)
            self.gui_elements[f'lbl_value_{i}'].grid(
                row=i, column=2, sticky=tk.W, padx=10)

    def show(self):
        """Display the GUI. Blocking call."""
        self.window.mainloop()

    def update(self, updated_values: dict):
        """Update the values displayed in the GUI. Expects a dictionary with keys matching the field names passed to the constructor."""
        for field in self.gui_elements:
            if field.startswith('lbl_field'):
                field_value = field.replace('field', 'value')
                self.gui_elements[field_value].configure(
                    text=updated_values[self.gui_elements[field].cget('text').rstrip(self.SEP)])
        self.window.update()

class CarParkDisplay(mqtt_device.MqttDevice):
    """Provides a simple display of the car park status. This is a skeleton only. The class is designed to be customizable without requiring and understanding of tkinter or threading."""
    # determines what fields appear in the UI
    fields = ['Available bays', 'Temperature', 'At']

    def __init__(self, inp_config):
        super().__init__(inp_config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.msg_str = None  # Message string to be continuously updated
        # self.client.loop_forever()

        thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        # thread.daemon = True
        thread.start()

        self.window = WindowedDisplay('Moondalup', CarParkDisplay.fields)
        self.window.show()

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()  #
        self.msg_str = data.split(';')  # List[str] - ["<spaces>","<temperature>","<time>"]

        field_values = dict(zip(CarParkDisplay.fields, [
            f'{self.msg_str[0]}',
            f'{self.msg_str[1]}℃',
            f'{self.msg_str[2]}'
        ]))

        # Pretending to wait on updates from MQTT
        # time.sleep(random.randint(1, 10))

        # When you get an update, refresh the display.
        self.window.update(field_values)


if __name__ == '__main__':
    config = {'name': 'display',
     'location': 'L306',
     'topic-root': "lot",
     'broker': 'localhost',
     'port': 1883,
     'topic-qualifier': 'na'
     }
    # TODO: Read config from file

    CarParkDisplay(config)