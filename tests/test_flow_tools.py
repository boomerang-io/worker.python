import pytest
import mock

from flow_tools import PropertyManager


@pytest.mark.flow_tools
def test_property_manager_instances_1():
    inst1 = PropertyManager()
    inst2 = PropertyManager()

    print(inst1)
    print(inst2)
    print(PropertyManager.shared)

    assert inst1 is not inst2
    assert PropertyManager.shared is PropertyManager.shared
    assert PropertyManager() is not PropertyManager.shared


@pytest.mark.flow_tools
@mock.patch("flow_tools._property_manager.constants.TASK_INPUT_FILES",
            ["tests/resources/test_input_1.properties"])
def test_task_input_properties_1():
    properties = PropertyManager().task_input_properties

    print(properties)

    assert len(properties) == 4
    assert "pythonVersion" in properties
    assert "pythonPackages" in properties
    assert "pythonScript" in properties
    assert "pythonArguments" in properties


@pytest.mark.flow_tools
@mock.patch("flow_tools._property_manager.constants.TASK_INPUT_FILES",
            ["tests/resources/test_input_2.properties"])
def test_task_input_properties_2():
    properties = PropertyManager().task_input_properties

    print(properties)

    assert len(properties) == 3
    assert "pythonVersion" in properties
    assert "pythonScript" in properties
    assert "key_with_comment" in properties


@pytest.mark.flow_tools
@mock.patch("flow_tools._property_manager.constants.TASK_INPUT_FILES",
            ["tests/resources/test_input_3.properties"])
def test_task_input_properties_3():
    properties = PropertyManager().task_input_properties

    print(properties)

    assert len(properties) == 0


@pytest.mark.flow_tools
@mock.patch("flow_tools._property_manager.constants.TASK_INPUT_FILES",
            ["tests/resources/test_input_4.properties"])
def test_task_input_properties_4():
    properties = PropertyManager().task_input_properties

    print(properties)

    assert len(properties) == 0


@pytest.mark.flow_tools
@mock.patch("flow_tools._property_manager.constants.TASK_INPUT_FILES",
            ["tests/resources/test_input_5.properties"])
def test_task_input_properties_5():
    properties = PropertyManager().task_input_properties

    print(properties)

    assert len(properties) == 5
    assert "key_with_comment" not in properties
    assert "pythonVersion" in properties
    assert "pythonPackages" in properties
    assert "pythonScript" in properties
    assert "pythonArguments" in properties

    assert "Python 3" in properties["pythonVersion"]
    assert all(package in properties["pythonPackages"]
               for package in ["DecryptLogin", "clepy", "retexto"])
    assert "class Solution:\n    def " in properties["pythonScript"]


@pytest.mark.flow_tools
@mock.patch("flow_tools._property_manager.constants.TASK_INPUT_FILES", [
    "tests/resources/inexisting_file.properties",
    "tests/resources/also_inexistent.txt",
    "tests/resources/test_input_3.properties",
    "tests/resources/test_input_1.properties",
    "tests/resources/test_input_5.properties"
])
def test_task_input_properties_order_1():
    properties = PropertyManager().task_input_properties

    print(properties)

    assert len(properties) == 0


@pytest.mark.flow_tools
def test_properties_from_file_1():
    properties = PropertyManager.shared.get_properties_from_file(
        "tests/resources/test_input_2.properties")

    print(properties)

    assert len(properties) == 3

    assert properties["pythonVersion"] == "Python 2 (version 2.7.16) "
    assert "return a + b" in properties["pythonScript"]
    assert properties["key_with_comment"] == "Value # Comment"


@pytest.mark.flow_tools
def test_properties_from_file_2():
    properties = PropertyManager.shared.get_properties_from_file(
        "tests/resources/test_input_5.properties")

    print(properties)

    assert len(properties) == 5

    assert properties["pythonVersion"] == "Python 3 (version 3.9.5) "
    assert properties["pythonArguments"] == ("LLRLLGGGLLRGLLGRLLRGLGGLRGLLLRLR"
                                             "LRLGRLRLRLRRRRRLGLRGLRGL")
