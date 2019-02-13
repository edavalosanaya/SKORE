//SKORE: Arduino code
//CURRENTLY BEST CODE WE GOT BOI
//Last edit: 2/12/18
//The purpose of this code is to recive inputs from python tutoring script for SKORE.
//Once the settings are configured the program will continuously be looking for what LED to light up
//depending on what note is to be pressed.
//Each color will have its own meaning depending on the situation of the song and user.

#include <FastLED.h>
#define LED_PIN     7
#define NUM_LEDS   88
#define BRIGHTNESS 30
#define UPDATES_PER_SECOND 100


CRGBPalette16 currentPalette;
CRGB leds[NUM_LEDS];
TBlendType    currentBlending;


//byte ledColors[15]; //Format: [R0,G1,B2 (Whites) , R3,G4,B5 (Blacks) , R6,G7,B8(Correct) R9,G10,B11(Incorrect) , R12,G13,B14(Upcoming)]
byte ledColors[12] = {};//arbitrary values for colors.
byte ledNumber;// user input

////////Setting Flags/////////
//bool pianoSettings = true;
bool ledReady = false;
bool correctNotes = false;
bool wrongNotes = false;
bool upcomingNotes = false;
bool whiteNotes = false;
bool colorSettings = true;
bool resetSettings = false;
bool inputFinished = false;
bool newData = false;
bool blackNotes = false;
bool offNotes = false;
//////////////////////////////

///////InputVariables/////////
byte c = 0; //correct ndx
byte w = 0; // wrong ndx
byte k = 0; // normal ndx
byte u = 0; // upcoming ndx
byte x = 0;
byte i = 0; 
byte j = 0;
byte bl = 0;
byte wh = 0;
int n;
char rc;
char endMarker = '\n';
const byte numChars = 32;
char receivedChars[numChars];   // an array to store the received data
int key_array_size = 31; //default 76 key piano
int key_element = 0;
//////////////////////////////

//byte inputArray[20] = {};
byte wrongLeds[64] = {};
byte correctLeds[64] = {};
byte whiteLeds[64] = {};
byte upcomingLeds[64] = {};
byte blackLeds[64] = {};
byte offLeds[64] = {};

bool ledarray_bool[] = {false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
                        ,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false
                         ,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false,false};//88
                                      

void setup() {
  Serial.begin(115200);
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.show();
  currentPalette = RainbowColors_p;
  currentBlending = LINEARBLEND;
  FastLED.setBrightness( BRIGHTNESS );
  Serial.println("<Arduino is ready>");
}


/////////////////////////////////////////////////////////////////////////////////////////////////
void receiveLEDColors() {
  static byte ndx = 0;
  
  
  if (Serial.available() > 0) {
      rc = Serial.read(); 
      if (rc != endMarker && rc != ',') {
          receivedChars[ndx] = rc;
          ndx++;
          if (ndx >= numChars) {
              ndx = numChars - 1;
          }
        }
      else {    
          receivedChars[ndx] = '\0'; // terminate the string
          ndx = 0;

          ledColors[i] = atoi(receivedChars);
          //Serial.print("LedColor[i]: "); Serial.println(ledColors[i]);
          //Serial.print("i : "); Serial.println(i);
          i++;
          }
          if (i >= 12){
            ledReady = true;
            colorSettings = false;
            i = 0;
            Serial.print("+");
       
          }
         }    
        }
/////////////////////////////////////////////////////////////////////////////////////////////////

byte receivePianoSize(){
char receivedInput[numChars];
char character;
byte inputValue;
static byte ndx = 0;
  while (Serial.available() > 0){
    character = Serial.read();
    if (character != '\n') {
          receivedInput[ndx] = character;
          ndx++;
          if (ndx >= numChars) {
              ndx = numChars - 1;
          }
        }
    else{
      receivedInput[ndx] = '\0';
      ndx = 0;
      inputValue = atoi(receivedInput);
      //Serial.println(inputValue);
      return inputValue;
    }
  }
}


/////////////////////////////////////////////////////////////////////////////////////////////////
//getting the size of the piano.


