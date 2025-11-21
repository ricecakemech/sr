import json
from collections import defaultdict

def load_json_file(filepath):
    """Load a JSON file and return its content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def create_hash_map(textmap_data):
    """Create a dictionary mapping hash values to text."""
    hash_map = {}
    if isinstance(textmap_data, list):
        for entry in textmap_data:
            if isinstance(entry, dict) and 'textMapHash' in entry and 'text' in entry:
                hash_map[entry['textMapHash']] = entry['text']
    return hash_map

def process_back_equipment(equipment_data, hash_map):
    """Process GridFightBackEquipment data and create enriched output."""
    result = []
    
    for equipment in equipment_data:
        entry = {
            'RoleID': equipment.get('RoleID'),
            'EquipmentID': equipment.get('EquipmentID'),
            'Level': equipment.get('Level'),
            'DescHashValue': equipment.get('BackEquipmentDesc', {}).get('Hash'),
            'DescText': hash_map.get(str(equipment.get('BackEquipmentDesc', {}).get('Hash')), 'NOT FOUND'),
            'Parameters': equipment.get('ParamList', []),
            'ParamFormat': equipment.get('ParamFormat'),
            'DescParamList': [] # Assuming no desc params in equipment data
                }
        result.append(entry)
    
    return result

def process_role_rank(rank_data, hash_map):
    """Process GridFightBackRoleRank data and create enriched output."""
    result = []
    
    for rank in rank_data:
        entry = {
            'RankID': rank.get('RankID'),
            'Rank': rank.get('Rank'),
            'NameHashValue': rank.get('Name', {}).get('Hash'),
            'NameText': hash_map.get(str(rank.get('Name', {}).get('Hash')), 'NOT FOUND'),
            'DescHashValue': rank.get('Desc', {}).get('Hash'),
            'DescText': hash_map.get(str(rank.get('Desc', {}).get('Hash')), 'NOT FOUND'),
            'DescParamList': rank.get('DescParamList', []),
            'IconPath': rank.get('IconPath'),
            'TriggerHash': rank.get('Trigger', {}).get('Hash'),
            'ModifyEnergyBar': rank.get('ModifyEnergyBar', {}).get('Value') if 'ModifyEnergyBar' in rank else None
        }
        result.append(entry)
    
    return result

def save_json_file(data, filepath):
    """Save data to a JSON file."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

def main():
    # File paths - UPDATE THESE WITH YOUR ACTUAL FILE PATHS
    back_equipment_path = 'GridFightBackEquipment.json'
    back_role_rank_path = 'GridFightBackRoleRank.json'
    textmap_path = 'TextMap.json'  # Your textmap file
    
    output_back_equipment_path = 'processed_GridFightBackEquipment.json'
    output_role_rank_path = 'processed_GridFightBackRoleRank.json'
    
    print("Loading files...")
    
    # Load all files
    back_equipment_data = load_json_file(back_equipment_path)
    back_role_rank_data = load_json_file(back_role_rank_path)
    textmap_data = load_json_file(textmap_path)
    
    if not all([back_equipment_data, back_role_rank_data, textmap_data]):
        print("Error: Could not load one or more files.")
        return
    
    print("Creating hash map from textmap...")
    hash_map = create_hash_map(textmap_data)
    print(f"Loaded {len(hash_map)} hash mappings")
    
    print("Processing GridFightBackEquipment...")
    processed_equipment = process_back_equipment(back_equipment_data, hash_map)
    save_json_file(processed_equipment, output_back_equipment_path)
    
    print("Processing GridFightBackRoleRank...")
    processed_ranks = process_role_rank(back_role_rank_data, hash_map)
    save_json_file(processed_ranks, output_role_rank_path)
    
    print("\nProcessing complete!")
    print(f"Equipment entries: {len(processed_equipment)}")
    print(f"Rank entries: {len(processed_ranks)}")
    
    # Print sample entries
    print("\n--- Sample Equipment Entry ---")
    if processed_equipment:
        print(json.dumps(processed_equipment[0], indent=2, ensure_ascii=False))
    
    print("\n--- Sample Rank Entry ---")
    if processed_ranks:
        print(json.dumps(processed_ranks[0], indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()