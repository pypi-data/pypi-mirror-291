from .questAgents import quest_brainstormer, quest_refiner, quest_formatter

def generate_initial_quest(quest_prompt, objective_info, location_info, character_info):
    initial_generated_quest = quest_brainstormer.generate_quest(objective_info, quest_prompt, location_info, character_info)
    return initial_generated_quest

def generate_quest_with_objectives(initial_generated_quest, location_info, character_info):
    quest_with_objectives = quest_refiner.define_quest_objectives(initial_generated_quest, location_info, character_info)
    return quest_with_objectives

def generate_quest_reward(initial_generated_quest, rewards):    
    quest_reward = quest_refiner.define_quest_reward(initial_generated_quest, rewards)
    return quest_reward

def get_formatted_quest(quest, schema):
    return quest_formatter.format_quest(quest, schema)

def get_formatted_quest_with_rewards(quest, reward, schema):
    return quest_formatter.format_quest_with_rewards(quest, reward, schema)

