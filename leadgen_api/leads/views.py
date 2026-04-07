from rest_framework.decorators import api_view
from rest_framework.response import Response
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from .utils import search_and_scrape

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


@api_view(['POST'])
def generate_leads(request):
    industry = request.data.get("industry")
    location = request.data.get("location")

    if not industry or not location:
        return Response({"error": "industry and location required"}, status=400)

    queries = [
        f"{industry} {location} small business",
        f"{industry} company {location}",
        f"{industry} services {location}",
    ]

    leads = []

    for q in queries:
        data = search_and_scrape(q)

        if data == "No results":
            leads.append("No leads found for this query")
            continue

        prompt = f"""
        Extract:
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
            leads.append(response.content)
        except Exception as e:
            error_str = str(e)
            if "RESOURCE_EXHAUSTED" in error_str:
                leads.append("API quota exceeded, please try again later")
            else:
                leads.append(f"Error processing query: {error_str}")

    return Response({"leads": leads})

    return Response({
        "status": "success",
        "leads": leads
    })