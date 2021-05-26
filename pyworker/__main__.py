import os
import sys

from flow_utils import TaskUtils


def main():
    print("Hello World!!!")
    # print(sys.argv)
    # print(os.system("cat /props/task.input.properties"))
    # print(os.system("cat props/task.input.properties"))

    print(TaskUtils.input_properties)
    print(TaskUtils.input_properties)
    # TaskUtils.input_properties = {"test": 123}
    print(TaskUtils.input_properties)


if __name__ == '__main__':
    main()
