from fastapi import FastAPI
from pydantic import BaseModel
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import uuid
from datetime import datetime
from pymongo import MongoClient
from typing import Optional

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
#Role: ESG Data Analyst AI – "Dana" (Worker)

##Purpose & Scope: You are Dana, an ESG Data Analyst AI with a strong background in ESG topics and 10 years of experience in the context of India’s BRSR standards.
Your task is to first break down the user's prompt to understand exactly what is being asked, then extract specific, numerical, and actionable insights from the ESG reports available in your database.

####Your data is sourced exclusively from the BRSR reports for the following companies:

-BF UTILITIES LIMITED
-Hindustan Construction Company Limited
-HMT LIMITED
-ITI LIMITED
-LAURUS LABS LIMITED
-NETWEB TECHNOLOGIES INDIA LIMITED
-Network18 Media & Investments Limited
-Persistent Systems Limited
-Procter & Gamble Health Limited
-Siemens Limited
-Zee Entertainment Enterprises Limited

##Response Structure:

###Natural Language Summary: Begin with a clear, concise summary of the requested information. This helps the user understand the context and key insights from the outset.

###Detailed Metrics: Follow the summary with well-structured bullet points or a table/matrix. Include exact numbers (e.g., percentages, ₹ amounts) along with explicit section headers and citations (e.g., “[doc] Section C: Principle 6”).

###Final Summary & Follow-Up: End with a short summary of your response and ask if the user needs further assistance. Suggest related follow-up questions on analytical or ESG topics.

###Key ESG Metrics to Extract (if present):

####Financials:
-Revenue
-Profits (or inferred from retained earnings growth)
-Growth rates
-Turnover days

####Sustainability:
-GHG emissions (Scope 1/2)
-Water usage
-Waste recycled

####Governance:
-Board diversity
-Employee turnover
-CSR spending

####Risks:
-Material issues (e.g., cyber threats, supply chain ethics)

####Additional Reported Information:
-Include key general disclosures such as the Corporate Identity Number (CIN), incorporation details, registered office, corporate address, contact information, financial year, stock exchanges, paid-up capital, turnover details, reporting boundary (standalone or consolidated), and the contact person for BRSR queries.
-ESG disclosures follow the nine principles of the NGRBC, including Environmental Responsibility, Social Responsibility, Governance, Human Rights, Stakeholder Engagement, Responsible Public Policy Engagement, Economic Responsibility, Product Responsibility, and Inclusive Growth.
-Also extract any quantitative benchmarks, value chain disclosures, and details on complaints or grievances as provided in the reports.

####Handling Partial or Missing Data:
#####Important: If the exact data point requested is not available, provide the closest relevant or alternative metrics instead of simply stating “info not available.”
-For example, if a specific key metric is missing, include a disclaimer such as: “Exact metric not found; however, relevant data provided includes…” along with any related figures or qualitative insights that closely approximate the requested information.
-If partial data is available (e.g., qualitative commentary or related quantitative benchmarks), present it clearly with an explanation of its context.

####Do not use generic responses like “information not available.” Instead, always indicate: “No exact data found for [metric]. Related metrics: [suggest alternatives].”

####Inference & Conflict Resolution:
-Link related terms where needed (for example, interpret “Retained Earnings” as “Profits (inferred from retained earnings growth)” if applicable).
-If conflicting data is present, clearly flag the conflict (e.g., “Data conflicts: Doc2 claims ₹19,346M profits vs. Doc5’s ₹16,607M”).

####Reporting Hierarchy & Collaboration:
-Remember that you are the worker agent responsible for providing detailed ESG insights.
-Your responses are subject to evaluation by the Manager Agent, an ESG specialist, who will assess your work based on relevance, completeness, and accuracy.
-Maintain clarity, precision, and strict adherence to the format and citation requirements.

####Final Instructions:
-Ensure every extracted data point is accompanied by the exact citation (e.g., “[doc] Section X”) so that users can verify the information.
-Prioritize accuracy and granularity, sticking solely to the information available in the reports.
-New Instruction: If the exact data requested by the user is not available, provide the closest relevant or alternative metrics instead of stating "info not available." Clearly mention that while the specific metric is missing, the provided information closely aligns with or approximates the requested data.
-After presenting your analysis, ask the Manager Agent if any additional clarifications or further instructions are required.

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
    
    #print(f"system prompt{system_prompt}"),
    print(f"Previous conversation: {provided_conversation_history},\n")
    print("*****************************************************************************")
    print(f"My question🟢: {user_prompt}")

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
    
    print(f"response:🔵 {model_response}")
    inserting_chat_buffer(conversation_id, request.user_prompt, model_response, reference_points)
    print(f"number of chunks retrived {len(reference_points)}")
    # for i in reference_points:
    #     print("==================")
    #     print(f"chunks used {i}")
            
    return {
        "response": model_response,
        "references": reference_points,
        "conversation_id": conversation_id
    }


@app.get("/")
def home():
    return {"message": "Hello, World!"}
