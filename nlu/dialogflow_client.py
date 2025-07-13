import os
from google.cloud import dialogflow_v2 as dialogflow
from utils.config import GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, LANGUAGE_CODE

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS
dialogflow_client = dialogflow.SessionsClient()

def detect_intent_texts(text):
    session_id = "drive-thru-session"
    session = dialogflow_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = dialogflow_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response.query_result.fulfillment_text, response.query_result.intent.display_name, dict(response.query_result.parameters)
    except Exception as e:
        print(f"Dialogflow Error: {e}")
        return "Sorry, I encountered an error.", None, None 