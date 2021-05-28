import logging


class LoggerConf(object):
    @classmethod
    def configure(cls):

        logging.basicConfig()
        custom_level_names = [(logging.DEBUG, "🔬"), (logging.INFO, "💡"),
                              (logging.WARNING, "⚠️"), (logging.ERROR, "🚫"),
                              (logging.CRITICAL, "🧨")]

        for level, icon in custom_level_names:
            logging.addLevelName(level,
                                 f"{icon}:{logging.getLevelName(level)}")

    @classmethod
    def loggerForModule(cls, module_name: str):
        modules_map = {"__main__": "PyWorker"}
        return logging.getLogger(modules_map.get(module_name, module_name))
