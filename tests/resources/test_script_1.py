import sys


class Solution:
    def isRobotBounded(self, instructions: str) -> bool:
        # Position is a tuple (X, Y) and directions are:
        # 0 - North
        # 1 - East
        # 2 - South
        # 3 - West
        position, direction = (0, 0), 0

        # Execute all steps and compute final position
        for instruction in instructions:

            if instruction == "G":

                # Move forward, compute new position
                if direction == 0:
                    position = (position[0], position[1] - 1)
                elif direction == 1:
                    position = (position[0] + 1, position[1])
                elif direction == 2:
                    position = (position[0], position[1] + 1)
                elif direction == 3:
                    position = (position[0] - 1, position[1])

            elif instruction == "L":

                # Rotate left
                direction = (direction - 1) % 4

            elif instruction == "R":

                # Rotate right
                direction = (direction + 1) % 4

        # If final position is at (0, 0) without considering the direction or
        # the robot's position has changed along its direction, than the robot
        # moves in a circle plane
        return position == (0, 0) or direction != 0


# Get algorithm input from command line arguments (if any)
print(f"Command line arguments: {sys.argv}")

# Default inputs
inputs = ["RLLGGLRGLGLLLGRLRLRLRRRRLRLGRLLLGGL"]

# Get inputs from command line arguments
if len(sys.argv) > 1:
    inputs = sys.argv[1:]

# Execute the algorithm for each input
for input in inputs:

    output = Solution().isRobotBounded(input)
    print(f"Input: {input}\nOutput: {output}")
