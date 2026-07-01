import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv()

endpoint = os.getenv("LANGUAGE_ENDPOINT")
key = os.getenv("LANGUAGE_KEY")

client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)


def summarize_text(text: str):
    """
    Generates an abstractive summary.
    """

    poller = client.begin_abstract_summary([text])

    result = poller.result()

    for document in result:

        if document.is_error:
            return None

        summaries = [summary.text for summary in document.summaries]

        return " ".join(summaries)

    return None


def analyze_text(text: str):

    document = [text]

    # Language
    language = client.detect_language(document)[0]

    # Sentiment
    sentiment = client.analyze_sentiment(document)[0]

    # Key Phrases
    key_phrases = client.extract_key_phrases(document)[0]

    # Named Entities
    entities = client.recognize_entities(document)[0]

    # PII
    pii = client.recognize_pii_entities(document)[0]

    # Summary
    summary = summarize_text(text)

    return {

        "language": {
            "name": language.primary_language.name,
            "iso_code": language.primary_language.iso6391_name,
            "confidence": round(
                language.primary_language.confidence_score,
                3
            )
        },

        "sentiment": {
            "label": sentiment.sentiment,
            "confidence": {
                "positive": round(
                    sentiment.confidence_scores.positive,
                    3
                ),
                "neutral": round(
                    sentiment.confidence_scores.neutral,
                    3
                ),
                "negative": round(
                    sentiment.confidence_scores.negative,
                    3
                )
            }
        },

        "key_phrases": key_phrases.key_phrases,

        "entities": [
            {
                "text": entity.text,
                "category": entity.category,
                "subcategory": entity.subcategory,
                "confidence": round(entity.confidence_score, 3)
            }
            for entity in entities.entities
        ],

        "pii": [
            {
                "text": entity.text,
                "category": entity.category,
                "confidence": round(entity.confidence_score, 3)
            }
            for entity in pii.entities
        ],

        "redacted_text": pii.redacted_text,

        "summary": summary
    }