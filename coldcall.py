from langchain_google_genai import ChatGoogleGenerativeAI
import os
from condense_context import CONDENSE_CONTEXT
# from dotenv import load_dotenv
# load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.2
    
)

def chat_call(system_prompt, user_prompt):
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    return response.content
def normalize_output(output):
    if isinstance(output, list) and output and isinstance(output[0], dict):
        return output[0].get("text", "")
    return str(output)

def inputtooutput(url: str):
    first = get_company_info(url)
    clean_first = normalize_output(first)
    condense = condenseanaylyzer(clean_first)
    sales=salesagent(condense,clean_first)
    return {
        "input_url": url,
        "company_analysis": first,
        "condense_analysis": condense,
        "sales_guidance":sales
    }


def get_company_info(url: str):
    return chat_call(
        "You are an experienced web scraper agent",
        f"""
        Analyze company website: {url}

        Provide:
        - What the company does
        - Revenue model
        - Customers
        - Use of real-time data
        - Impact of real-time data on their business

        Rules:
        - Do not hallucinate
        - Be professional
        - Cite evidence if possible
        """
    )
def condenseanaylyzer(output):
  return chat_call(
      f"You are an expert condense product fit analyzer",
      f'''
      I want you to analyze whether the company given in this particular {output}'s context is fit for using condense as a product {CONDENSE_CONTEXT}.
      '''
  )
def salesagent(condense,company_info):
    return chat_call(
        f"You are a sales guidance agent whose job is to guide the sales team on how to sell our product  condense to the customer",
    f'''
I want you to give some pitch ideas on how to sell our product {condense} to customers based on the company information {company_info}.

   
    '''
    )