import azure.functions as func
import json, os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv('AZURE_ENDPOINT')
key = os.getenv('AZURE_API_KEY')

client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        text = req_body.get('text', '')

        analysis = client.analyze_sentiment([text])[0]

        result = {
            "sentiment": analysis.sentiment,
            "scores": {
                "positive": analysis.confidence_scores.positive,
                "neutral": analysis.confidence_scores.neutral,
                "negative": analysis.confidence_scores.negative,
            }
        }

        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
