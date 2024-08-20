from .itemAgents import item_brainstormer, item_refiner, item_formatter
import json

def get_items(quest, required_items_schema, item_templates):
    required_items = item_refiner.get_required_items(quest)
    
    formatted_required_items = item_formatter.get_formatted_required_items(required_items, required_items_schema)
    required_items_json = json.loads(formatted_required_items)
    
    item_cues = required_items_json.get("items", [])
    items = []
    for item_cue in item_cues:
        item_type = item_cue.get("item_type")
        item_template = item_templates.get(item_type)
        item = None
        if item_type == "Action Item":
            item = item_brainstormer.generate_action_item(quest, item_cue, item_template)
        else:
            item = item_brainstormer.generate_equipment(quest, item_cue, item_template)
        
        item = item_formatter.get_formatted_item(item)
        items.append(item)
    
    return items