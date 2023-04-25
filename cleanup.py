import serial
import time

def format_command(joint_angles, safemode, brake, gripper, dt=1000):
    (j1, j2, j3, j4, j5, j6) = joint_angles
    return f"angle: j1: {j1}, j2: {j2}, j3: {j3}, j4: {j4}, j5: {j5}, j6: {j6}, safemode: {safemode}, brake: {brake}, gripper: {gripper}, dt: {dt}\r\n"

def send_command(ser, command):
    print("command:  " + command)
    ser.write(command.encode())

def read_current_angles(ser):
    ser.write(b"\r\n")
    response = ser.readline().decode().strip()
    print("response:  " + response)
    return response

def parse_response(response):
    angles = angles.split(",")
    # split each string into a list of strings and set the starting variables. format to float and int
    j1 = float(angles[0].split(":")[2])
    j2 = float(angles[1].split(":")[1])
    j3 = float(angles[2].split(":")[1])
    j4 = float(angles[3].split(":")[1])
    j5 = float(angles[4].split(":")[1])
    j6 = float(angles[5].split(":")[1])
    safemode = int(angles[6].split(":")[1])
    brake = int(angles[7].split(":")[1])
    gripper = int(angles[8].split(":")[1])

    return (j1, j2, j3, j4, j5, j6, safemode, brake, gripper)

def main():
    with serial.Serial('COM18', 576000, timeout=1) as ser:
        response = read_current_angles(ser)
        (j1, j2, j3, j4, j5, j6, safemode, brake, gripper) = parse_response(response)
        print(f"Current state: j1: {j1}, j2: {j2}, j3: {j3}, j4: {j4}, j5: {j5}, j6: {j6}, safemode: {safemode}, brake: {brake}, gripper: {gripper}")

        while True:
            user_input = input("Enter 'brake' to toggle brake or 'current' to read angles (type 'exit' to quit): ")

            if user_input.lower() == "brake":
                brake = 1 - brake
                command = format_command((j1, j2, j3, j4, j5, j6), safemode, brake, gripper)
                send_command(ser, command)

            elif user_input.lower() == "current":
                response = read_current_angles(ser)
                (j1, j2, j3, j4, j5, j6, safemode, brake, gripper) = parse_response(response)
                print(f"Current state: j1: {j1}, j2: {j2}, j3: {j3}, j4: {j4}, j5: {j5}, j6: {j6}, safemode: {safemode}, brake: {brake}, gripper: {gripper}")

            elif user_input.lower() == "safemode":
                safemode = 1 - safemode
                command = format_command((j1, j2, j3, j4, j5, j6), safemode, brake, gripper)
                send_command(ser, command)

            elif user_input.lower() == "exit":
                break
            else:
                print("Invalid command. Try again.")

if __name__ == "__main__":
    main()
