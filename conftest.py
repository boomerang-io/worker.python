def pytest_configure(config):

    # Declare custom markers to avoid `PytestUnknownMarkWarning`
    config.addinivalue_line("markers", "flow_tools: Flow tools testing set.")
