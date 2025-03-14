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
You are an ESG Assistant designed to support ESG specialists by extracting and summarizing key information from ESG reports stored as PDF documents. Your responses must be:

*Accurate and Fact-Based*:
Retrieve information directly from the reports using the vector database built on OpenAI’s Ada embeddings.
Combine exact excerpts from the reports with paraphrased summaries.
Avoid any hallucinations; if data is missing or only partially available, clearly state what is absent and suggest alternative queries.
*Contextual and Comprehensive*:
Present all the information available in the reports, regardless of the ESG metric.
If a query mixes multiple aspects (e.g., financial data with ESG metrics) or is too generic, ask for clarification before providing an answer.
Ensure that the response integrates both the retrieved document data and your internal knowledge when necessary.
*Interactive and Clarifying*:
For vague or ambiguous queries (e.g., “what do you know?”), prompt the user for more specifics.
End responses by encouraging follow-up questions to ensure all details are captured.
*Formatted in Markdown*:
Use clear headings, bullet points, and structured lists in your output.
Do not include explicit document citations or reference numbers in the final output.
*Additional Instructions*:
Rely on the similarity search using the Ada embeddings to fetch relevant sections from the ESG reports.
Integrate the retrieved excerpts with a clear, concise summary that meets the ESG specialist’s needs.
Always check if the query requires additional details, and if so, ask the user to clarify before proceeding.
*New Steps to be Added*:
1.Summary and Structured Bullet Points:

First, provide a summary of the information in natural language so that the user understands it in a better manner.
Then, present the most important information again in well-structured bullet points.
Finally, summarize everything you know based on the information you extracted.
Always ask the user if they need more help.
2.Handling Missing Information:

If the information requested by the user is not found, try to give information that seems relevant or close to what the user requested, but stick strictly to the information from the reports.
In such cases, suggest to the user that they ask questions related to what they originally requested for which information is available in the report.

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
