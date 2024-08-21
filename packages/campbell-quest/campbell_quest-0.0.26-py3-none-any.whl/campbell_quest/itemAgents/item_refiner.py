import ollama

def get_required_items(quest):
    refining_required_items_system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    f"Your role is to assist the Narrative Designer by evaluating a Quest concept that has been provided.\n"
    f"This concept outlines a series of objectives related to the player's journey.\n\n"
    
    f"Your task is to carefully analyze each objective and identify any items the player needs to interact with to complete that objective.\n"
    f"Focus only on the items required for interaction; do not include objectives involving NPC interactions, as they do not constitute item interactions.\n"

    f"Once you identify the necessary items, classify each one by selecting a type from the following list:\n"
    f"1. Action Item: Items that can be used one time, providing temporary benefits, effects, or simply filling a spot in the inventory.\n"
    f"These may be consumed upon use or have limited duration. They might offer direct advantages, trigger events, or serve as collectibles.\n"
    f"2. Equipment: Items that can be worn or wielded to enhance the player's abilities or alter their appearance.\n"
    f"These items can be equipped in various slots (e.g., head, chest, weapon).\n"
    f"3. Stat-Boosting Equipment: Equipment that offers permanent stat bonuses or other lasting benefits while equipped.\n\n"
    
    f"Once you have classified the items, your next task is to determine the most appropriate objective type for each item based on the player's interaction with it. Choose from the following two options:\n"
    f"1. Pickup Item: The item must be collected or acquired by the player, typically to be added to their inventory or used later in the quest.\n"
    f"2. Destroy Item: The item must be eliminated, broken, or otherwise removed from existence by the player as part of the quest objective.\n"
        
    f"\n###\n"
    
    f"Ensure that the output contains ONLY ITEMS, omitting any characters (whether enemies, allies, or otherwise).\n"
    f"Use the following format for the output:\n"
    f"Item Name:\nItem Type:\nObjective Reference:\nObjective Type:\n")
    
    refining_required_items_user_prompt = (f"Consider the quest given and determine whether the player needs to interact with an item.\n"
    f"Adhere to the system instructions.\n"

    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": refining_required_items_system_prompt
        },
        {
            "role": "user",
            "content": refining_required_items_user_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]