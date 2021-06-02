import logging


def configureLogging():
    __custom_level_names = [(logging.DEBUG, "🔬"), (logging.INFO, "💡"),
                            (logging.WARNING, "⚠️"), (logging.ERROR, "🚫"),
                            (logging.CRITICAL, "🧨")]

    # Configure the logging system
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Update logging level names
    for level, icon in __custom_level_names:
        logging.addLevelName(level, f"{icon}{logging.getLevelName(level)}")
