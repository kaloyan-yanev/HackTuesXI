import time
import json
import pymysql
import socket
import asyncio
from bleak import BleakClient
import datetime


db = pymysql.connect(
host = "localhost",
port = 3306,
user = "root",
passwd = "gogo112008",
db = "sensor_data"
) 
db.autocommit = True
mycursor = db.cursor()

# BLE device address and characteristic UUID
DEVICE_ADDRESS = "40:4c:ca:57:78:92"
CHARACTERISTIC_UUID = "BEB5483E-36E1-4688-B7F5-EA07361B26A8"  # Replace with your BLE characteristic UUID

def No_Data():
    return "No Data"

# Function to handle sensor data
def Sensor_Data_Handler(jsonData):
    json_Dict = json.loads(jsonData)

    dist1 = json_Dict['dist1']
    dist2 = json_Dict['dist2']
    gir_seat = json_Dict['giros_seat_X']
    gir_stol = json_Dict['giros_human_Y']
    val = [datetime.datetime.now() , gir_seat, gir_stol, dist1, dist2]
    my_sql = "INSERT INTO sensor_data (date_and_time, angle_seat, angle_stol, dist1, dist2) VALUES (%s, %f, %f, %f, %f)"

    mycursor.execute(my_sql, val)
    db.commit()
    print(jsonData)

# Async function to handle BLE communication
async def main():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print("Connected to BLE device")
        while True:
            try:
                # Read data from the characteristic
                data = await client.read_gatt_char(CHARACTERISTIC_UUID)
                decoded_packet = data.decode('utf-8')
                if decoded_packet == "No data":
                    No_Data()
                else:
                    spl = decoded_packet.split("@")
                    Sensor_Data_Handler(spl[0])
            except Exception as e:
                print(f"Error: {e}")
                
                break

# Run the BLE event loop
asyncio.run(main())