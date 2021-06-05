def pytest_configure(config):

    # Declare custom markers to avoid `PytestUnknownMarkWarning`
    config.addinivalue_line("markers", "flow_tools: Flow tools testing set.")
    config.addinivalue_line(
        "markers", "python_script_runner: Python script runner testing set.")
    config.addinivalue_line(
        "markers", "pip_package_installer: Pip package installer testing set.")
