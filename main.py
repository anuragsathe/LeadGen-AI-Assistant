from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel, Field
from typing import List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from tools import save_tool



class LeadResponse(BaseModel):
    company: str = Field(description="Company name")
    contact_info: str = Field(description="Phone, address, or contact info")
    email: str = Field(description="Email address if available")
    summary: str = Field(description="Why they may need IT services")
    outreach_message: str = Field(description="Short outreach message")
    tools_used: List[str] = Field(description="Tools used (can be empty)")

class LeadResponseList(BaseModel):
    leads: List[LeadResponse]



llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

parser = PydanticOutputParser(pydantic_object=LeadResponseList)



prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a sales research assistant.

Task:
Find exactly 5 small businesses in Vancouver, Canada that may need IT services.

STRICT RULES:
- Return ONLY valid JSON
- No explanations, no extra text
- No markdown
- Must match schema exactly
- Always return 5 leads

{format_instructions}
"""
    ),
    ("human", "{query}")
]).partial(format_instructions=parser.get_format_instructions())



chain = prompt | llm



query = "Find 5 small businesses in Vancouver that may need IT services."

response = chain.invoke({"query": query})

print("\n RAW RESPONSE:\n", response)



if isinstance(response, str):
    output_text = response
elif hasattr(response, "content"):
    output_text = response.content
else:
    output_text = str(response)

print("\n EXTRACTED TEXT:\n", output_text)



try:
    structured_response = parser.parse(output_text)

    json_data = structured_response.model_dump_json(indent=2)

    print("\n STRUCTURED OUTPUT:\n")
    print(json_data)


    save_result = save_tool.run(json_data)
    print("\n SAVE STATUS:", save_result)

except Exception as e:
    print("\n Parsing Failed:", e)
    print("\n RAW OUTPUT:\n", output_text)