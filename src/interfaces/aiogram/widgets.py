from enum import Enum

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Multiselect, Select
from aiogram_dialog.widgets.text import Format, Text


class SelectFromEnum(Select):
    def __init__(
        self, enum: Enum, widget_id: str, exclude_button_from_id: str | None = None
    ):
        text = Format("{item}")
        items = [e.value for e in enum]
        super().__init__(text, widget_id, str, items, self.__on_click)

        self.items_getter = self.__items_getter
        self.__items = items
        self.__id = widget_id
        self.__exclude_button_from_id = exclude_button_from_id

    def __items_getter(self, data: dict):
        exclude_data = data["dialog_data"].get(self.__exclude_button_from_id, None)
        return (item for item in self.__items if item != exclude_data)

    async def __on_click(
        self, call: CallbackQuery, select, manager: DialogManager, item: str
    ):
        manager.current_context().dialog_data[self.__id] = item
        await manager.dialog().next()


class MultiselectRelatedPayment(Multiselect):
    def __init__(
        self,
        checked_text: Text,
        unchecked_text: Text,
        items: dict,
        widget_id: str,
        related_select_id: str,
    ):
        super().__init__(checked_text, unchecked_text, widget_id, str, items)

        self.__related_select_id = related_select_id
        self.items_getter = self.__items_getter
        self.__items = items
        self.__id = widget_id

    def __items_getter(self, data: dict):
        related_data_selector = data["dialog_data"].get(self.__related_select_id)
        return self.__items[related_data_selector]