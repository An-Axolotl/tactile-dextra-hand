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
// Output: one line per sample at 9600 baud, e.g.
//   Palm:0, Thumb:412, Index:0, Middle:388, Ring:0, Pinky:0

const int fsrPins[6] = {A0, A1, A2, A3, A4, A5};

enum Finger {
  INDEX = 0,
  MIDDLE = 1,
  THUMB = 2,
  PALM = 3,
  RING = 4,
  PINKY = 5
};

const char* fingerNames[6] = {
  "Index",
  "Middle",
  "Thumb",
  "Palm",
  "Ring",
  "Pinky"
};

// Desired output order
const int printOrder[6] = {
  PALM,
  THUMB,
  INDEX,
  MIDDLE,
  RING,
  PINKY
};

void setup() {
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 6; i++) {
    int idx = printOrder[i];
    int v = analogRead(fsrPins[idx]);

    int contact = (v > 0) ? 1 : 0;

    Serial.print(fingerNames[idx]);
    Serial.print(":");
    Serial.print(v);

    if (i < 5) Serial.print(", ");
  }
  Serial.println();
}
