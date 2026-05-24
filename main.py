import os
import uvicorn
from fastapi import FastAPI, Form, Response
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import data layer tools
from database import init_db, query_student_database, get_user_profile

load_dotenv()

app = FastAPI(title="Sujho Role-Based Multi-Agent System")
client = genai.Client()

class BypassNgrokWarningMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["ngrok-skip-browser-warning"] = "true"
        return response

app.add_middleware(BypassNgrokWarningMiddleware)

init_db()

@app.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"\n📥 Inbound Webhook Received from sender number: {From}")
    print(f"💬 Message content: '{Body}'")
    
    # 1. SECURITY LAYER: Check user registry
    user_profile = get_user_profile(From)
    
    if not user_profile:
        # Handling unauthorized or unknown outside numbers
        ai_reply = "Welcome to Sujho. This phone number is not currently registered in our school information system. Please request your class coordinator to update your metrics profile."
    else:
        user_name = user_profile["name"]
        user_role = user_profile["role"]
        target_child = user_profile["associated_student"]
        
        print(f"🛡️ [ACCESS GRANTED]: Authenticated '{user_name}' as Role: '{user_role}'")
        
        # 2. CONTEXT & SYSTEM INSTRUCTION POLICIES BASED ON ROLES
        if user_role == "TEACHER":
            system_prompt = (
                f"You are Sujho's AI Assistant supporting the teacher: {user_name}. "
                "You have administrative clearance. You can look up ANY student's profile "
                "using the `query_student_database` tool whenever asked. Keep responses crisp."
            )
        elif user_role == "PARENT":
            system_prompt = (
                f"You are Sujho's AI Assistant speaking with {user_name}, the parent of {target_child}. "
                f"SECURITY POLICY: You have access to information ONLY for {target_child}. "
                f"If the parent asks about their child, you must look them up using `query_student_database` with parameter '{target_child}'. "
                f"If the parent explicitly tries to ask about other students like 'Aanya' or 'Kabir', you must firmly but politely deny the request "
                "stating that cross-student profiles are strictly restricted for data privacy rules."
            )
        else: # STUDENT Role
            system_prompt = (
                f"You are Sujho's student study buddy speaking to {user_name}. "
                "You do NOT have access to the grading database tool. Encourage them to study hard, "
                "and help them answer basic study questions, but tell them to ask their teacher for official grades."
            )

        # 3. CONSTRUCT AGENT INSTANCE WITH CONDITIONAL TOOLING ACCESS
        # If user is a student, we strip the database lookup entirely!
        available_tools = [query_student_database] if user_role in ["TEACHER", "PARENT"] else []

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=Body,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=available_tools
                )
            )
            ai_reply = response.text
        except Exception as e:
            ai_reply = "Processing error encountered within the authorization matrix."
            print(f"❌ Core Agent Error: {e}")

    print(f"📤 Outbound Routing Response:\n{ai_reply}\n")

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response><Message>{ai_reply}</Message></Response>"""
    return Response(content=twiml_response, media_type="application/xml")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)