import json
import pytest
import random
import threading

from script_runner import PythonVersion
from script_runner import PythonScriptRunner


@pytest.mark.python_script_runner
def test_python_version_1():
    assert PythonVersion.PYTHON_0_9 < PythonVersion.PYTHON_2_3
    assert PythonVersion.PYTHON_2_7 >= PythonVersion.PYTHON_2_6
    assert PythonVersion.PYTHON_3_10 > PythonVersion.PYTHON_3_1
    assert PythonVersion.PYTHON_3_2 == PythonVersion.PYTHON_3_2
    assert PythonVersion.PYTHON_3_3 >= PythonVersion.PYTHON_3_3
    assert not PythonVersion.PYTHON_3_6 > PythonVersion.PYTHON_3_9
    assert not PythonVersion.PYTHON_1_0 >= PythonVersion.PYTHON_1_5
    assert not PythonVersion.PYTHON_2_1 <= PythonVersion.PYTHON_1_6
    assert not PythonVersion.PYTHON_1_2 > PythonVersion.PYTHON_1_3
    assert not PythonVersion.PYTHON_2_4 != PythonVersion.PYTHON_2_4


@pytest.mark.python_script_runner
def test_property_access_1():
    python_script_runner = PythonScriptRunner()

    with pytest.raises(InterruptedError, match=r".*once.*script.*completed.*"):
        python_script_runner.output

    with pytest.raises(InterruptedError, match=r".*once.*script.*completed.*"):
        python_script_runner.result

    python_script_runner.run()

    with pytest.raises(InterruptedError, match=r".*executed.*multi.*times.*"):
        python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.output == ""
    assert python_script_runner.result == 0


@pytest.mark.python_script_runner
def test_property_threaded_access_1():
    python_script_runner = PythonScriptRunner()
    thread_count = 10
    success_runs, failed_runs = 0, 0

    def thread_function():
        nonlocal python_script_runner, success_runs, failed_runs

        try:
            python_script_runner.run()
            success_runs = success_runs + 1
        except InterruptedError:
            failed_runs = failed_runs + 1

    threads = [
        threading.Thread(target=thread_function) for _ in range(thread_count)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    assert success_runs == 1
    assert failed_runs == thread_count - 1


@pytest.mark.python_script_runner
def test_property_threaded_access_2():
    python_script_runner = PythonScriptRunner()
    predicted = 0

    def thread_function_run(should_fail: bool):
        nonlocal python_script_runner, predicted

        try:
            python_script_runner.run()
            predicted = predicted + int(not should_fail) * 2 - 1
        except InterruptedError:
            predicted = predicted + int(should_fail) * 2 - 1

    def thread_function_property(should_fail: bool):
        nonlocal python_script_runner, predicted

        try:
            _ = python_script_runner.output
            _ = python_script_runner.result
            predicted = predicted + int(not should_fail) * 2 - 1
        except InterruptedError:
            predicted = predicted + int(should_fail) * 2 - 1

    thread1 = threading.Thread(target=thread_function_property, args=(True, ))
    thread2 = threading.Thread(target=thread_function_property, args=(True, ))
    thread1.start(), thread2.start()
    thread1.join(), thread2.join()

    assert predicted == 2

    thread3 = threading.Thread(target=thread_function_run, args=(False, ))
    thread4 = threading.Thread(target=thread_function_run, args=(False, ))
    thread3.start(), thread4.start()
    thread3.join(), thread4.join()

    assert predicted == 2

    thread5 = threading.Thread(target=thread_function_property, args=(False, ))
    thread6 = threading.Thread(target=thread_function_property, args=(True, ))
    thread5.start(), thread6.start()
    thread5.join(), thread6.join()

    assert predicted == 2


@pytest.mark.python_script_runner
def test_success_result_1():
    a, b = random.randint(0, 100), random.randint(0, 100)
    python_script_runner = PythonScriptRunner(
        script=(f"def sum_func(a, b):\n\tx = a + b\n\treturn x\n\n"
                f"print(\"sum:\", sum_func({a}, {b}))\n\n"))
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 0
    assert f"sum: {a + b}" in python_script_runner.output


@pytest.mark.python_script_runner
def test_success_result_2():
    a, b = random.randint(0, 100), random.randint(0, 100)
    python_script_runner = PythonScriptRunner(
        script=(f"def sum_func(a, b):\n\tx = a + b\n\treturn x\n\n"
                f"exit(sum_func({a}, {b}))"))
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == a + b
    assert python_script_runner.output == ""


@pytest.mark.python_script_runner
def test_failed_result_1():
    python_script_runner = PythonScriptRunner(
        script=("def sum_func(a, b):\n\tx = a + b\n\treturn x\n\n"
                "sum_func(13)"))
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 1
    assert ("missing 1 required positional argument"
            in python_script_runner.output)


@pytest.mark.python_script_runner
def test_failed_result_2():
    python_script_runner = PythonScriptRunner(
        script=("def sum_func(a, b):\n\tx = a + b\n\treturn x\n\n"
                "sum_func1(13, 42)"))
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 1
    assert "'sum_func1' is not defined" in python_script_runner.output


@pytest.mark.python_script_runner
def test_script_python_version_1():
    python_script_runner = PythonScriptRunner(
        python_version=PythonVersion.PYTHON_3_9,
        script="print(sum([1, 2, 3]))")
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 0
    assert "6" in python_script_runner.output


@pytest.mark.python_script_runner
def test_script_python_version_2():
    python_script_runner = PythonScriptRunner(
        python_version=PythonVersion.PYTHON_2_7, script="print sum([1, 2, 3])")
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 0
    assert "6" in python_script_runner.output


@pytest.mark.python_script_runner
def test_script_python_version_3():
    python_script_runner = PythonScriptRunner(
        python_version=PythonVersion.PYTHON_3_9, script="print sum([1, 2, 3])")
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 1
    assert "SyntaxError: invalid syntax" in python_script_runner.output


@pytest.mark.python_script_runner
def test_script_python_arguments_1():
    arguments = ["--help", "me", "another_argument", "--x", "file.txt"]
    python_script_runner = PythonScriptRunner(
        python_version=PythonVersion.PYTHON_3_9,
        script="import sys\n\nprint(sys.argv)",
        cmd_args=" ".join(arguments))
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    assert python_script_runner.result == 0

    for argument in arguments:
        assert argument in python_script_runner.output

    for false_argument in ["this", "arguments", "are_very", "FALSE.txt"]:
        assert false_argument not in python_script_runner.output


@pytest.mark.python_script_runner
def test_script_python_arguments_2():
    arguments = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "X", "Y", "Z"]
    random.shuffle(arguments)

    python_script_runner = PythonScriptRunner(
        python_version=PythonVersion.PYTHON_3_9,
        script=(
            "import sys\n"
            "x=\", \".join('\"' + y + '\"' for y in sorted(sys.argv[1:]))\n"
            "print(f\"[{x}]\")"),
        cmd_args=" ".join(arguments))
    python_script_runner.run()

    print(python_script_runner.output, python_script_runner.result)

    output_list = list(json.loads(python_script_runner.output))

    assert python_script_runner.result == 0
    assert sorted(arguments) == output_list
