import json
import os
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from PIL import Image


class ViewMap:
    def __init__(self, map_name: str, csv_file_path: str):
        # Get the directory of the current script
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.map_name = map_name
        self.csv_file_path = os.path.join(self.base_dir, csv_file_path)
        self.image_file_path = os.path.join(self.base_dir, "..", "assets", "maps", map_name, "display_icon.png")
        self.json_file_path = os.path.join(self.base_dir, "..", "data", "maps", f"{map_name}.json")

        self.selected_map = self.load_map_data()
        self.map_img = self.load_map_image()
        self.current_game = self.load_csv_data()

    def load_map_image(self) -> Image.Image:
        if not os.path.isfile(self.image_file_path):
            raise FileNotFoundError(f"Map image not found: {self.image_file_path}")
        try:
            return Image.open(self.image_file_path)
        except OSError as e:
            raise RuntimeError(f"Failed to load map image: {e}")

    def load_map_data(self) -> dict[str, Any]:
        if not os.path.isfile(self.json_file_path):
            raise FileNotFoundError(f"Map data not found: {self.json_file_path}")
        try:
            with open(self.json_file_path) as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load map data: {e}")

    def load_csv_data(self) -> pd.DataFrame:
        if not os.path.isfile(self.csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
        try:
            return pd.read_csv(self.csv_file_path)
        except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise RuntimeError(f"Failed to load CSV data: {e}")

    def convert_coordinates(self, x: float, y: float, map_data: dict[str, Any]) -> tuple[float, float]:
        x_image = (y * map_data["xMultiplier"]) + map_data["xScalarToAdd"]
        y_image = (x * map_data["yMultiplier"]) + map_data["yScalarToAdd"]
        return x_image, y_image

    def update(
        self, frame: int, players: list[plt.Line2D], map_data: dict[str, Any], plot: plt.Axes
    ) -> list[plt.Line2D]:
        phase = self.current_game.iloc[frame]["phase"]
        round_number = self.current_game.iloc[frame]["roundNumber"]

        for i, scatter in enumerate(players):
            x = self.current_game.iloc[frame][f"{i+1}_x"]
            y = self.current_game.iloc[frame][f"{i+1}_y"]

            if pd.isna(x) or pd.isna(y):
                scatter.set_data([], [])
            else:
                x_img, y_img = self.convert_coordinates(x, y, map_data)
                scatter.set_data([x_img * self.map_img.width], [y_img * self.map_img.height])

        plot.set_title(f"{map_name} Map - Phase: {phase}, Round: {round_number}")
        return players

    def show_map(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(self.map_img, extent=[0, self.map_img.width, self.map_img.height, 0])

        players = [ax.plot([], [], "o", markersize=8, label=f"Player {i+1}")[0] for i in range(10)]

        _ = FuncAnimation(
            fig,
            self.update,
            fargs=(players, self.selected_map, ax),
            frames=len(self.current_game),
            interval=5,
            blit=False,
        )

        # Customize the plot
        ax.set_xlim(0, self.map_img.width)
        ax.set_ylim(self.map_img.height, 0)
        ax.legend(loc="upper right")

        # Display the animation
        plt.show()


# Testing the ViewMap class
if __name__ == "__main__":
    map_name = "Haven"  # Update with your actual map name
    csv_file_path = "prueba.csv"  # Update with your actual CSV file path

    # Create ViewMap instance and show map
    map_view = ViewMap(map_name, csv_file_path)
    map_view.show_map()
