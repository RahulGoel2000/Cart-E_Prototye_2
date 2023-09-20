/*
 *  Simple HTTP get webclient test
 */

#include <WiFi.h>
#include <HTTPClient.h>
// #include <WiFiClient.h>

#define ledPin 18 /**/
#define BUTTON_PIN_BITMASK 0x200000000 // 2^33 in hex

RTC_DATA_ATTR int bootCount = 0;
unsigned long countStart = 0;

const char* ssid = "AlgaForCartE";//"CameraZh";    
const char* password = "AlgaPeng";//"0931093b"; 

const int RSSI_MAX =-50;// define maximum strength of signal in dBm
const int RSSI_MIN =-100;// define minimum strength of signal in dBm
const int displayEnc=1;// set to 1 to display Encryption or 0 not to display
const int wifi_scan_num = 1; // determine the number of times to scan wifi before sending to server

// Set timer to 30 seconds (30000)
unsigned long duration = 60000;
unsigned long timerDelay = 30000;

//Domain name with URL path or IP address with path
int router_num = 30;
String routers[30] = {"94:B4:0F:E6:35:A", "94:B4:0F:E6:45:C", "94:B4:0F:E6:44:E", "E8:26:89:37:9B:8", "E8:26:89:37:DB:8", 
                    "94:B4:0F:E6:45:E", "F0:5C:19:6E:A0:A", "94:B4:0F:E6:34:E", "F0:5C:19:6E:74:C",
                    "94:B4:0F:E6:60:E", "94:B4:0F:E6:62:0", "94:B4:0F:E6:62:4",
                    "94:B4:0F:E6:5F:0", "94:B4:0F:E6:47:8", "94:B4:0F:E6:61:0", "94:B4:0F:E6:5E:4",
                    "B4:5D:50:83:FE:2", "B4:5D:50:81:56:E", "94:B4:0F:E6:62:4", "F0:5C:19:76:3D:C", "AC:A3:1E:05:40:E",
                    "F0:5C:19:A9:38:8", "F0:5C:19:A9:5C:A", "F0:5C:19:A9:59:A", "F0:5C:19:A9:59:C", "F0:5C:19:A9:59:8",
                    "F0:5C:19:A9:38:8", "F0:5C:19:A9:5A:8", "F0:5C:19:A9:31:2", "F0:5C:19:A9:32:0"};
String serverName = "http://connect.owendpersonal.com/data"; //"132.236.79.6:80/post";
int MAX_signal = 10;
int scan_size = 0;
String MAC_scan[10] = {};
int dB_accum_scan[10] = {0,0,0,0,0,0,0,0,0,0};
int dB_num_scan[10]   = {0,0,0,0,0,0,0,0,0,0};
int exist_in_scan = 0;

WiFiClient client;

void setup() {
  Serial.begin(9600);
  Serial.println("Setup");

  // Deep Sleep Mode Test LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  countStart = millis(); // start counter
  Serial.println("RESTART");
  /*
  First we configure the wake up source
  We set our ESP32 to wake up for an external trigger.
  There are two types for ESP32, ext0 and ext1 .
  ext0 uses RTC_IO to wakeup thus requires RTC peripherals
  to be on while ext1 uses RTC Controller so doesnt need
  peripherals to be powered on.
  Note that using internal pullups/pulldowns also requires
  RTC peripherals to be turned on.
  */
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_33,0); //1 = High, 0 = Low
}

void loop(){
  // within duration, wifi will scan and send http message
  if( (millis() - countStart) <= duration ){
    // Scan the WiFi signal first
    String signals = WIFI_Scan(); 
    Serial.println(signals);
    // if received data from wifi scan
    if(signals != ""){
      WIFI_Connect();
      //Check WiFi connection status
      if(WiFi.status() == WL_CONNECTED){
        HTTPClient http;

        // Your Domain name with URL path or IP address with path
        http.begin(client, serverName);

        // Send HTTP POST request
        http.addHeader("Content-Type", "text/plain"); 

        auto httpCode = http.POST(signals); // Send the request
        if (httpCode>0) {
          Serial.println("--------------------------------------------------");
          Serial.println("--------------------------------------------------");
          Serial.print("HTTP Response code: ");
          Serial.println(httpCode);
          String payload = http.getString(); // Get the response payload
          Serial.println(payload);
        }
        else {
          Serial.print("Error code: ");
          Serial.println(httpCode);
        }
        // Free resources
        http.end();
      }
      else {
        Serial.println("WiFi Disconnected");
      }
    }
  }
  else{
    // Send an HTTP POST request depending on timerDelay
    // delay(timerDelay);
    digitalWrite(ledPin, LOW);
    Serial.println("Going to sleep now");
    esp_deep_sleep_start();  
  }
}

