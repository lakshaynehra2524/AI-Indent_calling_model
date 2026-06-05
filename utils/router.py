def route_intent(intent):

    """
    Maps predicted intent
    to UI section names.
    """

    routes = {

        "open_call": "call",
        "open_mail": "mail",
        "open_camera": "camera",
        "open_music": "music",
        "open_alarm": "alarm",
        "open_calculator": "calculator",
        "open_running": "running",
        "open_water_tracker": "water",
        "open_sleep_tracker": "sleep",
        "open_flashlight": "flashlight"

    }

    return routes.get(intent, "home")