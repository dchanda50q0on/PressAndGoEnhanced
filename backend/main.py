from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from browser_use.agent.service import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with your frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up API key for Langchain Google GenAI
os.environ["GEMINI_API_KEY"] = "AIzaSyBr8eyDTGeLYQU4cP7vYcQqvcnKdf4w2rM"

# Define the request model
class TaskRequest(BaseModel):
    task: list[str]  # List of tasks

@app.post("/execute")
async def execute_task(request: TaskRequest):
    try:
        # Get the task from the frontend
        tasks = request.task

        # Initialize the LLM
        api_key = os.environ["GEMINI_API_KEY"]
        llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=SecretStr(api_key))

        # Initialize the agent
        agent = Agent(tasks, llm, use_vision=True)

        # Execute the task asynchronously
        history = await agent.run()
        test_result = history.final_result()

        return {"result": test_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)