/*
 *  Timer Sleep
 */

#include <WiFi.h>
#include <HTTPClient.h>

#define uS_TO_S_FACTOR 1000000ULL  /* Conversion factor for micro seconds to seconds */
#define ledPin 18
#define vibration_sw 33
#define BUTTON_PIN_BITMASK 0x200000000 // 2^33 in hex
#define TIME_TO_SLEEP  900 // sleep for 15 minutes

RTC_DATA_ATTR int prev_signal = -1;
unsigned long countStart = 0;

const char* ssid = "RedRover";   
const char* password = "";

const int RSSI_MAX =-50;// define maximum strength of signal in dBm
const int RSSI_MIN =-100;// define minimum strength of signal in dBm
const int displayEnc=1;// set to 1 to display Encryption or 0 not to display
const int wifi_scan_num = 2; // determine the number of times to scan wifi before sending to server

// Set scan duration to 180 seconds (180000)
unsigned long duration = 180000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;

int signal_history[8] = {};
int history_size = 8;
int history_idx = 0;
int sleep_mode = 0;

//Domain name with URL path or IP address with path
int router_num = 30;
String routers[30] = {"94:B4:0F:E6:35:A", "94:B4:0F:E6:45:C", "94:B4:0F:E6:44:E", "E8:26:89:37:9B:8", "E8:26:89:37:DB:8", 
                    "94:B4:0F:E6:45:E", "F0:5C:19:6E:A0:A", "94:B4:0F:E6:34:E", "F0:5C:19:6E:74:C",
                    "94:B4:0F:E6:60:E", "94:B4:0F:E6:62:0", "94:B4:0F:E6:62:4",
                    "94:B4:0F:E6:5F:0", "94:B4:0F:E6:47:8", "94:B4:0F:E6:61:0", "94:B4:0F:E6:5E:4",
                    "B4:5D:50:83:FE:2", "B4:5D:50:81:56:E", "94:B4:0F:E6:62:4", "F0:5C:19:76:3D:C", "AC:A3:1E:05:40:E",
                    "F0:5C:19:A9:38:8", "F0:5C:19:A9:5C:A", "F0:5C:19:A9:59:A", "F0:5C:19:A9:59:C", "F0:5C:19:A9:59:8",
                    "F0:5C:19:A9:38:8", "F0:5C:19:A9:5A:8", "F0:5C:19:A9:31:2", "F0:5C:19:A9:32:0"};
                    
String serverName = "http://connect.owendpersonal.com/data";
int MAX_signal = 30;
int scan_size = 0;
String MAC_scan[30] = {};
int dB_accum_scan[30] = {};
int dB_num_scan[30]   = {};
int exist_in_scan = 0;
int vibrate = 0;

WiFiClient client;

void setup() {

  for(int i = 0; i < 30; i++){
    dB_accum_scan[i] = 0;
    dB_num_scan[i] = 0;
  }

  Serial.begin(9600);

  // Deep Sleep Mode Test LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);

  countStart = millis(); // start counter
  Serial.println("RESTART");

  pinMode(vibration_sw, INPUT);
  vibrate = digitalRead(vibration_sw);

  /*
  Configure the wake up source
  Set ESP32 to wake up every 60 seconds
  */
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
}

void loop(){
  // within duration, wifi will scan and send http message
  if( (millis() - countStart) <= duration ){
    // Scan the WiFi signal first
    String signals = WIFI_Scan(); 

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
      if(sleep_mode == 1){
        enter_deep_sleep();
      }
    }
  }
  else{
    enter_deep_sleep();
  }
}

void history_check(int signal_history[]){
  int eq = 1;
  if(history_idx == history_size - 1){
    // check the history list to see if the 5 previous readings are the same
    for(int i = 1; i < sizeof(signal_history); i++){
      // if not the same, set flag eq to be 0
      if(signal_history[i-1] != signal_history[i]){
        eq = 0;
      }
    }

    // if the history table shows the same signal for all 5 scans
    // save the signal and go to sleep
    if(eq){
      prev_signal = signal_history[4];
      Serial.println("history siganl the same");
      enter_deep_sleep();
    }
  }
}

// function to put ESP32 to deep sleep mode 
void enter_deep_sleep(){
  // Send an HTTP POST request depending on timerDelay
  // delay(timerDelay);
  digitalWrite(ledPin, LOW);
  delay(timerDelay);
  Serial.println("Going to sleep now");
  esp_deep_sleep_start();  
}

// function to perform WIFI scanning
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
    //  Serial.print("MAC:");
    //  Serial.print(MAC_scan[i]); //BSSID 
    //  Serial.println();
    //  Serial.print("dB:");
    //  Serial.print((float)dB_accum_scan[i]/(float)dB_num_scan[i]);// Avg signal strength in %
    //  Serial.println();
  }

  signals = signals + "MAC:" + MAC_scan[max_index] + " " + "dB:" + (float)dB_accum_scan[max_index]/(float)dB_num_scan[max_index] + " " + "ESP:" + WiFi.macAddress();
  
  // save the signal to history table
  for(int i = 0; i < router_num; i++){
    if(routers[i] == MAC_scan[max_index]){
      signal_history[history_idx] = i;
    }
  }

  if(history_idx == 0){
    // if vibration is detected
    if(vibrate == 0){
      // if the signal has not changed from previous reading
      // go to sleep again
      if(signal_history[history_idx] == prev_signal){
        Serial.println("vibrate and prev siganl the same");
        sleep_mode = 1;
      }
    }
  }

  // check if the previous readings are the same
  // if so, put to deep sleep
  history_check(signal_history);

  // reset it back to 0 once it reaches the upper bound
  if(history_idx < history_size){
    history_idx++;
  }else{
    history_idx = 0;
  }

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
  // delay(timerDelay);
  // Serial.println("Timer set to 10 seconds (timerDelay variable), it will take 10 seconds before publishing the first reading.");
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
