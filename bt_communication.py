import time
import json
import pymysql
import socket
import asyncio
from bleak import BleakClient


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

# Function to handle sensor data
def Sensor_Data_Handler(jsonData):
    json_Dict = json.loads(jsonData)

    but1 = json_Dict['but1']
    but2 = json_Dict['but2']
    but3 = json_Dict['but3']
    but4 = json_Dict['but4']
    but5 = json_Dict['but5']
    dist1 = json_Dict['dist1']
    dist2 = json_Dict['dist2']
    but6 = json_Dict['but6']
    but7 = json_Dict['but7']
    but8 = json_Dict['but8']
    but9 = json_Dict['but9']
    but10 = json_Dict['but10']

    val = [but1, but2, but3, but4, but5, but6, but7, but8, but9, but10, dist1, dist2]
    my_sql = "INSERT INTO test_data (BUTTON1, BUTTON2, BUTTON3, BUTTON4, BUTTON5, BUTTON6, BUTTON7, BUTTON8, BUTTON9, BUTTON10, DISTANCE1, DISTANCE2 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

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
                spl = decoded_packet.split("@")
                Sensor_Data_Handler(spl[0])
            except Exception as e:
                print(f"Error: {e}")
                break

# Run the BLE event loop
asyncio.run(main())