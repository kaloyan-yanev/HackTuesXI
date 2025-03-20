//пинове за сензори за натиск са просто прекъсвачи защото това имаме
//за гърба
#define press1 1
#define press2 2
#define press3 3
#define press4 4
#define press5 5
#define dist1 A0
#define dist2 A1
#define rel1 11
#define rel2 22

//за седалката
#define press1 1
#define press2 2
#define press3 3
#define press4 4
#define press5 5
#define giros_SDA 20
#define giros_SCL 21
#define rel1 11
#define rel2 22

void setup() {
  Serial.begin(115200);
  
}

void loop() {
  
  Serial.println("Hello World!");
  delay(1000);
}
