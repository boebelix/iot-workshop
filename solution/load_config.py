import os


def check_config() -> bool:
    """
    Check enviroment variables are exist
    :return: True if config is valid, False otherwise
    """
    MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST")
    MQTT_BROKER_USERNAME = os.getenv("MQTT_BROKER_USERNAME")
    MQTT_BROKER_PASSWORT = os.getenv("MQTT_BROKER_PASSWORT")

    if (
            MQTT_BROKER_HOST is None
            or MQTT_BROKER_USERNAME is None
            or MQTT_BROKER_PASSWORT is None
    ):
        return False

    return True
