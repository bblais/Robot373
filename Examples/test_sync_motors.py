from Robot373 import *

left,right=Motors("ab")



# Synchronization settings
TARGET_SPEED = 50  # Target speed for motors
KP = 0.5  # Proportional gain for speed correction

T=Timer()

try:
    # Set both motors to the target speed initially
    BP.set_motor_dps(left.port, TARGET_SPEED)
    BP.set_motor_dps(right.port, TARGET_SPEED)

    while True:
        # Read motor encoder values
        left_position = left.position
        right_position = right.position

        # Calculate position error
        error = left_position - right_position

        # Adjust right motor speed based on error
        correction = KP * error
        BP.set_motor_dps(right.port, TARGET_SPEED + correction)

        # Small delay to avoid excessive CPU usage
        time.sleep(0.05)


        if left_position>100:  # stop after a certain distance
            break

        if T.value>5:  # stop after 5 seconds
            break

except KeyboardInterrupt:
    pass

# Stop motors on program exit
left.power=0
right.power=0

Shutdown()