from django.utils.translation import ugettext_lazy as _


def get_wind_direction(degree):
    """
    Get wind direction from degree

    Args:
        degree: wind direction in degree
    Returns: wind direction. eg: Southeast
    """
    val = int((degree / 22.5) + 0.5)
    directions = [
        _('North'),
        _('North-northeast'),
        _('Northeast'),
        _('East-northeast'),
        _('East'),
        _('East-southeast'),
        _('Southeast'),
        _('South-southeast'),
        _('South'),
        _('South-southwest'),
        _('Southwest'),
        _('West-southwest'),
        _('West'),
        _('West-northwest'),
        _('Northwest'),
        _('North-northwest'),
    ]
    return directions[(val % 16)]
