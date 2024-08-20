import ollama

def format_quest(quest, schema):
    formatter_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"Your task is to encode a given quest into a JSON format according to the provided schema.\n"
    f"Review the quest and generate a JSON output that strictly adheres to the schema.\n"
    f"Ensure the output is a valid JSON without including any additional text.\n"
    f"The output should ONLY include the valid JSON.\n"

    f"\n###\n"
    
    f"Quest:"
    f"{quest}\n"
        
    f"\n###\n"

    f"Schema:"
    f"{schema}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatter_system_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]

def format_quest_with_rewards(quest, reward, schema):
    formatter_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    f"Your task is to add a \"rewards\" field to a JSON object according to the provided schema.\n"
    f"Ensure that the output retains all existing fields in the JSON object and only adds the \"rewards\" field.\n"
    f"DO NOT modify or remove any other fields.\n"
    f"The output should be a valid JSON object with all original information intact, plus the added \"rewards\" field.\n"
    f"The output should ONLY include the valid JSON, without any additional text..\n"

    f"\n###\n"
    
    f"JSON:"
    f"{quest}\n"
    
    f"\n###\n"
    
    f"Reward:"
    f"{reward}\n"
        
    f"\n###\n"

    f"Schema:"
    f"{schema}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": formatter_system_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]