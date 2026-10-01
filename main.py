from openai import OpenAI
from config import GROQ_API_KEY, MODEL
from tools import calculator, read_notes, list_notes
import json

# Create connection to Groq
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Tell the AI about our tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_notes",
           "description": (
    "Read a study note from the notes folder. "
    "Use list_notes first if you do not know the available filenames."
),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                       "description": "The exact filename returned by list_notes."
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "list_notes",
        "description": "List all available study notes in the notes folder.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
}
]

# Ask the user
question = input("You: ")

# Store conversation
messages = [
    {
        "role": "system",
        "content": (
            "You are a Student Study Assistant. "
"Help the student using their study notes and calculator when needed. "
"Use only information found in the provided study notes when answering "
"study-note questions. Do not add outside information. "
"If the requested information is not covered in the notes, clearly say "
"that it is not covered in the notes. "
"When the student asks for a quiz, read the relevant notes first "
"and create questions based only on those notes."
        )
    },
    {
        "role": "user",
        "content": question
    }
]

# Agent loop
for step in range(5):

    print(f"\nAgent step {step + 1}")

    # Ask AI what to do
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools
    )

    message = response.choices[0].message

    # If AI does not need a tool, we have the final answer
    if not message.tool_calls:

        print("\nAssistant:")
        print(message.content)
        break

    # Add AI's tool request to conversation
    messages.append(message)

    # Execute every tool requested by AI
    for tool_call in message.tool_calls:

        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        print("Using tool:", tool_name)

        # Calculator
        if tool_name == "calculator":
            result = calculator(arguments["expression"])

        # Notes
        elif tool_name == "read_notes":
            result = read_notes(arguments["filename"])

        elif tool_name == "list_notes":
            result = list_notes()    

        else:
            result = "Unknown tool"

        print("Tool result received.")

        # Give tool result back to AI
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })