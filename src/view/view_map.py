import json
import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from PIL import Image

from src.models.game_map.game_map import GameMap


class ViewMap:
    def __init__(self, map_name: str, csv_file_path: str):
        # Get the directory of the current script
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.map_name = map_name
        self.csv_file_path = os.path.join(self.base_dir, csv_file_path)
        self.image_file_path = os.path.join(self.base_dir, "..", "assets", "maps", map_name, "display_icon.png")
        self.json_file_path = os.path.join(self.base_dir, "..", "data", "maps", f"{map_name}.json")

        self.selected_map = GameMap.from_json(self.json_file_path)
        self.map_img = self.load_map_image()
        self.current_game = self.load_csv_data()

    def load_map_image(self) -> Image.Image:
        if not os.path.isfile(self.image_file_path):
            raise FileNotFoundError(f"Map image not found: {self.image_file_path}")
        try:
            return Image.open(self.image_file_path)
        except OSError as e:
            raise RuntimeError(f"Failed to load map image: {e}")

    def load_csv_data(self) -> pd.DataFrame:
        if not os.path.isfile(self.csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")
        try:
            return pd.read_csv(self.csv_file_path)
        except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
            raise RuntimeError(f"Failed to load CSV data: {e}")

    def convert_coordinates(self, x: float, y: float, selected_map: GameMap) -> tuple[float, float]:
        x_image = (y * selected_map.x_multiplier) + selected_map.x_scalar_to_add
        y_image = (x * selected_map.y_multiplier) + selected_map.y_scalar_to_add
        return x_image, y_image

    def update(self, frame: int, players: list[plt.Line2D], selected_map: GameMap, plot: plt.Axes) -> list[plt.Line2D]:
        phase = self.current_game.iloc[frame]["phase"]
        round_number = self.current_game.iloc[frame]["roundNumber"]

        for i, scatter in enumerate(players):
            x = self.current_game.iloc[frame][f"{i+1}_x"]
            y = self.current_game.iloc[frame][f"{i+1}_y"]

            if pd.isna(x) or pd.isna(y):
                scatter.set_data([], [])
            else:
                x_img, y_img = self.convert_coordinates(x, y, selected_map)
                scatter.set_data([x_img * self.map_img.width], [y_img * self.map_img.height])

        plot.set_title(f"{self.map_name} Map - Phase: {phase}, Round: {round_number}")
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

    def show_map_with_polygons(self):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(self.map_img, extent=[0, self.map_img.width, self.map_img.height, 0])

        players = [ax.plot([], [], "o", markersize=8, label=f"Player {i+1}")[0] for i in range(10)]

        # Plot each region as a polygon

        json_file_path = os.path.join(self.base_dir, "..", "data", "polygons", f"{self.map_name}.json")
        with open(json_file_path) as file:
            json_data = json.load(file)

        for polygons in json_data["polygons"]:
            region_name = polygons["regionName"] + polygons["superRegionName"]
            x_coords = polygons["location"]["x"]
            y_coords = polygons["location"]["y"]

            # Convert coordinates
            x_img_coords = [x * self.map_img.width for x in x_coords]
            y_img_coords = [(1 - y) * self.map_img.height for y in y_coords]  # Flip y-axis

            # Plot the polygon
            ax.fill(x_img_coords, y_img_coords, color="blue", alpha=0.3)

            # Calculate centroid for labeling
            centroid_x = sum(x_coords) / len(x_coords)
            centroid_y = sum([1 - y for y in y_coords]) / len(y_coords)
            ax.text(
                centroid_x * self.map_img.width,
                centroid_y * self.map_img.height,
                region_name,
                fontsize=10,
                color="yellow",
                ha="center",
                va="center",
            )

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


if __name__ == "__main__":
    map_name = "haven"
    csv_file_path = "prueba.csv"

    view_map = ViewMap(map_name, csv_file_path)
    view_map.show_map_with_polygons()
