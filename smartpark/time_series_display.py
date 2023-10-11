import threading
import time
from datetime import datetime
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.io import show, push_notebook
from bokeh.driving import linear

from smartpark.mqtt_device import MqttDevice


class TimeSeriesDisplay(MqttDevice):
    def __init__(self, config):
        super().__init__(config)
        self.client.on_message = self.on_message
        self.client.subscribe('display')

        thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        thread.start()

        self.data = None

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode()  #
        data = data.split(';')  # List[str] - ["<spaces>","<temperature>","<time>"]
        if data[0] == "Full":
            data[0] = 0
        else:
            data[0] = int(data[0])

        data[1] = float(data[1])

        data[2] = datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")

        print(self.data)
        self.data = [data[0], data[1], data[2]]

config = {"name": "time-series-display",
          "location": "moondaloop",
          "topic-root": "lot",
          "topic-qualifier": "na",
          "broker": "localhost",
          "port": 1883
          }
ts_display = TimeSeriesDisplay(config)

source = ColumnDataSource(data={"x": [], "y": []})

plot = figure(height=300, width=800, x_axis_type="datetime", title="Available Spaces")
plot.line(x="x", y="y", source=source)



def update():
    if ts_display.data is not None:
        source.stream({"x": [ts_display.data[2]], "y": [ts_display.data[0]]}, rollover=5000)

curdoc().add_root(plot)
curdoc().add_periodic_callback(update, 50)
