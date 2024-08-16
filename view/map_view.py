from io import BytesIO
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.animation import FuncAnimation
from PIL import Image


class ViewMap:
    def __init__(self, map_name: str, csv_file_path: str):
        self.map_name = map_name
        self.csv_file_path = csv_file_path
        self.selected_map = self.load_map_data()
        self.map_img = self.load_map_image()
        self.current_game = pd.read_csv(csv_file_path)

    def load_map_data(self) -> dict[str, Any]:
        # TODO this fetch from the client
        # Here it's hardcoded for simplicity
        return {
            "status": 200,
            "data": {
                "uuid": "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047",
                "displayName": "Haven",
                "tacticalDescription": "A/B/C Sites",
                "coordinates": "27°28'N, 89°38'W",
                "displayIcon": (
                    "https://media.valorant-api.com/maps/" "2bee0dc9-4ffe-519b-1cbd-7fbe763a6047/displayicon.png"
                ),
                "xMultiplier": 7.5e-05,
                "yMultiplier": -7.5e-05,
                "xScalarToAdd": 1.09345,
                "yScalarToAdd": 0.642728,
            },
        }

    def load_map_image(self) -> Image.Image:
        try:
            response = requests.get(self.selected_map["data"]["displayIcon"])
            response.raise_for_status()
            return Image.open(BytesIO(response.content))
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to load map image: {e}")

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

        plot.set_title(f"{map_data['displayName']} Map - Phase: {phase}, Round: {round_number}")
        return players

    def show_map(self):
        # TODO fix import
        """client = ValorantClient()

        selected_map = client.get_map_by_uuid(UUID(ValorantConstants.Maps[map_name]))"""
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.imshow(self.map_img, extent=[0, self.map_img.width, self.map_img.height, 0])

        players = [ax.plot([], [], "o", markersize=8, label=f"Player {i+1}")[0] for i in range(10)]

        _ = FuncAnimation(
            fig,
            self.update,
            fargs=(players, self.selected_map["data"], ax),
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
    map_name = "Haven"
    csv_file_path = "view/prueba.csv"
    map_view = ViewMap(map_name, csv_file_path)
    map_view.show_map()
