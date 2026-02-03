from pydantic import BaseModel, HttpUrl, Field

class AnalyzeRequest(BaseModel):
    url: HttpUrl = Field(
        ...,
        description="Company website URL (must be a valid http/https URL)"
    )

    class Config:
        extra = "forbid"   # 🚨 THIS IS IMPORTANT
