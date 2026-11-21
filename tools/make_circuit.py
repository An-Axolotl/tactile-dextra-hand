"""Draw images/circuit.png: 6 FSR voltage dividers (5 fingertip + 1 palm) into an Arduino.

Each channel is a voltage divider:
    5V -- R_top (FSR) -- V_out (-> analog pin) -- R_bottom (100k + 100k = 200k) -- GND
"""
from pathlib import Path
import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).resolve().parent.parent / "images"
# (Arduino pin, sensor label) -- pin map from firmware/TripleFingerPadTouch
CH = [("A0", "Index"), ("A1", "Middle"), ("A2", "Thumb"),
      ("A3", "Palm"), ("A4", "Ring"), ("A5", "Pinky")]
DX = 4.0
GND_Y = -9.6

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=12, unit=2.2)
    span = DX * (len(CH) - 1)
    mid = span / 2
    elm.Line().right(span + 2.4).at((-0.6, 0))
    elm.Label().at((mid, 0.55)).label("+5V (Arduino 5V)")
    elm.Line().right(span + 2.4).at((-0.6, GND_Y))
    elm.Ground().at((mid + DX / 2, GND_Y))
    elm.Label().at((mid, GND_Y - 1.5)).label("GND (Arduino GND)")

    for i, (pin, name) in enumerate(CH):
        x = i * DX
        elm.Dot().at((x, 0))
        fsr = elm.ResistorVar().down().at((x, -0.4)).length(2.4)
        elm.Line().at((x, 0)).to(fsr.start)
        node = fsr.end
        elm.Dot().at(node)
        elm.Line().right(1.0).at(node)
        elm.Dot(open=True)
        elm.Label().at((x + 1.15, node[1])).label(f"V_out → {pin}", halign="left", fontsize=11)
        r1 = elm.Resistor().down().at(node).length(2.3)
        r2 = elm.Resistor().down().length(2.3)
        elm.Line().down().toy(GND_Y)
        elm.Dot()

        # labels
        elm.Label().at((x + 0.5, fsr.center[1] + 0.35)).label(
            f"R_top: {name}\n{'square FSR' if name == 'Palm' else 'round FSR'}",
            halign="left", fontsize=10)
        for r in (r1, r2):
            elm.Label().at((x + 0.45, r.center[1])).label("100 kΩ", halign="left", fontsize=10)
        elm.Label().at((x + 1.6, (r1.center[1] + r2.center[1]) / 2)).label(
            "R_bottom\n= 200 kΩ", halign="left", fontsize=9, color="#555")

        # dashed box marking the divider
        x0, x1, y0, y1 = x - 0.45, x + DX - 0.7, -0.25, r2.end[1] - 0.6
        for a, b in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                     ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
            elm.Line().at(a).to(b).linestyle("--").color("#1f77b4").linewidth(1)
        elm.Label().at((x + 0.3, y1 + 0.3)).label(
            "voltage divider", halign="left", fontsize=9, color="#1f77b4")

    elm.Label().at((mid, 2.0)).label(
        "V_out = 5V · R_bottom / (R_FSR + R_bottom),  R_bottom = 200 kΩ\n"
        "untouched: R_FSR ≫ 1 MΩ → V_out ≈ 0 V     pressed: R_FSR drops → V_out rises",
        fontsize=11)
    d.save(str(OUT / "circuit.png"), dpi=200)
    d.save(str(OUT / "circuit.svg"))
print("saved")
