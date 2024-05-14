#include <WiFi.h>
#include <HTTPClient.h>

const char *ssid = "RedRover";
const char *password = "";
const char* serverName = "http://10.49.20.67/data";
const char* ESP32_ID = "0003";

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(1000);
  pinMode(13, OUTPUT);
  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  // WiFi.begin(ssid);
  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(1000);
  //   Serial.println("Connecting...");
  // }
  // Serial.println("Connected to WiFi");
}

void loop() {
  // WiFi.begin(ssid, password);
  if (WiFi.status() != WL_CONNECTED)
    WiFi.begin(ssid);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(13, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(100);                      // wait for a second
    digitalWrite(13, LOW);   // turn the LED off by making the voltage LOW
    delay(100); 
    // delay(100);
    Serial.println("Connecting...");
  }
  // Send POST request with sample data
  String data = WIFI_Scan();
  Serial.println(data);
  if (sendChunkedData(data)) {
    Serial.println("Data sent successfully");
    delay(500);
  } else {
    Serial.println("Failed to send data");
  }
  delay(10);
  // WiFi.disconnect();
  // http.end();
   // Send data every 5 seconds
}

// String WIFI_Scan() {
//   int numNetworks = WiFi.scanNetworks();
//   String data = "";
//   if (numNetworks == 0) {
//     data = "No networks found";
//   } else {
//     for (int i = 0; i < numNetworks; ++i) {
//       data += "SSID: " + WiFi.SSID(i) + ", RSSI: " + String(WiFi.RSSI(i)) + "\n";
//     }
//   }
//   return data;
// }

int dBmtoPercentage(int dBm)
{
    int quality;
    const int RSSI_MIN = -100; // Define minimum strength of signal in dBm
    const int RSSI_MAX = -50;  // Define maximum strength of signal in dBm
    
    if(dBm <= RSSI_MIN)
    {
        quality = 0;
    }
    else if(dBm >= RSSI_MAX)
    {  
        quality = 100;
    }
    else
    {
        quality = 2 * (dBm + 100);
    }

    return quality;
}

String WIFI_Scan() {
    int numNetworks = WiFi.scanNetworks();
    String data=String(ESP32_ID)+"\n";
    if (numNetworks == 0) {
        data = "No networks found";
    } else {
        for (int i = 0; i < numNetworks; ++i) {
            String macAddress = WiFi.BSSIDstr(i); // Get MAC address instead of SSID
            int rssi = WiFi.RSSI(i); // Get RSSI value
            int quality = dBmtoPercentage(rssi); // Convert RSSI to percentage
            data += "MAC: " + macAddress + ", Signal Strength: " + String(quality) + "%\n";
        }
    }
    return data;
}


bool sendData(String data) {
  HTTPClient http;
  
  // Send HTTP POST request
  http.begin(client, serverName);
  http.addHeader("Content-Type", "text/plain");
  int httpResponseCode = http.POST(data);

  // Check response
  Serial.print("HTTP response code: ");
  Serial.println(httpResponseCode);
  
  if (httpResponseCode == HTTP_CODE_OK) {
    return true;
  } else {
    return false;
  }

  http.end();
}

bool sendChunkedData(String data) {
  HTTPClient http;
  http.begin(client, serverName);
  http.addHeader("Content-Type", "text/plain");
  int dataLength = data.length();
  int chunkSize = 1500; // Adjust the chunk size as needed
  for (int i = 0; i < dataLength; i += chunkSize) {
    int chunkEnd = min(i + chunkSize, dataLength);
    String chunk = data.substring(i, chunkEnd);
    int httpResponseCode = http.POST(chunk);
    if (httpResponseCode != HTTP_CODE_OK) {
      http.end();
      return false;
    }
  }
  http.end();
  return true;
}

