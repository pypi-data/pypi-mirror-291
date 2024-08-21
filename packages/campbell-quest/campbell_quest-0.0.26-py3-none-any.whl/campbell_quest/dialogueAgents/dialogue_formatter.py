import ollama

def get_formatted_required_dialogues(quest, required_dialogues, schema):
    formatting_required_dialogues_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"Your task is to encode the objectives of a quest into a JSON format based on the provided schema.\n"
    f"Review the required dialogues and generate a JSON output that strictly adheres to the schema.\n"
    f"Ensure the output is a valid JSON without including any additional text.\n"
    f"The output should ONLY include the valid JSON.\n"
    
    f"\n###\n"
    
    f"Quest:\n"
    f"{quest}\n"
    
    f"\n###\n"
    
    f"Required Dialogues:\n"
    f"{required_dialogues}\n"
    
    f"\n###\n"
    
    f"Schema:"
    f"{schema}\n"
    
    f"\n###\n"
    
    f"Remember to include ONLY the JSON in the output.\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatting_required_dialogues_system_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]

def get_formatted_dialogue_tree(dialogue_tree):
    formatting_dialogues_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"You are given a dialogue tree in JSON format.\n"
    f"Your task is to remove all non-JSON text, leaving only the JSON structure intact.\n"
    f"Ensure the output is a valid JSON without including any additional text.\n"
    f"The output should ONLY include the valid JSON.\n"
    f"Avoid enclosing the response in triple backticks (```).\n"
    
    f"\n###\n"
    
    f"Dialogue Tree:\n"
    f"{dialogue_tree}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatting_dialogues_system_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]