/////////////////////////////////////////////////////////////////////////////////////////////////
void  receiveInput() {
      static byte ndx = 0;
      static boolean recvInProgress = false;
      char startMarker = '<';
      char endMarker = '>';
     
      if (Serial.available() > 0) {
          rc = Serial.read();

          
          if( rc == 'w'){   // normal colors W & B
            Serial.print("white");
            correctNotes = false;
            wrongNotes = false;
            upcomingNotes = false;
            whiteNotes = true;
            blackNotes = false;
            offNotes = false;
          }

          else if( rc == 'b'){   // normal colors W & B
            correctNotes = false;
            wrongNotes = false;
            upcomingNotes = false;
            whiteNotes = false;
            blackNotes = true;
            offNotes = false;
          }
          
          else if( rc == 'i'){  //wrong Notes
            correctNotes = false;
            wrongNotes = true;
            upcomingNotes = false;
            whiteNotes = false;
            blackNotes = false;
            offNotes = false;
            
          }
          else if( rc == 'u'){  //upcoming Notes
            correctNotes = false;
            wrongNotes = false;
            upcomingNotes = true;
            whiteNotes = false;
            blackNotes = false;
            offNotes = false;
          }

           else if( rc == 'f'){
            correctNotes = false;
            wrongNotes = false;
            upcomingNotes = false;
            whiteNotes = false;
            blackNotes = false;
            offNotes = true;
           }

           
           else if( rc == '!'){
            FastLED.clear();
            FastLED.show(); 
          }
          
          
            
          //delay(2); //tolerance for serial buffering. 
          if (recvInProgress == true){
            if (rc != endMarker && rc != ',' && rc != '*') {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else if (rc == ','){
              receivedChars[ndx] = '\0'; // terminate the string
              ndx = 0;
           
              if(correctNotes){
                correctLeds[c] = atoi(receivedChars);
                c++;
                receiveInput();
              }

              else if(wrongNotes){
                wrongLeds[w] = atoi(receivedChars);
                w++;
                receiveInput();
              }

              else if(upcomingNotes){
                upcomingLeds[u] = atoi(receivedChars);
                u++;
                receiveInput();
              }
             
              else if(whiteNotes){
                whiteLeds[k] = atoi(receivedChars);
                k++;
                receiveInput();
              }
              else if(blackNotes){
                blackLeds[bl] = atoi(receivedChars);
                bl++;
                receiveInput();
              }

              else if(offNotes){
                offLeds[x] = atoi(receivedChars);
                x++;
                receiveInput();           
            }
            }

            else if (rc == endMarker){
            receivedChars[ndx] = '\0'; // terminate the string
            recvInProgress = false;
            ndx = 0;
            newData = true;
            c = 0;
            w = 0;
            u = 0;
            x = 0;
            k = 0;
            bl = 0;           
            }  
           }
           else if (rc == startMarker){
            recvInProgress = true;     
           }
          }
         }
        



/////////////////////////////////////////////////////////////////////////////////////////////////
// These 2 functions are responsible for the "lightshow" untill the user is ready to input settings.
void ledVisual(){
   static uint8_t startIndex = 0;
    startIndex = startIndex + 1; /* motion speed */
    
    FillLEDsFromPaletteColors( startIndex);
    
    FastLED.show();
    FastLED.delay(1000 / UPDATES_PER_SECOND);
}

void FillLEDsFromPaletteColors( uint8_t colorIndex)
{
    uint8_t brightness = 255;
    
    for( int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette( currentPalette, colorIndex, brightness, currentBlending);
        colorIndex += 3;
    }
}

/////////////////////////////////////////////////////////////////////////////////////////////////
// Binary searching
// if element is present at the middle then done,
// if the middle is greater than we "shrink" the array to left side
// or vice versa if smaller.
// I am using binary search here to save as much time as possible.
//Even though the array is relatively small this may make no difference.
bool binarySearch(int arr[], int l, int r, int x){

   if (r >= l) 
   { 
        int mid = l + (r - l)/2;     
        if (arr[mid] == x)   
            return true; 
        if (arr[mid] > x)  
            return binarySearch(arr, l, mid-1, x); 
        return binarySearch(arr, mid+1, r, x); 
        } 
   return false; 
   } 


/////////////////////////////////////////////////////////////////////////////////////////////////
//byte ledColors[15]; //Format: [R0,G1,B2 (Whites) , R3,G4,B5 (Blacks) , R6,G7,B8(Correct) R9,G10,B11(Incorrect) , R12,G13,B14(Wait)]
void ledLighting(){
  bool note_check;
//100,100,100,100,0,0,0,100,0,0,0,100


  
  for ( j = 0; j < 64; j++ ){

    if (offNotes){
      if(offLeds[j] != 0){
      leds[offLeds[j] - 1] = CRGB::Black;
      offLeds[j] = 0;
      Serial.println("offnotes");
      }
    }
    else if(wrongLeds || upcomingLeds || whiteLeds || blackLeds){    
      
      if(wrongLeds[j] != 0){
        leds[wrongLeds[j]-1] = CRGB(ledColors[6],ledColors[7],ledColors[8]);
        Serial.println("wrongnotes");
      }
      if(upcomingLeds[j] != 0){
        leds[upcomingLeds[j]-1] = CRGB(ledColors[9],ledColors[10],ledColors[11]);
        Serial.println("upcomnotes");
      }
      if(whiteLeds[j] != 0){
        Serial.println(whiteLeds[j]);
        leds[whiteLeds[j]-1] = CRGB(ledColors[0],ledColors[1],ledColors[2]);
      }
      if(blackLeds[j] != 0){
        Serial.println("blacknotes");
        leds[blackLeds[j]-1] = CRGB(ledColors[3],ledColors[4],ledColors[5]);
      }
    }

    offLeds[j] = 0;
    wrongLeds[j] = 0;
    upcomingLeds[j] = 0;
    whiteLeds[j] = 0;
    blackLeds[j] = 0;
    
  }
    
  FastLED.show();
  Serial.print("+"); // Printing for python to know we are finished processing previous input and ready for a new one.
  newData = false;
}

/////////////////////////////////////////////////////////////////////////////////////////////////

/////////////////////////////////////////////////////////////////////////////////////////////////    

void loop() {

  while(colorSettings) { receiveLEDColors(); } 


  if(ledReady){
  receiveInput();
    if(newData){
      ledLighting();
  }
 }
}
