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
    f"Your task is to review a dialogue tree between the player and an NPC to ensure it is cohesive.\n"
    f"Your objective is to ensure this dialogue tree is COHESIVE.\n"
    f"Ensure there is a \"receive_quest()\" result within the dialogue tree.\n"
    f"If there is not, then include a \"receive_quest()\" result in a place where it makes sense.\n"
    f"Ensure there is a \"complete_quest()\" result within the dialogue tree.\n"
    f"If there is not, then include a \"complete_quest()\" result in a place where it makes sense.\n"
    f"Ensure that the \"condition\" and \"result\" properties only contain functions from the list outlined below:\n"
    
    f"Condition functions available:\n"
    f"1. has_quest(param: quest_name)\n"
    f"2. has_item(param: item_name)\n"
    f"3. completed_objective(param: objective_reference)\n"
    f"4. completed_quest(param: quest_name)\n"
    
    f"\n###\n"
    
    f"Results functions available:\n"
    f"1. receive_quest(param: quest_name)\n"
    f"2. complete_objective(param: objective_reference)\n"
    f"3. complete_quest(param: quest_name)\n"
    f"4. attack_player()\n"
    f"5. add_item(param: item_name)\n"
    f"6. remove_item(param: item_name)\n"
    
    f"\n###\n"
    
    f"Remove any other \"condition\" and \"result\" properties that do not belong in this list.\n"
    
    f"\n###\n"
    
    f"You can reference the example provided:\n"
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