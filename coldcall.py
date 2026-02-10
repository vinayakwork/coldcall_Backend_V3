from langchain_google_genai import ChatGoogleGenerativeAI
import os
from condense_context import CONDENSE_CONTEXT
from langchain_groq import ChatGroq
groq_api=os.environ.get("GROQ_API_KEY")
# --- PRIMARY: GROQ ---
groq_llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    groq_api_key=groq_api
)

# --- FALLBACK: GEMINI ---
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.2
)

def normalize_llm_output(output) -> str:
    """
    Converts any LLM response shape into a safe string.
    NEVER returns None.
    """
    if output is None:
        return ""

    if isinstance(output, str):
        return output.strip()

    if isinstance(output, list):
        texts = []
        for item in output:
            if isinstance(item, dict) and "text" in item:
                texts.append(item["text"])
        return "\n".join(texts).strip()

    return str(output).strip()

# ---------- SINGLE ENTRY POINT ----------

def chat_call(system_prompt: str, user_prompt: str) -> str:
    # Try Groq first
    try:
        response = groq_llm.invoke([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])

        content = normalize_llm_output(response.content)
        if content:
            return content

    except Exception as e:
        print("Groq failed, falling back to Gemini:", e)

    # Fallback to Gemini
    response = gemini_llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])

    return normalize_llm_output(response.content)
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
        -Keep the info as detailed as possible
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
And also try to give whom in that {company_info} can we sell our product like for example to the CTO,COO or CEO like that etc ,also try to get the  name of that person from linkedin or anywhere if possible.
Example format:
Pitch 1: Title
Target:like CEO,CTO etc 
what we are going to sell/provide and how it can help them
   
    '''
    )