def get_settings(filename: str = "secret.env"):
    settings = {}
    with open(filename) as f:
        for line in f.readlines():
            key, value = line.split("==")
            settings[key] = value
    return settings
