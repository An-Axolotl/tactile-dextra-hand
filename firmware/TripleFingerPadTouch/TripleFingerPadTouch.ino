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
