# from valorant_client.client import ValorantClient, ValorantConstants
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.animation import FuncAnimation
from PIL import Image


class view_map:
    # Function to convert in-game coordinates to image coordinates
    def convert_coordinates(self, x, y, map_data):
        x_image = (y * map_data["xMultiplier"]) + map_data["xScalarToAdd"]
        y_image = (x * map_data["yMultiplier"]) + map_data["yScalarToAdd"]

        return x_image, y_image

    # Function to update the plot for each frame
    def update(self, frame, current_game, players, map_data, plot, map_img):
        phase = current_game.iloc[frame]["phase"]
        round_number = current_game.iloc[frame]["roundNumber"]

        for i, scatter in enumerate(players):
            x = current_game.iloc[frame][f"{i+1}_x"]
            y = current_game.iloc[frame][f"{i+1}_y"]

            # Check if the x or y is void (NaN or empty)
            if pd.isna(x) or pd.isna(y):
                scatter.set_data([], [])  # Hide the player marker
            else:
                x_img, y_img = self.convert_coordinates(x, y, map_data)
                scatter.set_data([x_img * map_img.width], [y_img * map_img.height])

        # Update the title with phase and round number
        plot.set_title(f"{map_data['displayName']} Map - Phase: {phase}, Round: {round_number}")
        return players

    def show_map(self, map_name, current_game):
        # TODO fix import
        """client = ValorantClient()

        selected_map = client.get_map_by_uuid(UUID(ValorantConstants.Maps[map_name]))"""
        selected_map = {
            "status": 200,
            "data": {
                "uuid": "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047",
                "displayName": "Haven",
                "tacticalDescription": "A/B/C Sites",
                "coordinates": "27\u00B028\u0027A\u0027N,89\u00B038\u0027WZ\u0027E",
                "displayIcon": (
                    "https://media.valorant-api.com/maps/" "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/" "displayicon.png"
                ),
                "xMultiplier": 7.5e-05,
                "yMultiplier": -7.5e-05,
                "xScalarToAdd": 1.09345,
                "yScalarToAdd": 0.642728,
                "callouts": [
                    {"regionName": "Garden", "superRegionName": "A", "location": {"x": 3100.261, "y": -4683.6016}},
                    {"regionName": "Link", "superRegionName": "A", "location": {"x": 4244.4214, "y": -10715.68}},
                    {"regionName": "Lobby", "superRegionName": "A", "location": {"x": 3438.537, "y": -6260.409}},
                    {"regionName": "Long", "superRegionName": "A", "location": {"x": 6209.695, "y": -6901.142}},
                    {"regionName": "Sewer", "superRegionName": "A", "location": {"x": 3452.8735, "y": -7915.7246}},
                    {"regionName": "Site", "superRegionName": "A", "location": {"x": 6309.3076, "y": -9225.703}},
                    {
                        "regionName": "Spawn",
                        "superRegionName": "Attacker Side",
                        "location": {"x": 1741.7622, "y": -2642.7925},
                    },
                    {"regionName": "Back", "superRegionName": "B", "location": {"x": 1966.1608, "y": -10664.775}},
                    {"regionName": "Site", "superRegionName": "B", "location": {"x": 1884.706, "y": -9231.335}},
                    {"regionName": "Link", "superRegionName": "C", "location": {"x": -87.761444, "y": -10004.415}},
                    {"regionName": "Lobby", "superRegionName": "C", "location": {"x": -1642.189, "y": -5720.345}},
                    {"regionName": "Long", "superRegionName": "C", "location": {"x": -3356.814, "y": -5990.872}},
                    {"regionName": "Garage", "superRegionName": "C", "location": {"x": 180.07678, "y": -7999.5845}},
                    {"regionName": "Window", "superRegionName": "C", "location": {"x": -10.126678, "y": -8993.241}},
                    {"regionName": "Site", "superRegionName": "C", "location": {"x": -2378.1328, "y": -9010.557}},
                    {"regionName": "Cubby", "superRegionName": "C", "location": {"x": -2119.7693, "y": -6561.603}},
                    {
                        "regionName": "Spawn",
                        "superRegionName": "Defender Side",
                        "location": {"x": 2946.3042, "y": -12714.707},
                    },
                    {"regionName": "Doors", "superRegionName": "Mid", "location": {"x": 151.11594, "y": -6262.9155}},
                    {
                        "regionName": "Courtyard",
                        "superRegionName": "Mid",
                        "location": {"x": 1822.1299, "y": -6712.6875},
                    },
                    {"regionName": "Window", "superRegionName": "Mid", "location": {"x": 1950.2218, "y": -5567.912}},
                    {"regionName": "Tower", "superRegionName": "A", "location": {"x": 6721.4043, "y": -10472.5205}},
                ],
            },
        }

        # Load the map image
        response = requests.get(selected_map["data"]["displayIcon"])
        map_img = Image.open(BytesIO(response.content))

        # Create a plot with the map as the background
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(map_img, extent=[0, map_img.width, map_img.height, 0])

        # Initialize scatter plots for the players
        players = []
        for i in range(1, 11):
            # TODO assing teams, and related names
            (scatter,) = ax.plot([], [], "o", markersize=8, label=f"Player {i}")
            players.append(scatter)

        # Create animation
        _ = FuncAnimation(
            fig,
            self.update,
            fargs=(current_game, players, selected_map["data"], ax, map_img),
            frames=len(current_game),
            interval=5,
            blit=False,
        )

        # Customize the plot
        ax.set_xlim(0, map_img.width)
        ax.set_ylim(map_img.height, 0)
        ax.legend(loc="upper right")

        # Display the animation
        plt.show()


if __name__ == "__main__":
    map_view = view_map()
    csv_file_path = "view/prueba.csv"  # Replace with your CSV file path
    data = pd.read_csv(csv_file_path)
    map_view.show_map("Triad", data)  # 'Triad' Haven
