import logging

SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")
def success(self, message, *args, **kws):
    if self.isEnabledFor(SUCCESS_LEVEL):
        # Yes, logger takes its '*args' as 'args'.
        self._log(SUCCESS_LEVEL, message, args, **kws)
logging.Logger.success = success

