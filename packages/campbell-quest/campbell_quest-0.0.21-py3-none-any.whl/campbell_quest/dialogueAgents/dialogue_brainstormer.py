import ollama

def generate_dialogue(quest, npc, dialogue_context, template, locations, characters):
    brainstorming_dialogue_generation_system_prompt = (f"You are a Writer at a Game studio.\n"
    f"You have been tasked with creating compelling dialogue for a Role-Playing Game.\n"
    f"Using the provided quest, location, and character information, generate suitable dialogue between the player and the NPC as specified in the dialogue context.\n"
    f"Ensure the dialogue is engaging and fits the context of the quest.\n"

    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n"

    f"\n###\n"

    f"Locations:\n"
    f"{locations}\n"

    f"\n###\n"

    f"Characters:\n"
    f"{characters}\n")
    
    brainstorming_dialogue_generation_user_prompt = (f"As a Writer at a Game Studio, your task is to generate appropriate dialogue based on the given dialogue context and system instructions.\n"
    f"Generate dialogue where the NPC initiates the conversation.\n"
    f"Ensure the dialogue contains only spoken lines; exclude any actions or descriptions.\n"
    f"Ensure you do not introduce new characters or locations, and avoid adding any extra requirements or restrictions.\n"
    
    f"\n###\n"
    
    f"NPC Name: {npc}\n"
    
    f"\n###\n"
    
    f"Dialogue Context:\n"
    f"{dialogue_context}\n"
    
    f"\n###\n"
    
    f"Do NOT introduce any new condition or reward functions that are not given below.\n"
    f"Format the dialogue in a clear manner similar to the provided template:\n"
    
    f"{template}\n"
    
    f"\n###\n"
    
    f"The functions available for the conditions are:\n"
    f"1. has_quest(param: quest_name)\n"
    f"2. has_item(param: item_name)\n"
    f"3. completed_objective(param: objective_reference)\n"
    f"4. completed_quest(param: quest_name)\n"
    
    f"\n###\n"
    
    f"The functions available for the results are:\n"
    f"1. receive_quest(param: quest_name)\n"
    f"2. complete_objective(param: objective_reference)\n"
    f"3. complete_quest(param: quest_name)\n"
    f"4. attack_player()\n"
    f"5. add_item(param: item_name)\n"
    f"6. remove_item(param: item_name)\n"
    
    f"\n###\n"
    
    f"Verify that the conditions and results for each segment are consistent and make sense.\n"
    f"Output the dialogue in a SINGLE unified structure.\n")
    
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