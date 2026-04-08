import json
import os
from pathlib import Path

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, BaseParser
from rest_framework.response import Response
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from .utils import search_and_scrape
from .models import Lead

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)


class PlainJSONParser(BaseParser):
    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        raw_data = stream.read().decode("utf-8")
        try:
            return json.loads(raw_data)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON in text/plain request body") from exc

MODEL_CANDIDATES = [
    os.getenv("GOOGLE_MODEL"),
    os.getenv("GEMINI_MODEL"),
    "gemini-2.5-flash",
    "gemini-2.1",
    "gemini-1.5-pro",
    "gemini-1.0",
]
MODEL_CANDIDATES = [m for m in MODEL_CANDIDATES if m]


def get_llm():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing Google API key. Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment."
        )

    last_error = None
    for model_name in MODEL_CANDIDATES:
        try:
            return ChatGoogleGenerativeAI(model=model_name, google_api_key=api_key)
        except Exception as exc:
            last_error = exc
            if any(keyword in str(exc).upper() for keyword in ["UNAVAILABLE", "HIGH DEMAND", "RESOURCE_EXHAUSTED"]):
                continue
            raise

    raise RuntimeError(
        f"Unable to initialize a Google LLM. Last error: {last_error}"
    )


@api_view(['POST'])
@parser_classes([JSONParser, PlainJSONParser])
def generate_leads(request):
    industry = request.data.get("industry")
    location = request.data.get("location")

    if not industry or not location:
        return Response({"error": "industry and location required"}, status=400)

    try:
        llm = get_llm()
    except RuntimeError as e:
        return Response({"error": str(e)}, status=500)


    queries = [
        f"{industry} {location} small business",
        f"{industry} company {location}",
        f"{industry} services {location}",
    ]

    leads = []
    lead_objects = []

    for q in queries:
        data = search_and_scrape(q)

        if data == "No results":
            leads.append("No leads found for this query")
            continue

        prompt = f"""
        Extract and format as JSON:
        - Company Name
        - Contact Info
        - Email
        - Why they need IT services
        - Outreach message

        DATA:
        {data}
        """

        try:
            response = llm.invoke(prompt)
            response_content = response.content
            leads.append(response_content)
            
            # Save to database
            lead_obj = Lead.objects.create(
                company_name="Generated Lead",
                industry=industry,
                location=location,
                raw_response=response_content,
            )
            lead_objects.append(lead_obj.id)
            
        except Exception as e:
            error_str = str(e)
            if "RESOURCE_EXHAUSTED" in error_str:
                leads.append("API quota exceeded, please try again later")
            else:
                leads.append(f"Error processing query: {error_str}")

    return Response({
        "leads": leads,
        "saved_lead_ids": lead_objects,
        "industry": industry,
        "location": location,
        "message": f"Generated and saved {len(lead_objects)} leads"
    })