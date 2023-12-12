#include "WiFi.h"

const int RSSI_MAX =-50;// define maximum strength of signal in dBm
const int RSSI_MIN =-100;// define minimum strength of signal in dBm

const int displayEnc=1;// set to 1 to display Encryption or 0 not to display
String routers[9] = {"94:B4:0F:E6:35:A", "94:B4:0F:E6:45:C", "94:B4:0F:E6:44:E", "E8:26:89:37:9B:8", "E8:26:89:37:DB:8", "94:B4:0F:E6:45:E", "F0:5C:19:6E:A0:A", "94:B4:0F:E6:5F:0", "F0:5C:19:6E:74:C"};

void setup() {
  Serial.begin(9600);
  Serial.println("Wifi Signal Scan");
  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(2000);

  Serial.println("Setup done");
}

void loop() {
  Serial.println("Wifi scan started");

  // WiFi.scanNetworks will return the number of networks found
  int n = WiFi.scanNetworks();
  Serial.println("Wifi scan ended");
  if (n == 0) {
    Serial.println("no networks found");
  } else {
    for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
      if ((WiFi.SSID(i)=="Cornell-Visitor") || (WiFi.SSID(i)=="eduroam") || (WiFi.SSID(i)=="RedRover")){
        if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1) == "94:B4:0F:E6:35:A")
          Serial.print("phillips-200ca-1 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:45:C")
          Serial.print("phillips-200ca-2 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:44:E")
          Serial.print("phillips-200ca-3 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "E8:26:89:37:9B:8")
          Serial.print("phillips-203 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "E8:26:89:37:DB:8")
          Serial.print("phillips-219 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:45:E")
          Serial.print("phillips-232 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:6E:A0:A")
          Serial.print("phillips-237 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:34:E")
          Serial.print("phillips-238 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:6E:74:C")
          Serial.print("phillips-239 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:60:E")
          Serial.print("phillips-100cb-1 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:62:0")
          Serial.print("phillips-100cb-2 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:62:4")
          Serial.print("phillips-100cb-3 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:47:8")
          Serial.print("phillips-300ca-1 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:61:0")
          Serial.print("phillips-300ca-2 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:5E:4")
          Serial.print("phillips-300ca-3 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "94:B4:0F:E6:5F:0")
          Serial.print("phillips-300cb-1 ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "B4:5D:50:83:FE:2")
          Serial.print("upson-30041-2-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "B4:5D:50:81:56:E")
          Serial.print("upson-30041-1-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:76:3F:E")
          Serial.print("upson-30040-1-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:76:3D:C")
          Serial.print("upson-30040-2-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "AC:A3:1E:05:40:E")
          Serial.print("upson-3-west ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:38:8")
          Serial.print("upson-20041-2-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:5C:A")
          Serial.print("upson-20041-1-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:59:C")
          Serial.print("upson-20040-1-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:59:A")
          Serial.print("upson-20040-2-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:59:8")
          Serial.print("upson-2-west ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:5A:8")
          Serial.print("upson-10041-1-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:32:0")
          Serial.print("upson-10040-1-ap ");
        else if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== "F0:5C:19:A9:31:2")
          Serial.print("upson-10040-2-ap ");

        Serial.print(WiFi.BSSIDstr(i)); //BSSID     
        Serial.print(" ");
        Serial.print(dBmtoPercentage(WiFi.RSSI(i)));//Signal strength in %  
        Serial.println("% )"); 
    }
      delay(10);
    }
  }
  Serial.println("");

  // Wait a bit before scanning again
  delay(5000);
  WiFi.scanDelete();  
}

/*
 * Written by Ahmad Shamshiri
  * with lots of research, this source was used:
 * https://support.randomsolutions.nl/827069-Best-dBm-Values-for-Wifi 
 * This is approximate percentage calculation of RSSI
 * WiFi Signal Strength Calculation
 * Written Aug 08, 2019 at 21:45 in Ajax, Ontario, Canada
 */

int dBmtoPercentage(int dBm)
{
  int quality;
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
