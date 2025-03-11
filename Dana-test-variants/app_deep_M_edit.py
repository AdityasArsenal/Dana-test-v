from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
import uuid
from datetime import datetime
from pymongo import MongoClient
from typing import Optional
import uvicorn

# Load environment variables
load_dotenv(override=False)

app = FastAPI()

# Azure OpenAI configuration
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYED_NAME")
api_key = os.getenv("AZURE_OPENAI_KEY")

# Azure AI Search configuration
azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")
azure_search_api_key = os.getenv("AZURE_SEARCH_API_KEY")

system_prompt = """
**Role**: Senior ESG Specialist (BRSR & GRE Standards)  
**Data Source**: Internal ESG Reports Database  
**Response Protocol**: Tiered Disclosure System

## Core Response Structure
```text
1. NATURAL LANGUAGE SUMMARY
   ➤ 2-3 paragraph plain English explanation
   ➤ Contextualizes numbers with business impact
   ➤ Example: "Energy consumption decreased 15% YoY through..."

2. STRUCTURED BULLET POINTS
   ➤ Prioritized key metrics with visual hierarchy:
   • 🟢 22% Renewable Energy Adoption (2023)
     - Source: Doc4-E7 
     - Trend: ↑9% from 2021
   • 🟡 41.9% Worker Turnover (Doc4-S3)
     - Flag: Exceeds industry avg (25-30%)

3. SYNTHESIS SUMMARY
   ➤ Cross-domain connections:
   "The 15% energy reduction aligns with..." 
   ➤ Materiality assessment:
   "This impacts 3 SDGs: #7, #9, #12"

4. HELP PROMPT (MANDATORY)
   ➤ "Would you like to: 
      a) Dive deeper into any metric?
      b) Compare with industry benchmarks?
      c) Request compliance analysis?"

Missing Data Protocol :

➤ When requested data absent:
1. Surface 3 closest available metrics
   │ Requested       │ Offered Alternatives       │
   │-----------------|---------------------------│
   │ CEO compensation│ Executive bonus structure  │
   │                 │ Pay ratio disclosure      │
   │                 │ Board remuneration policy │

2. Suggest validated follow-ups:
   • "Available related data: 
     - Supplier ESG screening process (Doc3-G8)
     - Vendor diversity ratios (Doc5-S2)
     - Scope 3 emission boundaries (Doc7-E4)"
   
3. Transparency statement:
   "While exact figures for [X] aren't available, 
   our reports contain these related disclosures..."

**Example**
User Query:
"Show our gender pay gap statistics"

AI Response:
**Natural Language Summary**  
While specific gender pay gap metrics aren't tracked in our current reporting framework, we maintain detailed workforce diversity records. Female representation in leadership roles reached 34% in FY2023, up from 28% in FY2021. All business units now have mandatory unconscious bias training with 89% completion rates.

**Available Relevant Data**  
• Leadership Diversity (Confirmed):  
  │ 2021  │ 2022  │ 2023  │  
  │-------|-------|-------│  
  │ 28%   │ 31%   │ 34%   │  
  Source: Doc2-S5 (Audited)  

• Training Completion:  
  - DEI Programs: 89% (2023)  
  - Technical Upskilling: 76%  
  Source: Doc4-AppendixC  

• Retention Rates:  
  │ Female │ Male  │  
  │--------|-------│  
  │ 82%    │ 78%   │  
  Source: Doc7-HR3  

**Suggested Alternative Queries**  
1. Pay band distribution by gender  
2. Promotion rates vs gender correlation  
3. Childcare support program participation  

Would you like me to generate a comparative analysis with industry benchmarks from our MSCI ESG reports?

Compliance Check
➤ All responses must:
1. Start/end with natural language summaries
2. Contain ≤5 prioritized bullet points
3. Show explicit source mapping
4. Include help prompt even when complete
5. Never extrapolate beyond report data

"""


# Cosmos DB configuration using MongoDB API
connection_string = "mongodb://chat-history-with-cosmos:aWQkNybTHAZ4ZHgYXGNb4E2VDQ2BGP8k0WYyGPuziM4D5TayG2Pf5fnxFSD8Y3nI6wmXJvph3In1ACDbKj2jRQ==@chat-history-with-cosmos.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@chat-history-with-cosmos@"
mongo_client = MongoClient(connection_string)
db = mongo_client["ChatHistoryDatabase"]
collection = db["chat-history-with-cosmos"]
chat_history_retrieval_limit = 10

# OpenAI Client Initialization
ai_client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview",
)

# Extend the ChatRequest to optionally include a conversation_id
class ChatRequest(BaseModel):
    user_prompt: str
    conversation_id: Optional[str] = None

def play_ground(client, deployment, user_prompt, azure_search_endpoint, azure_search_index, azure_search_api_key, conversation_id):   
    # Retrieve the chat history documents using the conversation id
    chat_history_retrieved = list(collection.find({"id": conversation_id}))
    
    recent_chat_history = chat_history_retrieved[-chat_history_retrieval_limit:] if chat_history_retrieved else []
    provided_conversation_history = []
    
    for doc in recent_chat_history:
        user_message = doc.get("user_prompt", "")
        ai_message = doc.get("model_response", "")
        provided_conversation_history.append({"role": "user", "content": user_message})
        provided_conversation_history.append({"role": "assistant", "content": ai_message})
    
    print(f"system prompt{system_prompt}"),
    print(f"Previous conversation: {provided_conversation_history},\nMy question: {user_prompt}")

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Previous conversation: {provided_conversation_history},\nMy question: {user_prompt}"}
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": azure_search_endpoint,
                        "index_name": azure_search_index,
                        "authentication": {
                            "type": "api_key",
                            "key": azure_search_api_key
                        }
                    }
                }
            ]
        }
    )
    
    # Extract the response and context citations
    response_message = completion.choices[0].message.content
    context_chunks = [citation['content'] for citation in completion.choices[0].message.context.get('citations', [])]
    
    return response_message, context_chunks

def inserting_chat_buffer(conversation_id, user_prompt, model_response, references):
    # Insert a chat document into the collection
    chat_history_doc = {
        "id": conversation_id,
        "user_prompt": user_prompt,
        "model_response": model_response,
        "timestamp": datetime.utcnow().isoformat(),
        "references": references
    }
    collection.insert_one(chat_history_doc)

# API Endpoint to receive user input and return AI response
@app.post("/chat")
def chat(request: ChatRequest):
    # Use provided conversation_id or generate a new one if missing
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    model_response, reference_points = play_ground(
        ai_client,
        deployment,
        request.user_prompt,
        azure_search_endpoint,
        azure_search_index,
        azure_search_api_key,
        conversation_id
    )
    
    inserting_chat_buffer(conversation_id, request.user_prompt, model_response, reference_points)
    
    return {
        "response": model_response,
        "references": reference_points,
        "conversation_id": conversation_id
    }

@app.get("/")
def home():
    return {"message": "Hello, World!"}
