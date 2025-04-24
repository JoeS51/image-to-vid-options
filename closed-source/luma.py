from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

class VideoReq(BaseModel):
    prompt: str
    model: str
    keyframes: dict

LUMA_APP_URL = "https://api.lumalabs.ai/dream-machine/v1/generations"
LUMA_API_KEY = "luma-847bec3c-13db-47a0-8386-6e869e500e44-1b817fac-9e0a-4ded-a4bf-a7394f492a41"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/generate-video")
async def generate_video(req: VideoReq):
    headers = {
        "Authorization": f"Bearer {LUMA_API_KEY}",
        "content-type": "application/json",
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            LUMA_APP_URL,
            headers=headers,
            json=req.dict()
        )
    
    return {
        "status": response.status_code,
        "response": response.json()
    }

@app.get("/check-status/{job_id}")
async def check_status(job_id: str):
    headers = {"Authorization": f"Bearer {LUMA_API_KEY}"}
    url = f"https://api.lumalabs.ai/dream-machine/v1/generations/{job_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    return response.json()
