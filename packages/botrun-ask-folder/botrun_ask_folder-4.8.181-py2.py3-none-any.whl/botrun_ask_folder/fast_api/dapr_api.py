from fastapi import FastAPI
from pydantic import BaseModel, Field
from botrun_ask_folder.services.drive.drive_store import (
    DRIVE_FOLDER_STORE_NAME,
    DriveFolderStore,
)
from botrun_ask_folder.constants import (
    PUBSUB_NAME_EMBEDDING,
    STATE_STORE_NAME,
    TOPIC_USER_INPUT_FOLDER,
)
from dapr.clients import DaprClient

app = FastAPI()


class FolderRequest(BaseModel):
    folder_id: str
    force: bool = False


@app.post("/process-folder")
async def process_folder(request: FolderRequest):
    print(f"receive folder {request.folder_id} with force={request.force}")
    with DaprClient() as client:
        # Publish message
        print(
            f"publish message to topic {TOPIC_USER_INPUT_FOLDER}: {request.folder_id}"
        )
        result = client.publish_event(
            pubsub_name=PUBSUB_NAME_EMBEDDING,
            topic_name=TOPIC_USER_INPUT_FOLDER,
            data=request.model_dump_json(),
            data_content_type="application/json",
        )
        # Save state
        print(f"save state to statestore: {request.folder_id}")
        client.save_state(
            store_name=STATE_STORE_NAME,
            key=DriveFolderStore.get_drive_folder_store_key(request.folder_id),
            value="processing",
        )
    print(f"state saved: {request.folder_id}")
    return {
        "message": f"Drive folder {request.folder_id}, with force={request.force} processing initiated",
        "status": "success",
    }


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
