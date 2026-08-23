
# AI-Assisted DBC Generation and CAN Data Visualization

This project demonstrates the design, transmission, decoding, and visualization of automotive CAN signals using **SocketCAN, Python, DBC, and SavvyCAN**.

## Features

* AI-assisted DBC generation and review
* SocketCAN virtual CAN network using `vcan0`
* Python-based CAN transmitter
* DBC-based signal decoding
* Real-time CAN visualization using SavvyCAN
* Raw CAN vs decoded signal comparison
* DBC scaling modification experiment
* Addition of Ambient Temperature signal

## CAN Messages

| CAN ID  | Message        | Signals                         |
| ------- | -------------- | ------------------------------- |
| `0x100` | VehicleStatus1 | Vehicle Speed, Engine RPM       |
| `0x101` | VehicleStatus2 | Coolant Temperature, Fuel Level |
| `0x102` | BatteryStatus  | Battery Voltage                 |
| `0x103` | AmbientStatus  | Ambient Temperature             |

## Tools Used

* Ubuntu Linux
* SocketCAN / `vcan0`
* Python
* `python-can`
* `cantools`
* SavvyCAN
* ChatGPT

## Project Flow

```text
Signal Definition
       ↓
DBC Creation
       ↓
Python CAN Transmitter
       ↓
SocketCAN (vcan0)
       ↓
Raw CAN Frames
       ↓
DBC Decoding
       ↓
SavvyCAN Visualization
```

## Run

Start the virtual CAN interface:

```bash
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

Run the transmitter:

```bash
python3 can_transmitter.py
```

Monitor raw CAN traffic:

```bash
candump vcan0
```

Run the decoder:

```bash
python3 can_decoder.py
```

The DBC file `vehicle_network.dbc` is used to decode the transmitted CAN messages into engineering values.

## Result

The system successfully visualizes:

**Vehicle Speed, Engine RPM, Coolant Temperature, Fuel Level, Battery Voltage, and Ambient Temperature** in real time.

Developed as part of an automotive communication networks assignment demonstrating an end-to-end CAN/DBC workflow.
