from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from coldcall import inputtooutput

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

@app.get("/")
def welcome():
    return {"status":"Everything is running fine"}

@app.post("/analyze")
async def analyze(req: UrlRequest):
    result = inputtooutput(req.url)
    return {"result": result}
