from ast import dump
import asyncio
from h11 import Data
import websockets
import json
from datetime import datetime, timezone
import csv

async def connect_ais_stream():

    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": "027416a0482eabbcdce8b5b6218515bcfb879f65", "BoundingBoxes": [[[3, 29], [38, 43]]], "FilterMessageTypes":["ShipStaticData"]}

        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
                
            message_type = message["MessageType"]            

            if message_type == "ShipStaticData":
                ais_message = message['Message']['ShipStaticData']
                ais_metadata = message['MetaData']               
                ais_message.update(ais_metadata)
                         
                csv_file_path = 'data.csv'
                
                with open(csv_file_path, 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    #for ship in ais_message:
                    csv.writer(csv_file).writerow(
                        [                                
                            ais_message['time_utc'],
                            ais_message['CallSign'],
                            ais_message['ShipName'],
                            ais_message['Type'],
                            ais_message['ImoNumber'],
                            ais_message['MMSI'],
                            ais_message['latitude'],
                            ais_message['longitude'],
                            ais_message['Destination'],
                            ais_message['FixType'],                            
                            ais_message['Dimension']['A'],
                            ais_message['Dimension']['B'],
                            ais_message['Dimension']['C'],
                            ais_message['Dimension']['D'],
                            ais_message['MaximumStaticDraught'],
                            ais_message['MessageID']
                             ]
                         )               

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())



