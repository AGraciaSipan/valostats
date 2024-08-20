import json

import pandas as pd


class ReadRiotJsonl:
    def __init__(self, jsonl_file):
        self.jsonl_file = jsonl_file

    def process_jsonl(self):
        all_rows = []
        game_id = None

        with open(self.jsonl_file) as f:
            for line in f:
                data = json.loads(line)  # Parse each line as a JSON object

                # Check if snapshot is present in the current JSON object
                if "snapshot" in data:
                    # Extract the phase and round number
                    phase = data["metadata"]["currentGamePhase"]["phase"]
                    round_number = data["metadata"]["currentGamePhase"]["roundNumber"]
                    current_game_id = data["metadata"]["gameId"]["value"]

                    # If it's a new game, save the previous game's data and reset
                    if game_id and game_id != current_game_id:
                        self.save_to_csv(all_rows, game_id)
                        all_rows = []  # Reset for the next game

                    game_id = current_game_id  # Update the current game ID

                    # Use a dictionary to store the positions grouped by timestamps
                    timestamp_dict = {}

                    # Iterate over players
                    for player in data["snapshot"].get("players", []):
                        player_id = player["playerId"]["value"]

                        # Iterate over timeseries data for the current player
                        for timeseries in player.get("timeseries", []):
                            position = timeseries["position"]
                            timestamp = timeseries["timestamp"]["includedPauses"]

                            # If this timestamp is not in the dictionary, add it
                            if timestamp not in timestamp_dict:
                                timestamp_dict[timestamp] = {
                                    "phase": phase,
                                    "roundNumber": round_number,
                                    "timestamp_includedPauses": timestamp,
                                }

                            # Store the x and y positions for this player at this timestamp
                            timestamp_dict[timestamp][f"{player_id}_x"] = position["x"]
                            timestamp_dict[timestamp][f"{player_id}_y"] = position["y"]

                    # Convert the dictionary for this JSON object into a list of rows and add it to the overall list
                    rows = (
                        pd.DataFrame.from_dict(timestamp_dict, orient="index").reset_index(drop=True).to_dict("records")
                    )
                    all_rows.extend(rows)  # Add rows to the overall list

                # Check if the game phase is GAME_ENDED and save the current match's data
                if "gamePhase" in data and data["gamePhase"]["phase"] == "GAME_ENDED":
                    self.save_to_csv(all_rows, game_id)
                    all_rows = []  # Reset for the next match

    def save_to_csv(self, all_rows, game_id):
        # Convert the combined list of rows into a DataFrame and save as a CSV
        df = pd.DataFrame(all_rows)
        if not df.empty:  # Check if DataFrame is not empty
            filename = f"output_{game_id}.csv"
            df.to_csv(filename, index=False)  # Save to CSV
            print(f"Saved {filename}")


if __name__ == "__main__":
    reader = ReadRiotJsonl("match/events_2695430_riot.jsonl")
    reader.process_jsonl()
