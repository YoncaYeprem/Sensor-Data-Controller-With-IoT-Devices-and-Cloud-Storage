#include "DHT.h"
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#define DHTPIN D5

#define MQ9 A0
#define DHTTYPE DHT11

float startTime;
float endTime;
float interval;
bool isTimeToSend;
String postURL = "http://52.3.249.77:5000/home";

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  WiFi.begin("TurkTelekom_T01B7", "battalgazi_10");   //WiFi connection
  while (WiFi.status() != WL_CONNECTED) {  //Wait for the WiFI connection completion
    delay(500);
    Serial.println("Waiting for connection");
  }
  startTime = 0;
  endTime = 0;
  interval = 3000;
  isTimeToSend = false;
}

void loop() {
  startTime = millis();
  if (startTime - endTime >= interval) {
    endTime += interval;
    isTimeToSend = true;
  }

  if (isTimeToSend == true) {
    int h = (int)dht.readHumidity();
    int t = (int)dht.readTemperature();
    float mq9val = ((float)analogRead(MQ9) / 1023) * 100;
    int m = round(mq9val);
    if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
      HTTPClient http;    //Declare object of class HTTPClient
      http.begin(postURL);      //Specify request destination
      http.addHeader("Content-Type", "text/plain");  //Specify content-type header
      int httpCode = http.POST("{'temperature:'" + String(t) + "',humidity:'" + String(h) + "', carbonmonoxide:'" + String(m) + "'}"); //Send the request
      String payload = http.getString();                  //Get the response payload
      Serial.println(httpCode);   //Print HTTP return code
      Serial.println(payload);    //Print request response payload
      http.end();  //Close connection
      Serial.println("Data Sent !");
    } else {
      Serial.println("Error in WiFi connection");
    }
    isTimeToSend = false;
  }
}
