import can
import cantools


# Load DBC database
db = cantools.database.load_file("vehicle_network.dbc")


# Connect to SocketCAN
bus = can.Bus(
    interface="socketcan",
    channel="vcan0"
)


print("DBC decoder started.")
print("Listening on vcan0...\n")


try:

    while True:

        message = bus.recv()

        if message is None:
            continue

        try:

            # Decode message using DBC
            decoded = db.decode_message(
                message.arbitration_id,
                message.data
            )

            print(
                f"ID: 0x{message.arbitration_id:03X} "
                f"-> {decoded}"
            )

        except Exception:

            # Ignore messages not defined in DBC
            pass


except KeyboardInterrupt:

    print("\nDecoder stopped.")


finally:

    bus.shutdown()
