from pathlib import Path
from typing import Optional, Any

from PyQt5.QtCore import QObject
from napari.layers import Points
from qtpy.QtCore import Signal

from napari_allencell_annotator.model.key import Key


class AnnotatorModel(QObject):

    image_changed: Signal = Signal()
    image_count_changed: Signal = Signal(int)
    images_shuffled: Signal = Signal(bool)
    image_set_added: Signal = Signal()
    annotation_started_changed: Signal = Signal()
    edit_points_layer_changed: Signal = Signal(str)
    annotation_recorded: Signal = Signal()

    def __init__(self):
        super().__init__()
        # dict of annotation key names -> Key objects containing information about that key
        # such as default values, options, type
        self._annotation_keys: dict[str, Key] = {}
        # Images that have been added to annotator
        self._added_images: list[Path] = []
        # Shuffled images list. If user has not selected shuffle, this remains None
        # and is populated with a shuffled list if the user has selected shuffle
        self._shuffled_images: Optional[list[Path]] = None

        # THE FOLLOWING FIELDS ONLY ARE NEEDED WHEN ANNOTATING STARTS AND ARE INITIALIZED AFTER STARTING.
        # Current image index, which is none by default
        # Changes to curr_img_index through set_curr_img_index() emits an image_changed event which parts of the app
        # react to display that image. -1 if the user has not started annotating.
        self._curr_img_index: int = -1
        self._previous_img_index: int = -1  # index of previously viewed image, -1 by default
        # annotations that have been crated. If annotating has not started, is None by default.
        # dict of annotated image path -> list of annotations for that image
        self._created_annotations: Optional[dict[Path, list[Any]]] = None
        # path to csv where data should be saved.
        # None if annotating has not started.
        self._csv_save_path: Optional[Path] = None

        self._annotation_started = False

        # dict storing current point layers {name: PointsLayer}
        self._curr_img_points_layer: dict[str, Points] = {}

    def get_annotation_keys(self) -> dict[str, Key]:
        return self._annotation_keys

    def clear_annotation_keys(self) -> None:
        self._annotation_keys.clear()

    def set_annotation_keys(self, annotation_keys: dict[str, Key]) -> None:
        self._annotation_keys = annotation_keys

    def add_image(self, file_item: Path, idx: Optional[int] = None) -> None:
        if idx:
            self._added_images.insert(idx)
        else:
            self._added_images.append(file_item)
        self.image_count_changed.emit(self.get_num_images())

    def get_all_images(self) -> list[Path]:
        if self.is_images_shuffled():
            return self._shuffled_images
        else:
            return self._added_images

    def get_image_at(self, idx: int) -> Path:
        if self.is_images_shuffled():
            return self._shuffled_images[idx]
        else:
            return self._added_images[idx]

    def get_num_images(self) -> int:
        if self.is_images_shuffled():
            return len(self._shuffled_images)
        else:
            return len(self._added_images)

    def set_all_images(self, list_of_img: list[Path]) -> None:
        self._added_images = list_of_img
        self.image_set_added.emit()
        self.image_count_changed.emit(self.get_num_images())

    def clear_all_images(self) -> None:
        self._added_images = []
        self._created_annotations = None
        if self.is_images_shuffled():
            self.set_shuffled_images(None)
        self.image_count_changed.emit(0)

    def empty_image_list(self) -> None:
        if self.is_images_shuffled():
            self._shuffled_images = []
        else:
            self._added_images = []

    def remove_image(self, item: Path) -> None:
        self._added_images.remove(item)
        self.image_count_changed.emit(self.get_num_images())

    def set_shuffled_images(self, shuffled: Optional[list[Path]]) -> None:
        self._shuffled_images = shuffled
        if shuffled is not None:
            # we are setting the _shuffled_images field to a list of shuffled images. emit event so ui reacts
            self.images_shuffled.emit(True)
        else:
            self.images_shuffled.emit(False)

    def get_shuffled_images(self) -> list[Path]:
        return self._shuffled_images

    def is_images_shuffled(self) -> bool:
        return self._shuffled_images is not None

    def get_curr_img_index(self) -> int:
        return self._curr_img_index

    def set_curr_img_index(self, idx: int) -> None:
        self._curr_img_index = idx
        self.clear_all_cur_img_points_layers()
        self.image_changed.emit()

    def get_curr_img(self) -> Optional[Path]:
        if self.get_curr_img_index() != -1:
            if self.is_images_shuffled():
                return self._shuffled_images[self._curr_img_index]
            else:
                return self._added_images[self._curr_img_index]
        else:
            return None

    def get_annotations(self) -> dict[Path, list[Any]]:
        return self._created_annotations

    def add_annotation(self, file_path: Path, annotation: list[Any]):
        self._created_annotations[file_path] = annotation

    def set_annotations(self, annotations: dict[Path, list[Any]]) -> None:
        self._created_annotations = annotations

    def set_previous_image_index(self, idx: int) -> None:
        self._previous_img_index = idx

    def get_previous_image_index(self) -> int:
        return self._previous_img_index

    def set_csv_save_path(self, path: Path) -> None:
        self._csv_save_path = path

    def get_csv_save_path(self) -> Path:
        return self._csv_save_path

    def is_annotation_started(self) -> bool:
        return self._annotation_started

    def set_annotation_started(self, started: bool) -> None:
        self._annotation_started = started
        self.annotation_started_changed.emit()

    def get_all_curr_img_points_layers(self) -> dict[str, Points]:
        return self._curr_img_points_layer

    def clear_all_cur_img_points_layers(self) -> None:
        self._curr_img_points_layer = {}

    def add_points_layer(self, name: str, points_layer: Points):
        self._curr_img_points_layer[name] = points_layer

    def get_points_layer(self, name: str) -> Points:
        return self._curr_img_points_layer[name]

    def edit_points_layer(self, annot_name: str) -> None:
        self.edit_points_layer_changed.emit(annot_name)

    def annotation_saved(self) -> None:
        self.annotation_recorded.emit()
