import json
from worker import worker
import os
import uuid
from consertations_handling import agents_conv_history, inserting_agent_chat_buffer, monolog, get_best_worker_response

director_system_prompt = """
you have all the data you need to give the response in the Previous conversation between you and worker agent.
say this director speasking before you answer
"""
manager_system_prompt = """
say this manager speasking before you answer
split the give question into parts.

##Response Format in json
Return your evaluation strictly in JSON format with the following keys:
"list_of_sub_questions": A python list of questions.

if you have all the required data 

"""
# Azure AI Search configuration
azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")
azure_search_api_key = os.getenv("AZURE_SEARCH_API_KEY")

def manager(
    client,
    deployment,
    user_prompt,
    provided_conversation_history,
    max_iterations,
    collection,
    chat_history_retrieval_limit,
    no_iterations,
    context_chunks,
    agents_conversation_id,
):   
    
    if agents_conversation_id is None:
        agents_conversation_id = str(uuid.uuid4())
        agents_conversation_history = agents_conv_history(agents_conversation_id, collection, chat_history_retrieval_limit)
        
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": manager_system_prompt},
                {"role": "user", "content": f"Previous conversation between user and you: {provided_conversation_history},\nMy question: {user_prompt}"},
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        manager_json_output = completion.choices[0].message.content

        if "```" in manager_json_output:
            manager_json_output = manager_json_output.replace("```json","")
            manager_json_output = manager_json_output.replace("```","")

        agent_response = json.loads(manager_json_output) # Parse the JSON response ecplicitly asked
        list_of_sub_questions =agent_response["list_of_sub_questions"]
        print("============================")
        print(list_of_sub_questions)
        print("============================")

        context_chunks = []
        i = 0
        for sub_question in list_of_sub_questions:
            i += 1

            worker_response, context_chunk =  worker(client, deployment, sub_question, agents_conversation_history, azure_search_endpoint, azure_search_index, azure_search_api_key)
            inserting_agent_chat_buffer(agents_conversation_id, collection, sub_question, worker_response, context_chunks)# chuncks used by worker agent

            context_chunks.append(context_chunk)
            print(f"{i}th iteration")

            if i == max_iterations:
                print("THE ITERATION ENDED BECAUSE : Max iterations reached")
                break
        no_iterations = i
        manager(
            client,
            deployment,
            user_prompt,
            provided_conversation_history, 
            max_iterations,
            collection,
            chat_history_retrieval_limit,
            no_iterations,
            context_chunks,
            agents_conversation_id,
        )
        
        # elif ask_user == "yes":
        #     final_response = agent_response["query_for_user"]
        #     return final_response, 0 , context_chunks
    else:
        agents_conversation_history = agents_conv_history(agents_conversation_id, collection, chat_history_retrieval_limit)
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": director_system_prompt},
                {"role": "user", "content": f"Previous conversation between user and you: {provided_conversation_history},\nMy question: {user_prompt}"},
                {"role": "assistant", "content": f"Previous conversation between you and worker agent: {agents_conversation_history}"}
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        manager_json_output = completion.choices[0].message.content

        if "```" in manager_json_output:
            manager_json_output = manager_json_output.replace("```json","")
            manager_json_output = manager_json_output.replace("```","")
        monolog(agents_conversation_history)
        print(f"🔵response:{manager_json_output}")
        return manager_json_output, no_iterations, context_chunks




from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uuid
from pymongo import MongoClient
from typing import Optional
from openai import AzureOpenAI
import os
import uvicorn

from consertations_handling import conv_history, inserting_chat_buffer

load_dotenv(override=False)
app = FastAPI()

# Extend the ChatRequest to optionally include a conversation_id
class ChatRequest(BaseModel):
    user_prompt: str
    conversation_id: Optional[str] = None

connection_string = "mongodb://chat-history-with-cosmos:aWQkNybTHAZ4ZHgYXGNb4E2VDQ2BGP8k0WYyGPuziM4D5TayG2Pf5fnxFSD8Y3nI6wmXJvph3In1ACDbKj2jRQ==@chat-history-with-cosmos.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@chat-history-with-cosmos@"
mongo_client = MongoClient(connection_string)
db = mongo_client["ChatHistoryDatabase"]
collection = db["chat-history-with-cosmos"]
chat_history_retrieval_limit = 10

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYED_NAME")
api_key = os.getenv("AZURE_OPENAI_KEY")

client =  AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview",
)

def agentic_flow(user_prompt,conversation_id):
    max_iterations = 3
    
    provided_conversation_history = conv_history(conversation_id, collection, chat_history_retrieval_limit)
    agents_conversation_id = None
    no_iterations = 0
    context_chunks = ""

    print(f"🟢  USER : {user_prompt} and agentic conv ID :{agents_conversation_id}")
    final_response, iteratations, context_chunks =  manager(client, deployment, user_prompt, provided_conversation_history, max_iterations, collection, chat_history_retrieval_limit, no_iterations, context_chunks, agents_conversation_id)

    #print(f"🟢{iteratations} times the worker was asked to improve the response")
    #print(f"🔵chunks used:  {context_chunks}")
    print(f"🔴  MODEL : {final_response}")

    return final_response, context_chunks

conversation_id = str(uuid.uuid4())
agentic_flow("What are the major differences between the materiality assessment of ITI Limited and HMT LIMITED", conversation_id)