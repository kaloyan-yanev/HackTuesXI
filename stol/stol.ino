#include <Arduino.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

//гърба
#define press1 1
#define press2 2
#define press3 3
#define press4 4
#define press5 5
#define dist1 A0
#define dist2 A1
#define rel1_nagr 11
#define rel1_ohlad 22

//седалката
#define press6 1
#define press7 2
#define press8 3
#define press9 4
#define press10 5
#define giros_human_SDA 20
#define giros_human_SCL 21
#define giros_seat_SDA 20
#define giros_seat_SCL 21
#define rel2_nagr 111
#define rel2_ohlad 222



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

  //гръб
  pinMode(press1, INPUT);
  pinMode(press2, INPUT);
  pinMode(press3, INPUT);
  pinMode(press4, INPUT);
  pinMode(press5, INPUT);
  pinMode(rel1_nagr, OUTPUT);
  pinMode(rel1_ohlad, OUTPUT);

  //седалка
  pinMode(press6, INPUT);
  pinMode(press7, INPUT);
  pinMode(press8, INPUT);
  pinMode(press9, INPUT);
  pinMode(press10, INPUT);
  pinMode(rel2_nagr, OUTPUT);
  pinMode(rel2_ohlad, OUTPUT);

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

String data_handler(){
  //гръб
  String my_json = "{";
  my_json += "\"but1\":" + String(digitalRead(press1)) + ",";
  my_json += "\"but2\":" + String(digitalRead(press2)) + ",";
  my_json += "\"but3\":" + String(digitalRead(press3)) + ",";
  my_json += "\"but4\":" + String(digitalRead(press4)) + ",";
  my_json += "\"but5\":" + String(digitalRead(press5)) + ",";
  my_json += "\"dist1\":" + String(analogRead(dist1)) + ",";
  my_json += "\"dist2\":" + String(analogRead(dist2)) + ",";
  //седалка
  my_json += "\"but6\":" + String(digitalRead(press6)) + ",";
  my_json += "\"but7\":" + String(digitalRead(press7)) + ",";
  my_json += "\"but8\":" + String(digitalRead(press8)) + ",";
  my_json += "\"but9\":" + String(digitalRead(press9)) + ",";
  my_json += "\"but10\":" + String(digitalRead(press10))+ ",";
  my_json += "\"giros_human_X\":" + String(digitalRead(press10))+ ",";
  my_json += "\"giros_human_Y\":" + String(digitalRead(press10))+ ",";
  my_json += "\"giros_seat_X\":" + String(digitalRead(press10))+ ",";
  my_json += "\"giros_seat_Y\":" + String(digitalRead(press10));
  my_json += "}@";
  
  return my_json;
}

void loop() {
  if(digitalRead(press1) == HIGH){
    if(runEvery(3000)){
      if (deviceConnected) {
          pCharacteristic->setValue(data_handler());
          pCharacteristic->notify();
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
