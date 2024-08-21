import ollama

def generate_action_item(quest, item_context, template):
    brainstorming_dialogue_generation_system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    f"You have been tasked with crafting engaging and immersive item descriptions for an RPG game.\n"
    f"Using the provided quest and item context, your goal is to create descriptions that not only fit seamlessly into the world but also enhance the player's experience.\n"
    
    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n"

    f"\n###\n"

    f"Item Context:\n"
    f"{item_context}\n"

    f"\n###\n"

    f"Format the item in a clear manner similar to the provided template:\n"
    
    f"{template}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": brainstorming_dialogue_generation_system_prompt
        }
    ], options={"temperature": 1.2})

    return response["message"]["content"]

def generate_equipment(quest, item_context, template):
    brainstorming_dialogue_generation_system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    f"You have been tasked with crafting engaging and immersive item descriptions for an RPG game.\n"
    f"Using the provided quest and item context, your goal is to create descriptions that not only fit seamlessly into the world but also enhance the player's experience.\n"
    
    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n"

    f"\n###\n"

    f"Item Context:\n"
    f"{item_context}\n"

    f"\n###\n"

    f"Based on the item's characteristics, assign an appropriate value to the \"allowedEquipLocation\" field from the following options:\n"
    f"Helmet, Necklace, Body, Trousers, Boots, Weapon, Shield, Gloves.\n"
    f"Ensure the location reflects the nature and usage of the item within the game context.\n"

    f"\n###\n"

    f"Format the item in a clear manner similar to the provided template:\n"
    
    f"{template}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": brainstorming_dialogue_generation_system_prompt
        }
    ], options={"temperature": 1.2})

    return response["message"]["content"]