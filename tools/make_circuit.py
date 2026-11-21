"""Draw images/circuit.png: 6 FSR voltage dividers (5 fingertip + 1 palm) into an Arduino."""
from pathlib import Path
import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).resolve().parent.parent / "images"
# (Arduino pin, sensor label) -- pin map from firmware/TripleFingerPadTouch
CH = [("A0", "Index"), ("A1", "Middle"), ("A2", "Thumb"),
      ("A3", "Palm"), ("A4", "Ring"), ("A5", "Pinky")]
DX = 3.6

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=12, unit=2.2)
    top = elm.Line().right(DX * len(CH) - DX + 1.2).at((-0.6, 0)).label("+5V (Arduino 5V)", "top")
    gnd_y = -9.4
    elm.Line().right(DX * len(CH) - DX + 1.2).at((-0.6, gnd_y))
    elm.Ground().at((DX * len(CH) / 2 - DX / 2, gnd_y))
    for i, (pin, name) in enumerate(CH):
        x = i * DX
        elm.Dot().at((x, 0))
        palm = name == "Palm"
        fsr = elm.ResistorVar().down().at((x, 0))
        elm.Label().at((x + 0.55, -1.1)).label(
            f"{name}\n{'square FSR' if palm else 'round FSR'}", halign="left", fontsize=10)
        node = fsr.end
        elm.Dot().at(node)
        elm.Line().right(0.9).at(node)
        elm.Dot(open=True).label(pin, "right")
        r1 = elm.Resistor().down().at(node).length(2.6)
        r2 = elm.Resistor().down().length(2.6)
        for r in (r1, r2):
            elm.Label().at((x + 0.45, r.center[1])).label("100 kΩ", halign="left", fontsize=10)
        elm.Line().down().toy(gnd_y)
        elm.Dot()
    elm.Label().at((DX * len(CH) / 2 - DX / 2, gnd_y - 1.4)).label("GND (Arduino GND)")
    elm.Label().at((DX * len(CH) / 2 - DX / 2, 1.5)).label(
        "V_pin = 5V · 200k / (R_FSR + 200k)   — no press: R_FSR ≫ 1 MΩ → ~0 V; press: R_FSR ↓ → V_pin ↑",
        fontsize=10)
    d.save(str(OUT / "circuit.png"), dpi=200)
    d.save(str(OUT / "circuit.svg"))
print("saved")
