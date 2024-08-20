class LightlyTrainError(Exception):
    pass


class UnknownModelError(LightlyTrainError):
    pass


class ConfigError(LightlyTrainError):
    pass


class ConfigUnknownKeyError(ConfigError):
    pass


class ConfigValidationError(ConfigError):
    pass


class ConfigMissingKeysError(ConfigError):
    pass
