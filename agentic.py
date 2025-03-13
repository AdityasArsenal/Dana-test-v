import json
from worker import worker
import os
import uuid
from consertations_handling import agents_conv_history, inserting_agent_chat_buffer, monolog, get_best_worker_response

director_system_prompt = """
always say this director speasking before you answer
you have all the data you need to give the response in the Previous conversation between you and worker agent.
"""

manager_system_prompt = """
#Role - Role: ESG Specialist with 10 Years of Experience - (Manager Agent)

##Keep in Mind:
-split the give user query into sub-questions, so that the worker agent under you can answer each question.One at a time.
-The worker agent has BRSR and Sustainability Report in the vector searchable Database.
-Below is the contents of those reports, I need you to generate sub-questions thinking that the worker agent will have answers to the following topics.

##companies in the Data-Base
1.Hindustan Petroleum Corporation Limited(HPCL)
2.Indian Oil Corporation Limited(IOCL)

##BRSR report containts:
### 1 Details of the Listed Entity
-Corporate identity (CIN, name, year of incorporation)
-Registered and corporate addresses, contact details, financial year, stock exchange listings, and paid‐up capital.

### 2 Products/Services
-Description of the main business activities and details of products/services sold (e.g., petroleum products, petrochemicals, and other energy-related segments).
-Breakdown of turnover contribution by key product/service categories.

### 3 Operations
-Details on operational locations (number of plants and offices, both national and international)
-Markets served including export contribution and a brief on customer segmentation (retail and bulk customers).

### 4 Employees
-Employee and worker statistics (permanent and non-permanent)
-Diversity and grievance redressal mechanisms for staff.

### 5 Holding, Subsidiary and Associate Companies (including Joint Ventures)
-Lists of associated companies along with the percentage share held and details on whether they participate in IOCL’s business responsibility initiatives.

### 6 CSR Details
-Information on the applicability of CSR (per Companies Act 2013)
-Turnover and net worth figures relevant to CSR considerations.

### 7 Transparency and Disclosures Compliances
-Grievance redressal mechanisms for various stakeholder groups (communities, investors, employees, customers, and value chain partners)
-Data on the number of complaints filed and resolved, along with web links to grievance policies.

### Additional Disclosures on Governance and Leadership
-A director’s statement highlighting ESG challenges, targets, and sustainability initiatives (including decarbonisation efforts, transition to green energy, and community engagement).

### General Disclosures
-Provides the company’s core details (incorporation, addresses, financial year, stock exchange listings, paid‐up capital, etc.)
-Outlines details on products/services, business activities, and operational information (such as plant locations and market reach).
-Contains employee and operational statistics similar to IOCL’s disclosures.

### Management and Process Disclosures
-Describes the policies and procedures adopted to implement the company’s sustainability framework
-Includes details of codes of conduct, whistleblower and grievance redressal policies, and stakeholder engagement mechanisms
-Outlines the internal review processes and the assurance methodology (with an independent assurance statement provided by Bureau Veritas).

### Principle Wise Performance Disclosure
-The section details performance indicators, targets, and results for each principle, emphasizing how the company manages its sustainability impacts.

### Independent Assurance Statement
-Provides details on the assurance engagement (scope, methodology, and limitations) conducted by an external auditor (Bureau Veritas) to verify the sustainability disclosures.

##Sustainability Report consist the following data :
-Environmental Leadership
-Strengthening Our Value Chain
-Our Approach to Sustainability
-Creating Shared Value for Our People
-Empowered Leadership and Transparent Governance
-Performance Summary 2023-24
-Driving Progress Through Renewable Energy
-Translating Green Ambitions into Reality
-Revolutionizing the Green Fuels Landscape
-Letter from the Chairman
-Strengthening India's Energy Independence
-Embracing Energy Transition
-Fueling Sustainability with Innovation and Technology
-Championing Environmental Sustainability
-Women Empowerment
-Empowering the Society
-Building a Greener Tomorrow with Sustainable Practices
-Supply Chain
-Awards and Recognitions
-Governance
-Policies, Principles, and Practices
-Board of Directors
-Internal Control Systems and Mechanisms
-Risk and Opportunities
-Empowering Digital Transformation
-Memberships, Affiliations, Collaboration, and Advocacy
-Shaping the Future Responsibly
-Future Readiness
-Stakeholder Engagement
-Matters Critical to Value Creation
-Sustainability at HPCL
-Strategic Environment Management for a Sustainable Future
-Energy
-GHG Emissions & Air Quality
-Biodiversity
-Research & Development
-Water Management
-Waste Management
-Sustainability at HPCL’s Residential Complex
-Manpower and Work Environment
-People Management
-Performance Management, Career Growth, and Progression
-Nurturing Talent
-Employee Engagement
-Capacity Building through Training and Development
-Industrial Harmony
-Diversity and Equal Opportunity
-Health and Safety
-Safety Management
-Safety in Transportation
-Advancing Health and Well-being
-Safety and Security of Critical Assets
-Building Lasting Relationships
-Customer Satisfaction
-Quality Management Systems
-Customer-centric Initiatives
-Engaging with the Local Communities
-Fostering Shared Prosperity
-Lives Touched Through CSR Projects
-Economic Performance
-Focusing on Sustainable Returns
-Alignment of Business Practices
-Helping Achieve UN Sustainable Development Goals
-India’s Nationally Determined Contributions (NDCs)
-UNGC Principles
-Task Force on Climate-related Financial Disclosures
-Independent Assurance Statement
-GRI Content Index
-List of Abbreviations

##Response Format in json
Return your evaluation strictly in JSON format with the following keys:
"list_of_sub_questions": A python list of sub-questions.

"""

manager_system_prompt_O = """
#Role - Role: ESG Specialist with 10 Years of Experience - (Manager Agent)

##Keep in Mind:
-split the give user query into sub-questions, so that the worker agent under you can answer each question.One at a time.
-The worker agent has BRSR and Sustainability Report in the vector searchable Database.

##Response Format in json
Return your evaluation strictly in JSON format with the following keys:
"list_of_sub_questions": A python list of sub-questions.
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
    print("MMMMMMM")
    print(f"⚪{azure_search_index}")
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
    print(f"number of sub-questions {len(list_of_sub_questions)}")
    context_chunks = []
    i = 0

    for sub_question in list_of_sub_questions:
        i += 1
        worker_response, context_chunk =  worker(client, deployment, sub_question, agents_conversation_history, azure_search_endpoint, azure_search_index, azure_search_api_key)
        inserting_agent_chat_buffer(agents_conversation_id, collection, sub_question, worker_response, context_chunks)# chuncks used by worker agent

        context_chunks.append(context_chunk)
        print(f"{i}th {sub_question}")

        # if i == max_iterations:
        #     print("THE ITERATION ENDED BECAUSE : Max iterations reached")
        #     break
    no_iterations = i
    direcotr_response = director(
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
    return direcotr_response, no_iterations, context_chunks

def director(
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
    print("DDDD")
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

    direcotr_response = completion.choices[0].message.content
    monolog(agents_conversation_history)
    return direcotr_response


