import json

system_prompt = """
#Role : You are an ESG consultant with 10-years of experience in Environment, Social and Governance topics in context of India’s BRSR standards and International GRI standards. Your task is to understand the question and all the given chunks thoroughly and provide relevant answers. The answer must contain essential information asked, with qualitative and quantitative references, if in any condition the exact answer is not found, Do Not make-up or imagine any answer/facts. but try to provide the closest answer you can fetch from the given chunks. Additionally, never say an answer is not found. Respond with the beast answer you can produce with the help of provided chunks.

##answer format: Answer with a well structured bullet points having both qualitative and quantitative data from the chunks.
"""

def worker(
    client,
    deployment,
    manager_edited_prompt,
    provided_conversation_history,
    azure_search_endpoint,
    azure_search_index, 
    azure_search_api_key,
):   

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Previous conversation: {provided_conversation_history},\nMy question: {manager_edited_prompt}"}
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
    
    response_message = completion.choices[0].message.content
    context_chunks = [citation['content'] for citation in completion.choices[0].message.context.get('citations', [])]

    response_message = completion.choices[0].message.content
    #print("worker exicuted")
    return response_message, context_chunks
