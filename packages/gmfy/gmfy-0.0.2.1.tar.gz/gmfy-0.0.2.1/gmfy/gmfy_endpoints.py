from enum import StrEnum


class GMFYEndpoints(StrEnum):
    events = "v1/events/"
    events_batch = url = "v1/events/batch/"
    payments = "v1/payments/"
    version = "v1/version/"
    users = "v1/users/"
    ratings = "v1/ratings/"
    notifications = "v1/notifications/"
    challenges = "v1/challenges/"
    badges = "v1/badges/"
