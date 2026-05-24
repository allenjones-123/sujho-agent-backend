import os
import uvicorn
from fastapi import FastAPI, Form, Response
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Clean Abstraction: Import our modular database layer
from database import init_db, query_student_database

load_dotenv()

app = FastAPI(title="Sujho AI Agent Backend")
client = genai.Client()

class BypassNgrokWarningMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["ngrok-skip-browser-warning"] = "true"
        return response

app.add_middleware(BypassNgrokWarningMiddleware)

# Initialize data layer on startup
init_db()

@app.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"📥 Received WhatsApp webhook from {From}: '{Body}'")
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=Body,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are Sujho's AI Teaching Assistant platform for Indian K-12 education. "
                    "You have direct access to our core school data layer via tools. "
                    "If a user asks about a student's metrics, you MUST use `query_student_database`. "
                    "Keep responses warm, highly professional, and under 3-4 sentences."
                ),
                tools=[query_student_database]
            )
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"Error processing agent request."
        print(f"❌ Agent Error: {e}")

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response><Message>{ai_reply}</Message></Response>"""
    return Response(content=twiml_response, media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)