import logging


def configure_logging():
    __custom_level_names = [(logging.DEBUG, "๐ฌ"), (logging.INFO, "๐ก"),
                            (logging.WARNING, "โ ๏ธ"), (logging.ERROR, "๐ซ"),
                            (logging.CRITICAL, "๐งจ")]

    # Configure the logging system
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    # Update logging level names
    for level, icon in __custom_level_names:
        logging.addLevelName(level, f"{icon}{logging.getLevelName(level)}")
