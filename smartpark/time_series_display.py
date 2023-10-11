import sys
import threading
from datetime import datetime
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource

from smartpark.mqtt_device import MqttDevice


QUIT_FLAG = False


class TimeSeriesDisplay(MqttDevice):
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')
        self.client.subscribe('quit')

        thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        thread.start()

        self.data = None

    def on_message(self, client, userdata, msg):
        global QUIT_FLAG

        if msg.topic != "quit":
            data = msg.payload.decode()  #
            data = data.split(';')  # List[str] - ["<spaces>","<temperature>","<time>"]
            if data[0] == "Full":
                data[0] = 0
            else:
                data[0] = int(data[0])

            data[1] = float(data[1])

            data[2] = datetime.now()

            print(self.data)
            self.data = [data[0], data[1], data[2]]

        elif msg.topic == "quit":
            QUIT_FLAG = True


config = {"name": "time-series-display",
          "location": "moondaloop",
          "topic-root": "lot",
          "topic-qualifier": "na",
          "broker": "localhost",
          "port": 1883
          }
ts_display = TimeSeriesDisplay(config)

source = ColumnDataSource(data={"Time": [], "Available Spaces": [], "Temperature": []})

plot_spaces = figure(height=300, width=800, x_axis_type="datetime", title="Available Spaces")
plot_spaces.line(x="Time", y="Available Spaces", source=source)

plot_temperature = figure(height=300, width=800, x_axis_type="datetime", title="Temperature")
plot_temperature.line(x="Time", y="Temperature", source=source)


def update():
    if QUIT_FLAG:
        exit()

    if ts_display.data is not None:
        source.stream({"Time": [ts_display.data[2]],
                       "Available Spaces": [ts_display.data[0]],
                       "Temperature": [ts_display.data[1]]},
                      rollover=5000)


curdoc().add_root(plot_spaces)
curdoc().add_root(plot_temperature)
curdoc().add_periodic_callback(update, 50)
