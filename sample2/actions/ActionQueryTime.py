import logging

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
from datetime import datetime, timedelta


class ActionQueryTime(Action):
    def name(self) -> Text:
        return "action_query_time"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Query time action triggered.")
        current_time = datetime.now().strftime("%H:%M:%S")
        dispatcher.utter_message(text=current_time)

        return []
