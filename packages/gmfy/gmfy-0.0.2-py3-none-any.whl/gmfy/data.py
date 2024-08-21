from __future__ import annotations

from gmfy.constants import LocaleEnum


class EventData:
    def __init__(self, event_type: str, user_id: str, event_action: str | None = None):
        self.event_type = event_type
        self.user_id = user_id
        self.event_action = event_action

    def to_dict(self) -> dict:
        data = {"event_type": self.event_type, "user_id": self.user_id}
        if self.event_action is not None:
            data["event_action"] = self.event_action
        return data


class PaymentData:
    def __init__(
        self,
        amount: dict,
        confirmation: dict,
        user_id: str,
        description: str | None = None,
        locale: LocaleEnum = LocaleEnum.RU,
    ):
        self.amount = amount
        self.confirmation = confirmation
        self.user_id = user_id
        self.description = description
        self.locale = locale

    def to_dict(self):
        return {
            "amount": self.amount,
            "confirmation": self.confirmation,
            "userId": self.user_id,
            "description": self.description,
            "locale": self.locale,
        }
