#include <Arduino.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Wire.h>
#include <MPU6050_tockn.h>

//гърба
#define dist1 1
#define dist2 10

//седалката
#define but_center_seat 16
#define MPU1_ADDR 0x68
#define MPU2_ADDR 0x69
#define SDA_pin 6
#define SCL_pin 7

MPU6050 mpu1(Wire);
MPU6050 mpu2(Wire);



BLEServer* pServer = NULL;
BLECharacteristic* pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"


class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
    }
};

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_pin, SCL_pin);

  Wire.beginTransmission(MPU1_ADDR);
  Wire.write(0x6B); 
  Wire.write(0x00);
  Wire.endTransmission(true);

  Wire.beginTransmission(MPU2_ADDR);
  Wire.write(0x6B);
  Wire.write(0x00);
  Wire.endTransmission(true);

  mpu1.begin();
  mpu1.calcGyroOffsets(true);

  mpu2.begin();
  mpu2.calcGyroOffsets(true);

  //гръб
  pinMode(but1, INPUT);
  pinMode(but2, INPUT);
  pinMode(but3, INPUT);
  pinMode(but4, INPUT);
  pinMode(but5, INPUT);

  //седалка
  pinMode(but_center_seat, INPUT);

  BLEDevice::init("ESP32");

  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ   |
                      BLECharacteristic::PROPERTY_WRITE  |
                      BLECharacteristic::PROPERTY_NOTIFY |
                      BLECharacteristic::PROPERTY_INDICATE
                    );

  pCharacteristic->addDescriptor(new BLE2902());

  // Start the service
  pService->start();

  // Start advertising
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(false);
  pAdvertising->setMinPreferred(0x0);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
}


float normalizeAngle(float angle) {
    while (angle > 360.0) angle -= 360.0;  // Wrap if greater than 360°
    while (angle < 0.0) angle += 360.0;    // Wrap if less than 0°
    return angle;
}

String data_handler(){
  mpu1.update();
  mpu2.update();
  //гръб
  String my_json = "{";
  my_json += "\"dist1\":" + String(analogRead(dist1)) + ",";
  my_json += "\"dist2\":" + String(digitalRead(dist2)) + ",";
  //седалка
  my_json += "\"but_center_seat\":" + String(digitalRead(but_center_seat)) + ",";
  my_json += "\"giros_human_Y\":" + String(normalizeAngle(mpu1.getAngleY()))+ ",";
  my_json += "\"giros_seat_X\":" + String(normalizeAngle(mpu2.getAngleX()));
  my_json += "}@";
  
  return my_json;
}

void loop() {
  if(digitalRead(but_center_seat)==HIGH){
    if(runEvery(2000)){
      if (deviceConnected) {
          pCharacteristic->setValue(data_handler());
          pCharacteristic->notify();
          Serial.println(data_handler());
      }
    }
  }
  
  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
      delay(500); // give the bluetooth stack the chance to get things ready
      pServer->startAdvertising(); // restart advertising
      Serial.println("start advertising");
      oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
      // do stuff here on connecting
      oldDeviceConnected = deviceConnected;
  }
}

boolean runEvery(unsigned long interval) //интервала е в милисекунди
{
  static unsigned long previousMillis = 0;
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    return true;
  }
  return false;
}
