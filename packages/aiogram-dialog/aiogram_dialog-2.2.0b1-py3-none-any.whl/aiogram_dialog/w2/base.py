from dataclasses import dataclass
from typing import Generic, TypeVar, List, Protocol, Optional

from aiogram import Router
from aiogram.types import KeyboardButton, InlineKeyboardButton

from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

ContentT = TypeVar('ContentT')


@dataclass(kw_only=True)
class RenderedItem(Generic[ContentT]):
    type: object
    content: ContentT


KEYBOARD_TYPE = object()
TEXT_TYPE = object()
MEDIA_TYPE = object()
KeyType = KeyboardButton | InlineKeyboardButton
KeyboardContent = List[List[KeyType]]


@dataclass
class Keyboard(RenderedItem[KeyboardContent]):
    type = KEYBOARD_TYPE


@dataclass
class Text(RenderedItem[str]):
    type = TEXT_TYPE


class Media(RenderedItem[MediaAttachment]):
    type = MEDIA_TYPE


WidgetT = TypeVar('WidgetT')


class ManagedWidget(Generic[WidgetT]):
    def __init__(self, widget: WidgetT, manager: DialogManager) -> None:
        self._widget = widget
        self._manager = manager


ManagedT = TypeVar('ManagedT', covariant=True, bound=ManagedWidget)


class Widget(Protocol[ManagedT]):
    def render(
            self, data: dict, context: dict, manager: DialogManager,
    ) -> List[RenderedItem]:
        raise NotImplementedError

    def register(self, router: Router) -> None:
        raise NotImplementedError

    def managed(self, manager: DialogManager) -> ManagedT:
        raise NotImplementedError

    def find(self, widget_id: str) -> Optional["Widget"]:
        raise NotImplementedError
