// Tactile robot hand: reads 6 FSRs (5 round fingertip FSRs + 1 square palm FSR).
//
// Each sensor is wired as a voltage divider (see images/circuit.png):
//
//     5V -- FSR (R_top) --+-- 100k --- 100k -- GND
//                         |      (R_bottom = 200k)
//                         +--> analog pin (V_out)
//
//   V_out = 5V * 200k / (R_FSR + 200k)
//
// Untouched, the FSR is effectively open (>> 1 MOhm), so the pin reads ~0.
// Pressing lowers R_FSR, so V_out (and analogRead, 0..1023) rises.
// The large 200k bottom resistor (2 x 100k) makes light touches show up
// clearly, but readings saturate sooner under heavy force.
//
// Each loop reads all 6 sensors into a snapshot first, then prints them
// together, so every line is one consistent sample of the whole hand.
//
// High-impedance dividers (FSR + 200k) are slower to charge the ADC's sample
// capacitor than the ~10k source the ATmega expects, so after switching
// channels the first reading can pick up some of the previous channel
// (crosstalk). Each channel is read twice and the first reading is discarded.
//
// Output: one line per sample at 115200 baud (Serial Monitor / Plotter), e.g.
//   Palm:0, Thumb:412, Index:0, Middle:388, Ring:0, Pinky:0

const int NUM_SENSORS = 6;
const long BAUD_RATE = 115200;

const int fsrPins[NUM_SENSORS] = {A0, A1, A2, A3, A4, A5};

enum Sensor {
  INDEX = 0,
  MIDDLE = 1,
  THUMB = 2,
  PALM = 3,
  RING = 4,
  PINKY = 5
};

const char* sensorNames[NUM_SENSORS] = {
  "Index",
  "Middle",
  "Thumb",
  "Palm",
  "Ring",
  "Pinky"
};

// Print order: palm first, then thumb to pinky
const int printOrder[NUM_SENSORS] = {PALM, THUMB, INDEX, MIDDLE, RING, PINKY};

int readings[NUM_SENSORS];

int readSettled(int pin) {
  analogRead(pin);              // discard: lets the ADC sample cap settle on this channel
  delayMicroseconds(50);
  return analogRead(pin);
}

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  // 1) snapshot all sensors
  for (int i = 0; i < NUM_SENSORS; i++) {
    readings[i] = readSettled(fsrPins[i]);
  }

  // 2) print the snapshot as one line
  for (int i = 0; i < NUM_SENSORS; i++) {
    int idx = printOrder[i];
    Serial.print(sensorNames[idx]);
    Serial.print(':');
    Serial.print(readings[idx]);
    if (i < NUM_SENSORS - 1) Serial.print(", ");
  }
  Serial.println();
}
