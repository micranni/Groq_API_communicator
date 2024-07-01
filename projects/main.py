# get groq API key
# set up python environment
# pip install fastapi and uvicorn
# pip insall groq
# export api key
# make sure to execute code in the directory 'main.py' is in.


import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq



# Initialize the Groq client with the API key from environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Initialize FastAPI app
app = FastAPI()

# Define the request model
class ChatRequest(BaseModel):
    message: str

# Define the response model
class ChatResponse(BaseModel):
    response: str

# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI app. Go to /docs for API documentation."}

# Define the endpoint for chat completion
@app.post("/chat", response_model=ChatResponse)
def get_chat_completion(request: ChatRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
            model="llama3-8b-8192",
        )
        response_message = chat_completion.choices[0].message.content
        return ChatResponse(response=response_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)