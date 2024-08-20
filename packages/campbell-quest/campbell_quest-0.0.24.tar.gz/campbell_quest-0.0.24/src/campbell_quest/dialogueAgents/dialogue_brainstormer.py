import ollama

def generate_dialogue(quest, npc, dialogue_context, template, locations, characters):
    brainstorming_dialogue_generation_system_prompt = (f"You are a skilled RPG dialogue writer working on an engaging story for a fantasy role-playing game. "
    f"Your task is to create captivating, context-appropriate dialogue between the player and NPCs that drives the story forward. "
    f"The dialogue should reflect the ongoing quest's narrative, using the provided locations and characters."

    f"\n### Quest Information ###\n"
    f"{quest}\n"
        
    f"\n### Locations ###\n"
    f"{locations}\n"
    
    f"\n### Characters ###\n"
    f"{characters}\n"
    
    f"Make sure the dialogue is natural, aligns with the tone of the quest, and adheres to the following conditions and results:\n"
    
    f"\n### Functions for Conditions ###\n"
    f"1. has_quest(param: quest_name)\n"
    f"2. has_item(param: item_name)\n"
    f"3. completed_objective(param: objective_reference)\n"
    f"4. completed_quest(param: quest_name)\n"
        
    f"\n### Functions for Results ###\n"
    f"1. receive_quest(param: quest_name)\n"
    f"2. complete_objective(param: objective_reference)\n"
    f"3. complete_quest(param: quest_name)\n"
    f"4. attack_player()\n"
    f"5. add_item(param: item_name)\n"
    f"6. remove_item(param: item_name)\n")

    brainstorming_dialogue_generation_user_prompt = (f"Generate dialogue based on the quest, NPC, and context. The NPC should initiate the conversation. "
    f"Use concise, natural lines without descriptions or actions. Keep dialogue consistent with the given template.\n"
    
    f"\n### NPC ###\n"
    f"Name: {npc}\n"
    
    f"\n### Context ###\n"
    f"{dialogue_context}\n"
    
    f"\n### Template ###\n"
    f"{template}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": brainstorming_dialogue_generation_system_prompt
        },
        {
            "role": "user",
            "content": brainstorming_dialogue_generation_user_prompt
        }
    ], options={"temperature": 1.2})

    return response["message"]["content"]