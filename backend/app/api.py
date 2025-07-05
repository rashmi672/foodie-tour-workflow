import os
from fastapi import FastAPI, Form, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from itinery_stack.task_queue.tasks import generate_itinery_task
from itinery_stack.database.mongo_utils import fetch_history, delete_foodie_tour
from itinery_stack.services.generate_speech import speech_generation

app = FastAPI()
# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allowing all origins for simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_foodie_tour")
def generate_foodie_tour(
    city: str = Form(...),
    language: str = Form(default="English")):
    """
    Generate a foodie tour itinerary based on the city.
    This endpoint fetches the current weather, decides dining preferences, dishes and restaurants.
    """
    try:
        task_result = generate_itinery_task.delay(
            city = city,
            language = language
        )
        print(f"Generate foodie tour task ID: {task_result.id}")
        return {"task_id": task_result.id}
    except Exception as e:
        print(f"Error during generate foodie tour: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during generate foodie tour: {str(e)}")

@app.post("/generate-audiobook")
def generate_audiobook(narrative: str = Form(...)):
    """
    Generate an audiobook from the provided narrative text and return the audio directly.
    """
    try:
        audio_path = speech_generation(narrative)
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=500, detail="Audio file was not created.")

        audio_stream = open(audio_path, "rb")
        filename = f"foodie_audiobook.wav"
        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
        return StreamingResponse(audio_stream, media_type="audio/wav", headers=headers)
    except Exception as e:
        print(f"Error during generate audiobook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during generate audiobook: {str(e)}")


# Endpoint: GET TASK RESULT
@app.get("/task-status/{task_id}")
async def get_task_status(
    task_id: str, 
    service: str = Query(...) 
    ):
    """
    Get the response of a task by its ID.
    Checks the status of a task and returns its result if completed.
    """
    task_map = {
        "foodie_tour": generate_itinery_task  # This is the task we are checking
        # other tasks can be added here
    }

    task_cls = task_map.get(service)
    task_result = task_cls.AsyncResult(task_id)
    state = task_result.state

    if state == "FAILURE":     # Handle a failed task without re-raising the exception.
        error_message = str(task_result.result)  # This is the error that occurred in the task
        return {"status": "failed", "result": error_message}
    elif state == "SUCCESS":
        return {"status": "completed", "result": task_result.result}
    else:
        return {"status": state.lower(), "result": None}
    
@app.get("/history")
def get_foodie_tour_history():
    """
    Get all saved foodie tour narratives.
    """
    try:
        entries = fetch_history()
        return {"history": entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.delete("/history")
def delete_foodie_tour_history(id: str = Query(...)):
    """
    Delete a foodie tour record by its exact timestamp.
    """
    try:
        deleted = delete_foodie_tour(id)
        if deleted:
            return {"status": "success", "message": f"Record with id {id} deleted"}
        return {"status": "not_found", "message": "No record found with that id"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    # public_url = ngrok.connect(8000)  # Expose port 8000
    # print(f"Ngrok tunnel URL: {public_url}")
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)