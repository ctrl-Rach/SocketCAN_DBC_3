import can
import time
import math
import random


# ---------------------------------------------------------
# SocketCAN configuration
# ---------------------------------------------------------
CHANNEL = "vcan0"


# ---------------------------------------------------------
# Create CAN bus
# ---------------------------------------------------------
bus = can.Bus(
    interface="socketcan",
    channel=CHANNEL
)


# ---------------------------------------------------------
# Initial vehicle values
# ---------------------------------------------------------
speed = 0.0
rpm = 800.0
coolant = 25.0
fuel = 100.0
battery = 14.2
ambient = 25.0

start_time = time.time()


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------
def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


# ---------------------------------------------------------
# Message 0x100
# Vehicle Speed + Engine RPM
# ---------------------------------------------------------
def encode_vehicle_status_1(speed, rpm):

    # Vehicle Speed:
    # Scale = 0.01 km/h
    raw_speed = int(speed / 0.01)

    # Engine RPM:
    # Scale = 1 rpm
    raw_rpm = int(rpm)

    data = [
        raw_speed & 0xFF,
        (raw_speed >> 8) & 0xFF,

        raw_rpm & 0xFF,
        (raw_rpm >> 8) & 0xFF,

        0x00,
        0x00,
        0x00,
        0x00
    ]

    return data


# ---------------------------------------------------------
# Message 0x101
# Coolant Temperature + Fuel Level
# ---------------------------------------------------------
def encode_vehicle_status_2(coolant, fuel):

    # Coolant:
    # Physical = Raw - 40
    # Therefore Raw = Physical + 40
    raw_coolant = int(coolant + 40)

    # Fuel:
    # Scale = 0.5 %
    raw_fuel = int(fuel / 0.5)

    data = [
        raw_coolant & 0xFF,
        raw_fuel & 0xFF,

        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00
    ]

    return data


# ---------------------------------------------------------
# Message 0x102
# Battery Voltage
# ---------------------------------------------------------
def encode_battery_status(battery):

    # Scale = 0.01 V
    raw_battery = int(battery / 0.01)

    data = [
        raw_battery & 0xFF,
        (raw_battery >> 8) & 0xFF,

        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00
    ]

    return data


# ---------------------------------------------------------
# Message 0x103
# Ambient Temperature
# ---------------------------------------------------------
def encode_ambient_status(ambient):

    # DBC:
    # Scale = 1
    # Offset = -40
    #
    # Physical = Raw - 40
    #
    # Therefore:
    # Raw = Physical + 40

    raw_ambient = int(ambient + 40)

    data = [
        raw_ambient & 0xFF,

        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00
    ]

    return data


# ---------------------------------------------------------
# Main transmission loop
# ---------------------------------------------------------
print("Vehicle CAN transmitter started.")
print("Channel:", CHANNEL)
print("Messages: 0x100, 0x101, 0x102, 0x103")
print("Press Ctrl+C to stop.\n")


try:

    while True:

        elapsed = time.time() - start_time


        # -------------------------------------------------
        # Vehicle Speed
        # -------------------------------------------------
        speed = 60 + 55 * math.sin(elapsed / 8)
        speed = clamp(speed, 0, 120)


        # -------------------------------------------------
        # Engine RPM
        # -------------------------------------------------
        rpm = 1000 + speed * 30
        rpm += 150 * math.sin(elapsed / 2)
        rpm = clamp(rpm, 800, 5000)


        # -------------------------------------------------
        # Coolant Temperature
        # -------------------------------------------------
        coolant = 75 + 15 * math.sin(elapsed / 20)
        coolant = clamp(coolant, 20, 120)


        # -------------------------------------------------
        # Fuel Level
        # -------------------------------------------------
        fuel -= 0.01
        fuel = clamp(fuel, 0, 100)


        # -------------------------------------------------
        # Battery Voltage
        # -------------------------------------------------
        battery = 13.8 + 0.4 * math.sin(elapsed / 5)
        battery += random.uniform(-0.05, 0.05)
        battery = clamp(battery, 11, 15)


        # -------------------------------------------------
        # Ambient Temperature
        # -------------------------------------------------
        ambient = 25 + 10 * math.sin(elapsed / 30)
        ambient += random.uniform(-0.2, 0.2)
        ambient = clamp(ambient, -20, 60)


        # -------------------------------------------------
        # Send 0x100
        # -------------------------------------------------
        message_100 = can.Message(
            arbitration_id=0x100,
            data=encode_vehicle_status_1(speed, rpm),
            is_extended_id=False
        )

        bus.send(message_100)


        # -------------------------------------------------
        # Send 0x101
        # -------------------------------------------------
        message_101 = can.Message(
            arbitration_id=0x101,
            data=encode_vehicle_status_2(coolant, fuel),
            is_extended_id=False
        )

        bus.send(message_101)


        # -------------------------------------------------
        # Send 0x102
        # -------------------------------------------------
        message_102 = can.Message(
            arbitration_id=0x102,
            data=encode_battery_status(battery),
            is_extended_id=False
        )

        bus.send(message_102)


        # -------------------------------------------------
        # Send 0x103
        # -------------------------------------------------
        message_103 = can.Message(
            arbitration_id=0x103,
            data=encode_ambient_status(ambient),
            is_extended_id=False
        )

        bus.send(message_103)


        # -------------------------------------------------
        # Display values
        # -------------------------------------------------
        print(
            f"Speed: {speed:6.2f} km/h | "
            f"RPM: {rpm:6.0f} rpm | "
            f"Coolant: {coolant:5.1f} °C | "
            f"Fuel: {fuel:5.1f} % | "
            f"Battery: {battery:4.2f} V | "
            f"Ambient: {ambient:5.1f} °C"
        )


        # 100 ms transmission period
        time.sleep(0.1)


except KeyboardInterrupt:

    print("\nTransmitter stopped.")


finally:

    bus.shutdown()
