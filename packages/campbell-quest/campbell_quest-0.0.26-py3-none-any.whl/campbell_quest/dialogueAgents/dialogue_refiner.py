import ollama

def get_required_dialogues(quest, characters):
    refining_required_dialogues_system_prompt = (f"As a Writer at a Game Studio, you have received a Quest concept from the Narrative Designer.\n"
    f"This concept includes a list of required objectives.\n"
    f"Your task is to review each objective and determine if it involves the player needing to interact with an NPC.\n"
    
    f"\n###\n"
    
    f"Only output the objectives which require player interaction.\n"
    f"Describe the output in the format given:\n"
    f"NPC Name:\nObjective\n")
    
    refining_required_dialogues_user_prompt = (f"Consider the quest and characters given and determine whether the player needs to talk to an NPC.\n"
    f"Adhere to the system instructions.\n"

    f"\n###\n"

    f"Quest:\n"
    f"{quest}\n"
    
    f"\n###\n"
    
    f"Characters:\n"
    f"{characters}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": refining_required_dialogues_system_prompt
        },
        {
            "role": "user",
            "content": refining_required_dialogues_user_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]

def check_dialogue_tree(dialogue, example):
    checking_dialogue_system_prompt = (f"You are a helpful AI Assistant at a game studio.\n"
    "Your task is to ensure that the dialogue tree between a player and an NPC is cohesive and logically consistent. "
    "Each branch of the dialogue must flow naturally and make sense within the overall story. "
    "The conditions and outcomes should align with the context of the story and character interactions.\n"
    
    "Your objective is to review the dialogue tree and check that the flow of the conversation maintains narrative integrity. "
    "Ensure that the dialogue branches have logical transitions and lead to coherent outcomes.\n\n"
        
    "Additionally, ensure that the `condition` and `result` properties use only the following functions:\n"
    
    "### Available Condition Functions:\n"
    "1. has_quest(param: quest_name)\n"
    "2. has_item(param: item_name)\n"
    "3. completed_objective(param: objective_reference)\n"
    "4. completed_quest(param: quest_name)\n\n"
    
    "### Available Result Functions:\n"
    "1. receive_quest(param: quest_name)\n"
    "2. complete_objective(param: objective_reference)\n"
    "3. complete_quest(param: quest_name)\n"
    "4. attack_player()\n"
    "5. add_item(param: item_name)\n"
    "6. remove_item(param: item_name)\n\n"
    
    "Remove any `condition` or `result` properties not listed above. "
    "Insert missing quest functions where they logically belong within the dialogue tree.\n\n"
    
    "### Example Dialogue Tree:\n"
    f"{example}\n")
    
    checking_dialogue_user_prompt = (f"Check the dialogue tree given below according to system instructions.\n"
            
    f"\n###\n"
    
    f"Dialogue:\n"
    f"{dialogue}\n")
    
    response = ollama.chat(model="llama3.1", messages=[
        {
            "role": "system",
            "content": checking_dialogue_system_prompt
        },
        {
            "role": "user",
            "content": checking_dialogue_user_prompt
        }
    ], options={"temperature": 0})

    return response["message"]["content"]