String WIFI_Scan()
{
  String signals = "";
  Serial.println("--------------------------------------------------");
  Serial.println("--------------------------------------------------");
  Serial.println("Wifi Signal Scan");
  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  for(int i = 0; i < wifi_scan_num; i++){
    // WiFi.scanNetworks will return the number of networks found
    int n = WiFi.scanNetworks();

    if (n == 0) {
      Serial.println("no networks found");
    } else {
      for (int i = 0; i < n; ++i) {
        // if the BSSID is in the mac_scan list, add the strength
        // if BSSID in MAC_scan
        for (int k = 0; k < MAX_signal; k++){
          if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1)== MAC_scan[k])
          {
            exist_in_scan = 1;
            dB_accum_scan[k] += dBmtoPercentage(WiFi.RSSI(i));
            dB_num_scan[k] += 1;
            break;
          }
        }
        // else
        if (!exist_in_scan){
          // if it is a new mac address from a known router
          for (int j = 0; j < router_num; j++){
            if (WiFi.BSSIDstr(i).substring(0, WiFi.BSSIDstr(i).length() - 1) == routers[j]){
                MAC_scan[scan_size] = routers[j]; // only store the known substring in the list
                dB_accum_scan[scan_size] = dBmtoPercentage(WiFi.RSSI(i));
                dB_num_scan[scan_size] += 1;
                scan_size += 1;
                break;
            }
          }
        }
        exist_in_scan = 0;
      }
    }
    delay(10);
  }
  float max_dB = 0;
  int max_index = 0;

  for (int i = 0; i < scan_size; i++){
    if ((float)dB_accum_scan[i]/(float)dB_num_scan[i] > max_dB) {
      max_dB = (float)dB_accum_scan[i]/(float)dB_num_scan[i];
      max_index = i;
    }
     Serial.print("MAC:");
     Serial.print(MAC_scan[i]); //BSSID 
     Serial.println();
     Serial.print("dB:");
     Serial.print((float)dB_accum_scan[i]/(float)dB_num_scan[i]);// Avg signal strength in %
     Serial.println();
  }

  //  signals = signals + "MAC:" + WiFi.BSSIDstr(i) + " " + "dB:" + dBmtoPercentage(WiFi.RSSI(i))+ " ";
  signals = signals + "MAC:" + MAC_scan[max_index] + " " + "dB:" + (float)dB_accum_scan[max_index]/(float)dB_num_scan[max_index] + " " + "ESP:" + WiFi.macAddress();

  for (int i = 0; i < MAX_signal; i ++){
    MAC_scan[i] = ""; 
    dB_accum_scan[i] = 0;   
    dB_num_scan[i] = 0; 
  }

  scan_size = 0;

  WiFi.scanDelete(); 
  Serial.println("Wifi scan ended"); 
  return signals;
}

void WIFI_Connect()
{
  digitalWrite(ledPin, LOW);
  Serial.println("--------------------------------------------------");
  Serial.println("--------------------------------------------------");
  // We send data by connecting to a WiFi network
  Serial.print("Connecting to ");
  Serial.println(ssid);

  /* Explicitly set the ESP8266 to be a WiFi-client, otherwise, it by default,
     would try to act as both a client and an access-point and could cause
     network-issues with your other WiFi-devices on your WiFi-network. */
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("ESP Board MAC Address:  ");
  Serial.println(WiFi.macAddress());

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  digitalWrite(ledPin, HIGH);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());  
  delay(timerDelay);
  Serial.println("Timer set to 10 seconds (timerDelay variable), it will take 10 seconds before publishing the first reading.");
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
