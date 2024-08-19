from fastapi import FastAPI, Request
import json
import uvicorn

from botrun_ask_folder.constants import PUBSUB_NAME_EMBEDDING, TOPIC_USER_INPUT_FOLDER

app = FastAPI()


@app.post("/process_user_input_folder")
async def process_user_input_folder(request: Request):
    data = await request.json()
    print(f"Received data: {data}", flush=True)
    return {"success": True}


@app.get("/dapr/subscribe")
def subscribe():
    subscriptions = [
        {
            "pubsubname": PUBSUB_NAME_EMBEDDING,
            "topic": TOPIC_USER_INPUT_FOLDER,
            "route": "/process_user_input_folder",
        }
    ]
    return subscriptions


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
