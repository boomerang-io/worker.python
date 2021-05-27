from .flow_tools import PropertiesManager


def main():
    print("Hello World!!!")
    print(PropertiesManager())
    print(PropertiesManager.shared_instance)
    print(PropertiesManager.shared_instance.task_input_properties)
    print(PropertiesManager.shared_instance.task_input_properties)
    print(PropertiesManager.shared_instance.task_input_properties)
    print(PropertiesManager.shared_instance.task_input_properties)
    print(f"fere")


if __name__ == '__main__':
    main()
