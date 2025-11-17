# Step1: Setup FastAPI backend
from fastapi import FastAPI, Form
from pydantic import BaseModel
import uvicorn

from ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI()

# Step2: Receive and validate request from Frontend
class Query(BaseModel):
    message: str



@app.post("/ask")
async def ask(query: Query):
    try:
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", query.message)]}
        #inputs = {"messages": [("user", query.message)]}
        config = {"recursion_limit": 50}
        stream = graph.stream(inputs, stream_mode="updates", config=config)
        tool_called_name, final_response = parse_response(stream)

        # Ensure we have a response
        if not final_response:
            final_response = "I'm here to support you, but I couldn't generate a response. Please try rephrasing your message."
        
        # Step3: Send response to the frontend
        return {"response": final_response,
                "tool_called": tool_called_name}
    except Exception as e:
        print(f"Error in /ask endpoint: {str(e)}")
        return {"response": f"I encountered an error while processing your request. Please try again.",
                "tool_called": "None"}
    


from fastapi.responses import PlainTextResponse
from xml.etree.ElementTree import Element, tostring

def _twiml_message(body: str) -> PlainTextResponse:
    """Create minimal TwiML <Response><Message>...</Message></Response>"""
    response_el = Element('Response')
    message_el = Element('Message')
    message_el.text = body
    response_el.append(message_el)
    xml_bytes = tostring(response_el, encoding='utf-8')
    return PlainTextResponse(content=xml_bytes, media_type='application/xml')



@app.post("/whatsapp_ask")
async def whatsapp_ask(Body: str = Form(...)): 
    user_text = Body.strip() if Body else ""
    inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_text)]}
    config = {"recursion_limit": 50}
    stream = graph.stream(inputs, stream_mode="updates", config=config)
    tool_called_name, final_response = parse_response(stream)    

    if not final_response:
        final_response = "I'm here to support you, but I couldn't generate a response just now."

    # Step3: Send response to Twilio
    return _twiml_message(final_response)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)







