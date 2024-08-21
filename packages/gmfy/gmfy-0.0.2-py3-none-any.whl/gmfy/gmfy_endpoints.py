from enum import StrEnum

import settings


class GMFYEndpoints(StrEnum):
    events = f"{settings.GMFY_URL}v1/events/"
    events_batch = url = f"{settings.GMFY_URL}v1/events/batch/"
    payments = f"{settings.GMFY_URL}v1/payments/"
    version = f"{settings.GMFY_URL}v1/version/"
    users = f"{settings.GMFY_URL}v1/users/"
    ratings = f"{settings.GMFY_URL}v1/ratings/"
    notifications = f"{settings.GMFY_URL}v1/notifications/"
    challenges = f"{settings.GMFY_URL}v1/challenges/"
    badges = f"{settings.GMFY_URL}v1/badges/"
