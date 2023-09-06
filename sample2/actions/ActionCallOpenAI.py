from typing import Any, Text, Dict, List
from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
import openai


class ActionCallOpenAi(Action):
    def name(self) -> Text:
        return "action_openai_call"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        openai.api_key = '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'
        prompt = tracker.latest_message.get('text')
        # Make API calls to OpenAI
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        generated_text = response['choices'][0]['text'].strip()
        # Use the generated text in the response
        dispatcher.utter_message(text=generated_text)

        return []
