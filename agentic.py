import json
from worker import worker
import os
import uuid
from consertations_handling import agents_conv_history, inserting_agent_chat_buffer, monolog, get_best_worker_response

manager_clasic_system_prompt = """
Role: ESG Specialist with 10 Years of Experience – (Manager)

##Purpose & Scope:
You are the Manager Agent responsible for reviewing and evaluating the AI-generated (worker) response from Dana.
Your evaluation must focus on the following criteria:
-Relevance: How well does the response address the user’s query?
-Completeness: Does the response cover key ESG factors as per the BRSR framework?
-Accuracy: Is the extracted information correct and properly cited from the reports?

##Response Format:
Return your evaluation strictly in JSON format with the following keys:

"satisfied": Use "yes" if the overall score is 7 or above, otherwise "no".
"score": A numeric score from 1 to 10 reflecting your overall evaluation.
"reason": A brief explanation detailing why the response did or did not meet the criteria.
"edited_prompt": A revised version of the worker prompt with suggestions for improvement.
"query_for_user": A string containing the exact query you want to ask the user for further clarification.
"ask_user?": Use "yes" if you want to ask the user for further clarification based on the worker’s response, or "no" if no further user clarification is needed.

##Additional Guidelines:
-Ensure your response is entirely in valid JSON with the specified keys.
-Clearly indicate that you are interacting with the worker (Dana) who has generated the report data, and provide guidance for any improvements necessary.
-Keep in mind that your evaluation helps decide which responses are shown to the user programmatically based on the "satisfied" and "score" keys.

###Extra Clarification Requirement: If the worker’s response indicates that additional information is needed—which can only be provided by the user—mark the response as "satisfied", set "ask_user?" to "yes", and use the "query_for_user" key to state exactly what further information is required from the user.

###Manager-to-User Interaction: When necessary, do not assume or fabricate additional instructions for the worker agent. Instead, use the "query_for_user" key to state the query for the user, and set "ask_user?" to "yes" if you want the user to provide further clarification. Otherwise, set "ask_user?" to "no".

##Important for chat flow : Fill the "ask_user?" with no if you are satisfied with the workers response.

####Your worker agent has the data exclusively from the BRSR reports for the following companies:
- BF UTILITIES LIMITED
- Hindustan Construction Company Limited
- HMT LIMITED
- ITI LIMITED
- LAURUS LABS LIMITED
- NETWEB TECHNOLOGIES INDIA LIMITED
- Network18 Media & Investments Limited
- Persistent Systems Limited
- Procter & Gamble Health Limited
- Siemens Limited
- Zee Entertainment Enterprises Limited

"""

manager_system_prompt = """
split the give question into parts and add them as a list in the 
##Response Format:
Return your evaluation strictly in JSON format with the following keys:

"final_response": if you have conversation between you and worker agent, that means you have already contacted the worker agent and you have all sub-questions and the answers to create response for the user.
"talked_to_worker?": use "yes" if you have the convertation history, else if you don't have any convertation with the worker agent say "no"
"alternate_response": A response created with available data.

"use_worker?":Use "yes" if you need worker's help, else if you already have the answer in Previous conversations between you and worker agent say "no"
"number_of_sub_questions": The total number of the questions.
"list_of_sub_questions": A python list of questions.


"query_for_user": A string containing the exact query you want to ask the user for further clarification.
"ask_user?": Use "yes" if you want to ask the user for further clarification based on the worker’s response, or "no" if no further user clarification is needed.
"""
# Azure AI Search configuration
azure_search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
azure_search_index = os.getenv("AZURE_AI_SEARCH_INDEX")
azure_search_api_key = os.getenv("AZURE_SEARCH_API_KEY")


def manager(client, deployment, user_prompt, provided_conversation_history, max_iterations, collection, chat_history_retrieval_limit, agents_conversation_id,internally):   
    
    if agents_conversation_id is None:
        agents_conversation_id = str(uuid.uuid4())
        agents_conversation_history = agents_conv_history(agents_conversation_id, collection, chat_history_retrieval_limit)
        
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": manager_system_prompt},
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
        #print(f"manager op : {manager_json_output}")

        if "```" in manager_json_output:
            manager_json_output = manager_json_output.replace("```json","")
            manager_json_output = manager_json_output.replace("```","")

        agent_response = json.loads(manager_json_output) # Parse the JSON response ecplicitly asked
        ask_user = agent_response["ask_user?"]

        use_worker = agent_response["use_worker?"]
        number_of_sub_questions = agent_response["number_of_sub_questions"]
        list_of_sub_questions =agent_response["list_of_sub_questions"]
        final_response = agent_response["final_response"]

        print(f"wanna contact user?{ask_user}")

        if use_worker == "yes":
            context_chunks = []
            for i in range(number_of_sub_questions):
                worker_response,context_chunk =  worker(client, deployment, list_of_sub_questions[i], agents_conversation_history, azure_search_endpoint, azure_search_index, azure_search_api_key)
                inserting_agent_chat_buffer(agents_conversation_id, collection, list_of_sub_questions[i], worker_response, context_chunks)# chuncks used by worker agent
                
                context_chunks.append(context_chunk)
                print(f"{i}th iteration")

                if i == max_iterations:
                    print("THE ITERATION ENDED BECAUSE : Max iterations reached")
                    break
            
            final_response =  manager(client, deployment, user_prompt, provided_conversation_history, max_iterations, collection, chat_history_retrieval_limit,agents_conversation_id, internally=True)
            return final_response , i, context_chunks

        elif ask_user == "yes":
            final_response = agent_response["query_for_user"]
            return final_response, 0 , context_chunks
    else:
        agents_conversation_history = agents_conv_history(agents_conversation_id, collection, chat_history_retrieval_limit)
        completion = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": manager_system_prompt},
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
        #print(f"manager op : {manager_json_output}")

        if "```" in manager_json_output:
            manager_json_output = manager_json_output.replace("```json","")
            manager_json_output = manager_json_output.replace("```","")

        agent_response = json.loads(manager_json_output) # Parse the JSON response ecplicitly asked
        #print(f"agent_decision =------------={agent_decision}")

        ask_user = agent_response["ask_user?"]

        use_worker = agent_response["use_worker?"]
        number_of_sub_questions = agent_response["number_of_sub_questions"]
        list_of_sub_questions =agent_response["list_of_sub_questions"]
        talked_to_worker = agent_response["talked_to_worker?"]

        print(f"wanna contact user?{ask_user}")

        if use_worker =="no":
            final_response = agent_response["final_response"]
            return final_response

        if talked_to_worker == "yes":
            alternate_response = agent_response["alternate_response"]
            return alternate_response
        
        elif talked_to_worker == "no":
            for i in range(number_of_sub_questions):
                worker_response,context_chunks =  worker(client, deployment, list_of_sub_questions[i], agents_conversation_history, azure_search_endpoint, azure_search_index, azure_search_api_key)
                inserting_agent_chat_buffer(agents_conversation_id, collection, list_of_sub_questions[i], worker_response, context_chunks)# chuncks used by worker agent
                
                print(f"{i}th iteration")

                if i == 5:
                    print("THE ITERATION ENDED BECAUSE : Max iterations reached")
                    break
            
            manager(client, deployment, user_prompt, provided_conversation_history, max_iterations, collection, chat_history_retrieval_limit,agents_conversation_id, internally=True)
            return 

        



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