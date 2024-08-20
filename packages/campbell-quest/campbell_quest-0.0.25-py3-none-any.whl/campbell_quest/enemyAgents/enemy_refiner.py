import ollama

def get_required_enemies(quest):
    refining_required_enemies_system_prompt = (f"You are a dedicated AI Assistant working at a game studio.\n"
    f"Your role is to assist the Narrative Designer by evaluating a Quest concept that has been provided.\n"
    f"This concept outlines a series of objectives related to the player's journey.\n\n"
    
    f"Your task is to carefully analyze each objective and identify any enemies the player needs to fight with to complete that objective.\n"
    f"Focus only on the enemies; do not include objectives involving friendly interactions.\n"
    
    f"Use the following format for the output:\n"
    f"Enemy Name:\nObjective Reference:\n")
    
    refining_required_enemies_user_prompt = (f"Consider the quest given and determine whether the player needs to fight with an enemy.\n"
    f"Adhere to the system instructions.\n"

    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": refining_required_enemies_system_prompt
        },
        {
            "role": "user",
            "content": refining_required_enemies_user_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]