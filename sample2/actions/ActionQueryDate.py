from typing import Any, Text, Dict, List
from datetime import datetime, timedelta
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
import logging


def text_date_to_int(text_date):
    if text_date == "今天":
        return 0
    if text_date == "明天":
        return 1
    if text_date == "昨天":
        return -1

    # in other case
    return None


class ActionQueryDate(Action):
    def name(self) -> Text:
        return "action_query_date"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Query date action triggered.")
        text_date = tracker.get_slot("date") or "今天"

        int_date = text_date_to_int(text_date)
        if int_date is not None:
            delta = timedelta(days=int_date)
            current_date = datetime.now()

            target_date = current_date + delta

            dispatcher.utter_message(text=target_date.strftime("%Y-%m-%d"))
        else:
            dispatcher.utter_message(text="系统暂不支持'{}'的日期查询".format(text_date))

        return []
