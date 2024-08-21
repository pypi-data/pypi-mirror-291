from __future__ import annotations

from functools import reduce
from operator import or_
from typing import TypeAlias

from pydantic import Field, RootModel

from gmfy.base_events import BaseEvent
from gmfy.utils import ClassCollector


def collect_event_classes() -> list[type]:
    collector = ClassCollector(BaseEvent)
    collector.collect_classes()
    imported_classes = collector.import_classes()
    BaseEvent.model_config["children_list"].extend(imported_classes)  # type: ignore[typeddict-item]
    return imported_classes


try:
    collect_event_classes()
    Events: TypeAlias = reduce(or_, BaseEvent.model_config["children_list"])  # type: ignore[typeddict-item, valid-type]
except TypeError as error:
    raise TypeError(
        "It seems you're encountering an issue with reduce() due to an empty iterable. "
        "Ensure you've created your events by inheriting from BaseEvents. Please create"
        " a Python package and add a file where you initialize your classes that extend"
        " BaseEvents to avoid this error.",
    ) from error


class EventManager(RootModel):
    root: list[Events] = Field(discriminator="event_type")


class SingleEventManager(RootModel):
    root: Events = Field(discriminator="event_type")
