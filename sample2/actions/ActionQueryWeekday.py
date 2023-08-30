import logging
from typing import Any, Text, Dict, List
from datetime import datetime, timedelta
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher

weekday_mapping = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期天"]


def text_date_to_int(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "昨天":
        return -1

    # in other case
    return None


def weekday_to_text(weekday):
    return weekday_mapping[weekday]


class ActionQueryWeekday(Action):
    def name(self) -> Text:
        return "action_query_weekday"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Query weekday action triggered.")
        text_date = tracker.get_slot("date") or "今天"

        int_date = text_date_to_int(text_date)
        if int_date is not None:
            delta = timedelta(days=int_date)
            current_date = datetime.now()

            target_date = current_date + delta

            dispatcher.utter_message(text=weekday_to_text(target_date.weekday()))
        else:
            dispatcher.utter_message(text="系统暂不支持'{}'的星期查询".format(text_date))

        return []
