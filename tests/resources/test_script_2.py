import sys


class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        result = "0"

        if num1 == "0" or num2 == "0":
            return result

        for i in range(len(num1)):
            result = self.__sum(
                self.__multiplySingle(num2, int(num1[-i - 1])) + "0" * i,
                result)
        return result

    def __multiplySingle(self, num: str, multiplier: int) -> str:
        result, mem = "", 0

        for i in range(len(num)):
            n_mul = int(num[-i - 1]) * multiplier + mem
            result = str(n_mul % 10) + result
            mem = 0 if n_mul < 10 else n_mul // 10

        return str(mem) + result if mem > 0 else result

    def __sum(self, num1: str, num2: str) -> str:
        result, mem = "", 0

        for i in range(max(len(num1), len(num2))):
            n1 = int(num1[-i - 1]) if i < len(num1) else 0
            n2 = int(num2[-i - 1]) if i < len(num2) else 0
            n3 = n1 + n2 + mem

            result = str(n3 % 10) + result
            mem = 0 if n3 < 10 else n3 // 10

        return str(mem) + result if mem > 0 else result


# Get algorithm input from command line arguments (if any)
print(f"Command line arguments: {sys.argv}")

# Default inputs
inputs = [("12", "72")]

# Get inputs from command line arguments
if len(sys.argv) > 2:
    inputs = [(sys.argv[i * 2 + 1], sys.argv[i * 2 + 2])
              for i in range((len(sys.argv) - 1) // 2)]

# Execute the algorithm for each input
for input in inputs:

    output = Solution().multiply(*input)
    print(f"Input: {input}\nOutput: {output}")
