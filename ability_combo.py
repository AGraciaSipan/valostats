import json
from collections import deque


# Function to handle "player-used-ability" events and build the event list
def handle_player_used_ability(event, sequence_number, events_queue, game_id_filter):
    event_type = event.get("type")
    if event_type != "player-used-ability":
        return

    actor = event.get("actor", {})
    state = actor.get("state", {})

    # Extract player and team information
    player_id = actor.get("id")
    team_id = state.get("teamId")

    game_state = state.get("game", {})
    abilities_list = game_state.get("abilities", [])

    # Extract Game ID from the event
    game_id = event.get("seriesStateDelta", {}).get("games", [{}])[0].get("id")

    # Check if the event's game_id matches the filter
    if game_id != game_id_filter:
        return

    # Collect abilities used in this event
    used_abilities = set()
    for ability in abilities_list:
        ability_id = ability.get("id")
        used_abilities.add(ability_id)

    # Store abilities along with player and team info, and sequence number
    events_queue.append(
        {
            "player_id": player_id,
            "team_id": team_id,
            "abilities": used_abilities,
            "sequence_number": sequence_number,
            "game_id": game_id,
        }
    )


# Function to check ability combination within the window of 8 player-used-ability events
def check_ability_combo(events, ability1_id, ability2_id):
    results = []
    num_events = len(events)

    for i, event in enumerate(events):
        player_id, team_id, abilities, sequence_number, game_id = event.values()

        # Check if the current event has ability1_id
        if ability1_id in abilities:
            # Check the window of events: 4 before and 4 after
            start = max(0, i - 4)
            end = min(num_events, i + 5)

            for j in range(start, end):
                if j == i:
                    continue  # Skip the current event

                next_event = events[j]
                next_player_id, next_team_id, next_abilities, next_sequence_number, next_game_id = next_event.values()

                # Check if the next event has ability2_id and is from the same team
                if ability2_id in next_abilities and team_id == next_team_id:
                    results.append(
                        {
                            "ability1_sequence_number": sequence_number,
                            "ability2_sequence_number": next_sequence_number,
                            "team_id": team_id,
                            "player1_id": player_id,
                            "player2_id": next_player_id,
                            "next_game_id": game_id,
                        }
                    )
                    break

    # Save the results to a JSON file
    if results:
        file_name = f"{game_id}_{ability1_id}_{ability2_id}.json"
        with open(file_name, "w") as file:
            json.dump(results, file, indent=4)
        print(f"Results saved to {file_name}")
    else:
        print("No matching abilities found.")

    return results


# Function to read and process the JSONL data
def read_jsonl_file(input_path, game_id):
    events_queue = deque()

    with open(input_path) as file:
        for line in file:
            try:
                data = json.loads(line.strip())
                sequence_number = data.get("sequenceNumber")  # Extract sequenceNumber from the root level
                events = data.get("events", [])

                for event in events:
                    # Handle the event and build the event queue
                    handle_player_used_ability(event, sequence_number, events_queue, game_id)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
    return events_queue


# Main function to run the process
def main(input_path, game_id, ability1_id, ability2_id):
    # Step 1: Read and process the JSONL file
    events_queue = read_jsonl_file(input_path, game_id)

    # Step 2: Check the ability combination within the processed events
    _ = check_ability_combo(events_queue, ability1_id, ability2_id)


# Example usage
if __name__ == "__main__":
    # Replace these with your specific ability IDs
    ability1_id = "paranoia"  # Ability A
    ability2_id = "fast-lane"  # Ability B
    game_id = "e220cc55-404b-460b-80eb-0248c6d949ee"  # Game 1

    # Replace 'your_input_file_path.jsonl' with the path to your JSONL file
    input_path = "valostats/events_2695430_grid.jsonl"

    main(input_path, game_id, ability1_id, ability2_id)
