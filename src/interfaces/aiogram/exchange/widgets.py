from typing import Callable

from aiogram_dialog.widgets.kbd import Multiselect, Select
from aiogram_dialog.widgets.text import Text


class RelatedMultiselect(Multiselect):
    def __init__(
            self, checked_text: Text, unchecked_text: Text, id: str,
            item_id_getter: Callable,
            related_widget_id: str, items: dict,
            min_selected: int = 0, max_selected: int = 0,
            on_click=None,
            on_state_changed=None,
            when=None
    ):
        super().__init__(checked_text, unchecked_text, id,
                         item_id_getter, items,
                         min_selected=min_selected,
                         max_selected=max_selected,
                         on_click=on_click,
                         on_state_changed=on_state_changed,
                         when=when)

        self.items_getter = self.__items_getter
        self.__related_widget_id = related_widget_id
        self.__items = items

    def __items_getter(self, data: dict):
        related_data_selector = data["dialog_data"].get(self.__related_widget_id)
        return self.__items[related_data_selector]



class SelectWithExclude(Select):
    def __init__(
            self, text: Text,
            id: str,
            item_id_getter,
            items: dict,
            exclude_selected_by_id: str | None = None,
            on_click=None,
            when=None
    ):
        super().__init__(text, id, item_id_getter,
                         list(items),
                         on_click=on_click,
                         when=when)

        self.items_getter = self.__items_getter
        self.__items = items
        self.__inverse_items = {v: k for k, v in items.items()}
        self.__exclude_selected_by_id = exclude_selected_by_id

    def __items_getter(self, data: dict):
        exclude_data = data["dialog_data"].get(self.__exclude_selected_by_id, None)
        return (self.__items[item] for item in self.__items if item != exclude_data)
