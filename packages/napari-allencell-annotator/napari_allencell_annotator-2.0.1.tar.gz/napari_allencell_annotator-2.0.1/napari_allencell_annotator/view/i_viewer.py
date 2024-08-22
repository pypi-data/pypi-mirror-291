from abc import ABC, abstractmethod
from enum import Enum

import numpy as np
from napari.layers import Layer, Points
from typing import List, Tuple


class PointsLayerMode(Enum):
    """
    Mode for view.

    ADD is used to add points.
    SELECT is used to move, edit, or delete points.
    PAN_ZOOM is the default mode and allows normal interactivity with the canvas.
    """

    ADD = "add"
    SELECT = "select"
    PAN_ZOOM = "pan_zoom"


class IViewer(ABC):
    def __init__(self):
        """Base abstract class for the viewer"""
        super().__init__()

    @abstractmethod
    def add_image(self, image: np.ndarray) -> None:
        pass

    @abstractmethod
    def clear_layers(self) -> None:
        pass

    @abstractmethod
    def alert(self, alert_msg: str) -> None:
        pass

    @abstractmethod
    def get_layers(self) -> List[Layer]:
        pass

    @abstractmethod
    def get_all_points_layers(self) -> List[Points]:
        pass

    @abstractmethod
    def create_points_layer(self, name: str, visible: bool, data: np.ndarray = None) -> Points:
        pass

    @abstractmethod
    def set_points_layer_mode(self, points_layer: Points, mode: PointsLayerMode) -> None:
        pass

    @abstractmethod
    def get_points_layer_mode(self, points_layer: Points) -> str:
        pass

    @abstractmethod
    def get_selected_points(self, point_layer: Points) -> List[Tuple]:
        pass

    @abstractmethod
    def get_all_point_annotations(self) -> dict[str, list[tuple]]:
        pass

    @abstractmethod
    def toggle_points_layer(self, annot_points_layer: Points) -> None:
        pass

    @abstractmethod
    def set_all_points_layer_to_pan_zoom(self) -> None:
        pass
