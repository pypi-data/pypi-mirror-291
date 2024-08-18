import ollama

def get_formatted_required_items(required_items, schema):
    formatting_required_items_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"Your task is to encode the items given into a JSON format based on the provided schema.\n"
    f"Review the required items and generate a JSON output that strictly adheres to the schema.\n"
    f"Ensure the output is a valid JSON without including any additional text.\n"
    f"The output should ONLY include the valid JSON.\n"
        
    f"\n###\n"
    
    f"Required Items:\n"
    f"{required_items}\n"
    
    f"\n###\n"
    
    f"Schema:"
    f"{schema}\n"
    
    f"\n###\n"
    
    f"Remember to include ONLY the JSON in the output.\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatting_required_items_system_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]

def get_formatted_item(item):
    formatting_items_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"You are given an item description in JSON format.\n"
    f"Your task is to remove all non-JSON text, leaving only the JSON structure intact.\n"
    f"Ensure the output is a valid JSON without including any additional text.\n"
    f"The output should ONLY include the valid JSON.\n"
    f"Avoid enclosing the response in triple backticks (```).\n"
    
    f"\n###\n"
    
    f"Item:\n"
    f"{item}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatting_items_system_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]