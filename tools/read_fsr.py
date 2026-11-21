#!/usr/bin/env python3
"""Live-read all 6 hand FSRs from the Arduino (firmware/TripleFingerPadTouch).

    pip install pyserial
    python tools/read_fsr.py                    # auto-detect port, live bar display
    python tools/read_fsr.py --port /dev/ttyACM0 --csv touch_log.csv

Each serial line is one snapshot of the whole hand, e.g.
    Palm:0, Thumb:412, Index:0, Middle:388, Ring:0, Pinky:0
Ctrl-C stops immediately (the CSV is flushed every line, so nothing is lost).
"""
import argparse
import csv
import sys
import time

import serial
from serial.tools import list_ports

SENSORS = ["Palm", "Thumb", "Index", "Middle", "Ring", "Pinky"]
ADC_MAX = 1023


def find_port():
    ports = [p.device for p in list_ports.comports()
             if "ACM" in p.device or "USB" in p.device or "usbmodem" in p.device]
    if not ports:
        sys.exit("No Arduino found. Plug it in or pass --port.")
    return ports[0]


def parse(line):
    """'Palm:0, Thumb:412, ...' -> {'Palm': 0, 'Thumb': 412, ...}; None if malformed."""
    try:
        vals = dict(kv.split(":") for kv in line.strip().split(", "))
        out = {k: int(vals[k]) for k in SENSORS}
    except (ValueError, KeyError):
        return None
    return out


def bar(v, width=30):
    n = round(width * v / ADC_MAX)
    return "█" * n + "·" * (width - n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", help="serial port (default: auto-detect)")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--csv", help="also log every sample to this CSV file")
    ap.add_argument("--threshold", type=int, default=20, help="reading above this counts as touch")
    args = ap.parse_args()

    port = args.port or find_port()
    ser = serial.Serial(port, args.baud, timeout=1)
    time.sleep(2)  # most Arduinos reset when the port opens
    ser.reset_input_buffer()
    print(f"Reading {port} @ {args.baud} baud. Ctrl-C to stop.\n")

    log = writer = None
    if args.csv:
        log = open(args.csv, "w", newline="")
        writer = csv.writer(log)
        writer.writerow(["time_s"] + SENSORS)

    t0 = time.time()
    n = 0
    try:
        while True:
            vals = parse(ser.readline().decode(errors="ignore"))
            if vals is None:
                continue
            n += 1
            t = time.time() - t0
            if writer:
                writer.writerow([f"{t:.4f}"] + [vals[k] for k in SENSORS])
                log.flush()
            if n % 5 == 0:  # redraw ~at a readable rate
                lines = [f"{k:>6} {vals[k]:4d} {bar(vals[k])} {'TOUCH' if vals[k] > args.threshold else ''}"
                         for k in SENSORS]
                sys.stdout.write(f"\x1b[{len(SENSORS) + 1}F" if n > 5 else "")
                sys.stdout.write("\n".join(lines) + f"\n{n / t:6.0f} Hz\x1b[K\n")
                sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()
        if log:
            log.close()
            print(f"\nSaved {n} samples to {args.csv}")


if __name__ == "__main__":
    main()
