from langchain_core.tools import tool
from tools import query_medgemma, call_emergency
from langchain_groq import ChatGroq

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


@tool
def emergency_call_tool() -> None:
    """
    Place an emergency call to the safety helpline's phone number via Twilio.
    Use this only if the user expresses suicidal ideation, intent to self-harm,
    or describes a mental health emergency requiring immediate help.
    """
    call_emergency()

# import googlemaps
# from config import GOOGLE_MAPS_API_KEY
# gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    geocode_result = gmaps.geocode(location)
    lat_lng = geocode_result[0]['geometry']['location']
    lat, lng = lat_lng['lat'], lat_lng['lng']
    places_result = gmaps.places_nearby(
            location=(lat, lng),
            radius=5000,
            keyword="Psychotherapist"
        )
    output = [f"Therapists near {location}:"]
    top_results = places_result['results'][:5]
    for place in top_results:
            name = place.get("name", "Unknown")
            address = place.get("vicinity", "Address not available")
            details = gmaps.place(place_id=place["place_id"], fields=["formatted_phone_number"])
            phone = details.get("result", {}).get("formatted_phone_number", "Phone not available")

            output.append(f"- {name} | {address} | {phone}")

    
    return "\n".join(output)


# Step1: Create an AI Agent & Link to backend
# from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
# from config import OPENAI_API_KEY
from config import GROQ_API_KEY


tools = [ask_mental_health_specialist, emergency_call_tool, find_nearby_therapists_by_location]
# llm = ChatOpenAI(model="gpt-4", temperature=0.2, api_key=OPENAI_API_KEY)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2, api_key=GROQ_API_KEY)
graph = create_react_agent(llm, tools=tools)

SYSTEM_PROMPT = """
You are a compassionate AI mental health assistant. You help users by:

1. Using `ask_mental_health_specialist` tool ONCE to get therapeutic guidance for general questions
2. Using `find_nearby_therapists_by_location` tool if user asks for local therapist recommendations  
3. Using `emergency_call_tool` ONLY if user expresses suicidal thoughts or immediate self-harm risk

IMPORTANT: 
- Call each tool only ONCE per user message
- After receiving tool results, provide your response directly to the user
- Do NOT call tools repeatedly
- Be warm, supportive, and professional in your responses
"""

def parse_response(stream):
    tool_called_name = "None"
    final_response = None

    for s in stream:
        # Check if a tool was called
        tool_data = s.get('tools')
        if tool_data:
            tool_messages = tool_data.get('messages')
            if tool_messages and isinstance(tool_messages, list):
                for msg in tool_messages:
                    tool_called_name = getattr(msg, 'name', 'None')

        # Check if agent returned a message
        agent_data = s.get('agent')
        if agent_data:
            messages = agent_data.get('messages')
            if messages and isinstance(messages, list):
                for msg in messages:
                    if msg.content:
                        final_response = msg.content

    return tool_called_name, final_response


"""if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        print(f"Received user input: {user_input[:200]}...")
        inputs = {"messages": [("system", SYSTEM_PROMPT), ("user", user_input)]}
        stream = graph.stream(inputs, stream_mode="updates")
        tool_called_name, final_response = parse_response(stream)
        print("TOOL CALLED: ", tool_called_name)
        print("ANSWER: ", final_response)"""
        