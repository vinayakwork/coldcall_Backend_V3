from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    temperature=0.2,
)

def chat_call(system_prompt, user_prompt):
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    return response.content

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
