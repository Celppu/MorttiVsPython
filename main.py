import serial
import time

def set_brake(ser, safemode_state, brake_state, gripper_state, joint_angles):
    (j1, j2, j3, j4, j5, j6) = joint_angles
    brake = 1 if brake_state else 0
    safemode = 1 if safemode_state else 0
    gripper = 1 if gripper_state else 0
    #command = f"brake: {brake} \r\n"
    command = f"angle: j1: {j1}, j2: {j2}, j3: {j3}, j4: {j4}, j5: {j5}, j6: {j6}, safemode: {safemode}, brake: {brake}, gripper: {gripper}, dt: 1000\r\n"
    print("command:  " + command)
    ser.write(command.encode())

def read_current_angles(ser):
    #ser.write(b"current\r\n")
    command = "\r\n"
    ser.write(command.encode())
    response = ser.readline().decode().strip()
    print("response:  " + response)
    return response

# read current and parse states from robot
def read_current_states(ser ):
    command = "\r\n"
    ser.write(command.encode())
    response = ser.readline().decode().strip()
    print("response:  " + response)
    # format is "angle: j1: %f, j2: %f, j3: %f, j4: %f, j5: %f, j6: %f, safemode: %i, brake: %i, gripper: %i"
    # split the string into a list of strings
    angles = response.split(",")
    # split each string into a list of strings
    j1 = angles[0].split(":")
    j2 = angles[1].split(":")
    j3 = angles[2].split(":")
    j4 = angles[3].split(":")
    j5 = angles[4].split(":")
    j6 = angles[5].split(":")
    safemode = angles[6].split(":")
    brake = angles[7].split(":")
    gripper = angles[8].split(":")
    # print startin robot state to terminal. print the serial answer and the parsed variables for debugging
    print("Current angles:", angles)
    print("j1: ", j1)
    print("j2: ", j2)
    print("j3: ", j3)
    print("j4: ", j4)
    print("j5: ", j5)
    print("j6: ", j6)
    print("safemode: ", safemode)
    print("brake: ", brake)
    print("gripper: ", gripper)
    print("response:  " + response)
    print("\n")
    return (j1, j2, j3, j4, j5, j6, safemode, brake, gripper)
    

def send_buffer_command(ser):
    buffer_command = "buffer\r\n"
    ser.write(buffer_command.encode())
    response = ser.readline().decode().strip()
    return response

# serial, safemodestate, brake, gripper an tuple of all joint angles. similar input to brake function
def set_safemode(ser, safemode_state, brake_state, gripper_state, joint_angles):
    (j1, j2, j3, j4, j5, j6) = joint_angles
    safemode = 1 if safemode_state else 0
    brake = 1 if brake_state else 0
    gripper = 1 if gripper_state else 0
    command = f"angle: j1: {j1}, j2: {j2}, j3: {j3}, j4: {j4}, j5: {j5}, j6: {j6}, safemode: {safemode}, brake: {brake}, gripper: {gripper}, dt: 1000\r\n"
    print("command:  " + command)
    ser.write(command.encode())

def main():
    # Replace 'COM_PORT' with the appropriate port for your robot
    with serial.Serial('COM18', 576000, timeout=1) as ser:
        # Read current angles and display them
        angles = read_current_angles(ser)
        print("Current angles:", angles)

        brake_state = False
        safemode_state = True
        # set starting variables to for j1  - j6 to  j1: -0.130014, j2: 1.936770, j3: -3.335180, j4: -0.033514, j5: 0.966732, j6: 1.616889
        # Hard coded angles when robot was tested 24/04/2023 DANGER 
        j1 = -0.130014
        j2 = 1.936770
        j3 = -3.335180
        j4 = -0.033514
        j5 = 0.966732
        j6 = 1.616889

        #read current angles, brakes and safemode from robot, and set them to the starting variables
        angles = read_current_angles(ser)
        # format is "angle: j1: %f, j2: %f, j3: %f, j4: %f, j5: %f, j6: %f, safemode: %i, brake: %i, gripper: %i"
        # split the string into a list of strings
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


        # print startin robot state to terminal. print the serial answer and the parsed variables for debugging
        print("Current angles:", angles)
        print("j1: ", j1)
        print("j2: ", j2)
        print("j3: ", j3)
        print("j4: ", j4)
        print("j5: ", j5)
        print("j6: ", j6)
        print("safemode: ", safemode)
        print("brake: ", brake)
        print("gripper: ", gripper)
        
        while True:
            user_input = input("Enter 'brake' to toggle brake or 'current' to read angles (type 'exit' to quit): ")

            if user_input.lower() == "brake":
                brake_state = not brake_state
                jointangles = (j1, j2, j3, j4, j5, j6)
                set_brake(ser, safemode_state= safemode_state, brake_state= brake_state, gripper_state= gripper, joint_angles= jointangles)

            elif user_input.lower() == "current":
                angles = read_current_angles(ser)
                print("Current angles:", angles)

            elif user_input.lower() == "buffer":
                angles = send_buffer_command(ser)
                print("buffer:", angles)

            elif user_input.lower() == "safemode":
                safemode_state = not safemode_state
                jointangles = (j1, j2, j3, j4, j5, j6)
                set_safemode(ser, safemode_state= safemode_state, brake_state= brake_state, gripper_state= gripper, joint_angles= jointangles)

            #read current states and set them to the starting variables
            elif user_input.lower() == "read":
                (j1, j2, j3, j4, j5, j6, safemode, brake, gripper) = read_current_states(ser)

            elif user_input.lower() == "exit":
                break

            else:
                print("Invalid command. Try again.")

if __name__ == "__main__":
    main()

# 0 pi/2 -pi/2 0 0 0