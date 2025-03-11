import json
from worker import worker
import os
import uuid
from consertations_handling import agents_conv_history, inserting_agent_chat_buffer, monolog, get_best_worker_response

manager_system_prompt = """
You are an ESG specialist reviewing an AI-generated response. Evaluate the response based on:
1. Relevance to the user's question.
2. Completeness in covering key ESG factors.
3. Accuracy based on the extracted BRSR report context.

For each evaluation, assign a score from 1 to 10 and determine if the overall response is satisfactory. 

Return your evaluation strictly in JSON format with the following keys:
- "satisfied": "yes" or "no" (set to "yes" if the overall score is 7 or above; otherwise "no").
- "score": The overall numeric score (from 1 to 10).
- "reason": A brief explanation detailing why the response did or did not meet the criteria.
- "edited_prompt": A revised version of the prompt with suggestions for the worker agent to generate an improved answer.

Your response must be valid JSON containing only these keys.
"""

# Azure AI Search configuration
azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")
azure_search_api_key = os.getenv("AZURE_SEARCH_API_KEY")

def manager(client, deployment, user_prompt, provided_conversation_history, max_iterations, collection, chat_history_retrieval_limit):   
    c = 0
    agents_conversation_id = str(uuid.uuid4())
    worker_response,context_chunks = worker(client, deployment, user_prompt, provided_conversation_history, azure_search_endpoint, azure_search_index, azure_search_api_key)

    while True:
        agents_conversation_history = agents_conv_history(agents_conversation_id, collection, chat_history_retrieval_limit)
        
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": manager_system_prompt},
                {"role": "user", "content": f"Previous conversation between user and you: {provided_conversation_history},\nMy question: {user_prompt}"},
                {"role": "assistant", "content": f"Previous conversation between you and worker agent: {agents_conversation_history},\nassistance response: {worker_response}"}
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )

        manager_json_output = completion.choices[0].message.content
        #print(f"manager op : {manager_json_output}")

        if "```" in manager_json_output:
            manager_json_output = manager_json_output.replace("```json","")
            manager_json_output = manager_json_output.replace("```","")

        agent_response = json.loads(manager_json_output) # Parse the JSON response ecplicitly asked
        agent_decision = agent_response["satisfied"]
        #print(f"agent_decision =------------={agent_decision}")
        agent_score = agent_response["score"]
        agent_reason = agent_response["reason"]
        agent_edited_prompt = agent_response["edited_prompt"]

        c+=1
        print(f"{c}th iteration")
        if c == max_iterations:
            print("THE ITERATION ENDED BECAUSE : Max iterations reached")
            monolog(agents_conversation_history)

            worker_response = get_best_worker_response(agents_conversation_history)
            return worker_response, c, context_chunks

        elif agent_decision == "yes":
            print("THE ITERATION ENDED BECAUSE : manager was satisfied")
            monolog(agents_conversation_history)
            return worker_response, c, context_chunks
        
        elif agent_decision == "no":
            worker_response,context_chunks = worker(client, deployment, agent_edited_prompt, provided_conversation_history, azure_search_endpoint, azure_search_index, azure_search_api_key)

            inserting_agent_chat_buffer(agents_conversation_id, collection, agent_edited_prompt, worker_response, context_chunks, agent_score) # chuncks which are used by worker agent but not final yet.

            #print(f"worker's {c}th attemt to please manager")

        

# from openai import AzureOpenAI
# from consertation_context import conv_history
# from pymongo import MongoClient

# user_prompt = "How robust is the company’s ESG governance framework, and how is board oversight structured to ensure accountability for ESG risks and opportunities?"

# connection_string = "mongodb://chat-history-with-cosmos:aWQkNybTHAZ4ZHgYXGNb4E2VDQ2BGP8k0WYyGPuziM4D5TayG2Pf5fnxFSD8Y3nI6wmXJvph3In1ACDbKj2jRQ==@chat-history-with-cosmos.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@chat-history-with-cosmos@"
# mongo_client = MongoClient(connection_string)
# db = mongo_client["ChatHistoryDatabase"]
# collection = db["chat-history-with-cosmos"]
# chat_history_retrieval_limit = 10

# conversation_id = "10deef48-464e-4987-9f1e-448383e3cbfb"

# endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
# deployment = os.getenv("AZURE_OPENAI_DEPLOYED_NAME")
# api_key = os.getenv("AZURE_OPENAI_KEY")

# client =  AzureOpenAI(
#     api_key=api_key,
#     azure_endpoint=endpoint,
#     api_version="2024-05-01-preview",
# )

# #provided_conversation_history = conv_history(conversation_id, collection, chat_history_retrieval_limit)
# provided_conversation_history = []
# manager(client, deployment, user_prompt, provided_conversation_history, max_iterations=2)