# from signalrcore.hub_connection_builder import HubConnectionBuilder

# hub_connection = HubConnectionBuilder('https://livetiming.formula1.com/signalr')
# hub_connection.build()
# hub_connection.on("ReceiveMessage", print)
# hub_connection.start()

####
# import logging
# from livetiming_fetch.client import SignalRClient


# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

# client = SignalRClient("TimingData.json", debug=False, timeout=600, topics=["TimingData"])
# """ 
# topics argument can be changed. 
# Default: ["CarData.z"]

# parameters:
#     ["Heartbeat", "CarData.z", "Position.z",
#     "ExtrapolatedClock", "TopThree", "RcmSeries",
#     "TimingStats", "TimingAppData",
#     "WeatherData", "TrackStatus", "DriverList",
#     "RaceControlMessages", "SessionInfo",
#     "SessionData", "LapCount", "TimingData"]
# """

# client.start()

# import signalr_live

from signalr_live import Connection
from base64 import b64decode
from zlib import decompress, MAX_WBITS
import json

from requests import session

def process_message(message):
    deflated_msg = decompress(b64decode(message), -MAX_WBITS)
    return json.loads(deflated_msg.decode())

# Create debug message handler.
async def on_debug(**msg):
    # In case of 'queryExchangeState'
    if 'R' in msg and type(msg['R']) is not bool:
        decoded_msg = process_message(msg['R'])
        print(decoded_msg)

# Create error handler
async def on_error(msg):
    print(msg)


# Create hub message handler
async def on_message(msg):
    decoded_msg = process_message(msg[0])
    print(decoded_msg)

if __name__ == "__main__":
    # Create connection
    # Users can optionally pass a session object to the client, e.g a cfscrape session to bypass cloudflare.
    # connection = Connection('https://beta.bittrex.com/signalr', session=None)

    sess = session()
    sess.headers = {'User-agent': 'BestHTTP',
                    'Accept-Encoding': 'gzip, identity',
                    'Connection': 'keep-alive, Upgrade'}
    # connection = Connection('https://livetiming.formula1.com/signalr', session=sess)
    connection = Connection('https://signalrasp.azurewebsites.net/raw-connection', session=None)

    # Register hub
    hub = connection.register_hub('Streaming')

    # Assign debug message handler. It streams unfiltered data, uncomment it to test.
    connection.received += on_debug

    # Assign error handler
    connection.error += on_error

    # Assign hub message handler
    hub.client.on('uE', print)
    hub.client.on('uS', print)
    hub.client.on('feed', print)

    # # Send a message
    # hub.server.invoke('SubscribeToExchangeDeltas', 'BTC-ETH')
    # hub.server.invoke('SubscribeToSummaryDeltas')
    # hub.server.invoke('queryExchangeState', 'BTC-NEO')

    # hub.server.invoke("Subscribe",["TimingData"])
    hub.server.invoke("Subscribe", ["streaming-connection"])

    # Start the client
    connection.start()