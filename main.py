from fastapi import FastAPI, HTTPException, Query
import uvicorn
from aws_iam_functions import list_access_keys_by_time

app = FastAPI()

@app.get("/")
def welcome():
    return {
        'endpoints': ['/docs', '/secure/list-access-keys']
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/secure/list-access-keys/")
async def get_access_keys(hours: int = Query(None, description="생성된지 [hours]가 초과한 결과만 가져옵니다.")):
    try:
        keys = list_access_keys_by_time(hours)
        return keys

    except HTTPException as e:
        raise e

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
