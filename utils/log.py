import logging
import logging.config

logging.config.fileConfig("utils/etc/log.conf")
level = "DEBUG"

class Log:
    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def get(self, level):
        self.set(level)
        return self.logger

    def set(self, level):
        self.logger.info("set LOG level %s" % level)
        if level == "DEBUG":
            self.logger.setLevel(logging.DEBUG)
        elif level == "INFO":
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.ERROR)

log = Log("Server").get(level)

if __name__ == '__main__':
    log = Log("root").get("DEBUG")
    log.debug("debug")
