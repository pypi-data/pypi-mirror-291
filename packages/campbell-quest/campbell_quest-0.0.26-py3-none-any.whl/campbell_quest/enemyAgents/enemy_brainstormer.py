import ollama

def generate_enemy(quest, enemy_context, template):
    brainstorming_dialogue_generation_system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    f"You have been tasked with crafting engaging enemy names for an RPG game.\n"
    f"Using the provided quest and enemy context, your goal is to create a unique enemy name.\n"
    
    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n"

    f"\n###\n"

    f"Enemy Context:\n"
    f"{enemy_context}\n"

    f"\n###\n"

    f"Format the enemy in a clear manner similar to the provided template:\n"
    
    f"{template}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": brainstorming_dialogue_generation_system_prompt
        }
    ], options={"temperature": 0.2})

    return response["message"]["content"]