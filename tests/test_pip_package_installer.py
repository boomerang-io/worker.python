import os
import re
import pytest
import threading

from script_runner import PipPackageInstaller


@pytest.mark.pip_package_installer
def test_property_access_1():
    pip_package_installer = PipPackageInstaller()

    with pytest.raises(InterruptedError, match=r".*once.*script.*completed.*"):
        pip_package_installer.output

    with pytest.raises(InterruptedError, match=r".*once.*script.*completed.*"):
        pip_package_installer.result

    pip_package_installer.run()

    with pytest.raises(InterruptedError, match=r".*packages.*installed.*"):
        pip_package_installer.run()

    print(pip_package_installer.output, pip_package_installer.result)

    assert pip_package_installer.result == 0


@pytest.mark.pip_package_installer
def test_property_threaded_access_1():
    pip_package_installer = PipPackageInstaller()
    thread_count = 10
    success_runs, failed_runs = 0, 0

    def thread_function():
        nonlocal pip_package_installer, success_runs, failed_runs

        try:
            pip_package_installer.run()
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


@pytest.mark.pip_package_installer
def test_property_threaded_access_2():
    pip_package_installer = PipPackageInstaller()
    predicted = 0

    def thread_function_run(should_fail: bool):
        nonlocal pip_package_installer, predicted

        try:
            pip_package_installer.run()
            predicted = predicted + int(not should_fail) * 2 - 1
        except InterruptedError:
            predicted = predicted + int(should_fail) * 2 - 1

    def thread_function_property(should_fail: bool):
        nonlocal pip_package_installer, predicted

        try:
            _ = pip_package_installer.output
            _ = pip_package_installer.result
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


@pytest.mark.pip_package_installer
@pytest.mark.parametrize("packages", [[("requests", "2.18.4")],
                                      [("requests", "2.18.4"),
                                       ("random-profile", "0.0.5"),
                                       ("empty-package", "0.0.1")],
                                      [("empty-package", "0.0.3"),
                                       ("rsokl-dummy", "0.1.2")]])
def test_install_packages_1(packages):
    packages_to_install = "\n".join(f"{package}=={version}"
                                    for package, version in packages)
    pip_package_installer = PipPackageInstaller(packages=packages_to_install)
    pip_package_installer.run()

    print(pip_package_installer.output, pip_package_installer.result)

    assert pip_package_installer.result == 0

    for package, version in packages:
        sys_pip_packages = os.popen("pip list").read()
        pattern = f"{re.escape(package)}.*{re.escape(version)}"

        assert bool(re.search(pattern, sys_pip_packages))


@pytest.mark.pip_package_installer
@pytest.mark.parametrize("package, version",
                         [("inexistent_package", "0.69.42.0"),
                          ("some_random_XXX_pack", "1.2.3"),
                          ("requests", "10.99.33")])
def test_install_packages_2(package, version):
    package_to_install = f"{package}=={version}"
    pip_package_installer = PipPackageInstaller(packages=package_to_install)
    pip_package_installer.run()

    print(pip_package_installer.output, pip_package_installer.result)

    assert pip_package_installer.result == 1
    assert "No matching distribution found" in pip_package_installer.output
