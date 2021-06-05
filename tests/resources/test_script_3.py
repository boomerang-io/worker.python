import sys


# Function for nth Fibonacci number
def fibonacci(n):

    # Check if input is 0 then it will return null
    if n < 0:
        return None

    # Check if n is 0 then it will return 0
    elif n == 0:
        return 0

    # Check if n is 1 or 2 it will return 1
    elif n == 1 or n == 2:
        return 1

    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# Get algorithm input from command line arguments (if any)
print "Command line arguments: {}".format(sys.argv)

# Default inputs
inputs = [14]

# Get inputs from command line arguments
if len(sys.argv) > 1:
    inputs = map(int, sys.argv[1:])

# Execute the algorithm for each input
for input in inputs:

    output = fibonacci(input)
    print "Input: {}\nOutput: {}".format(input, output)
