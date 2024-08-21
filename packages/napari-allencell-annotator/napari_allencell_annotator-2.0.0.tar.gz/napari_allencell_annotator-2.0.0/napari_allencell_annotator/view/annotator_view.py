from enum import Enum
from typing import Dict, List, Any

from qtpy.QtWidgets import QFrame
from qtpy import QtCore
from qtpy.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLabel,
    QGridLayout,
    QScrollArea,
    QPushButton,
    QVBoxLayout,
)
from napari import Viewer

from napari_allencell_annotator.model.annotation_model import AnnotatorModel
from napari_allencell_annotator.model.key import Key
from napari_allencell_annotator.widgets.file_input import (
    FileInput,
    FileInputMode,
)
from napari_allencell_annotator.widgets.template_list import TemplateList
from napari_allencell_annotator._style import Style


class AnnotatorViewMode(Enum):
    """
    Mode for view.

    ADD is used when there is not an annotation set selected
    VIEW is used when an annotation set has been made/selected, but annotating has not started.
    ANNOTATE is used when the image set is finalized and annotating has started.
    """

    ADD = "add"
    VIEW = "view"
    ANNOTATE = "annotate"


class AnnotatorView(QFrame):
    """
    A class used to create a view for annotations.

    Inputs
    ----------
    viewer : napari.Viewer
        a napari viewer where the plugin will be used
    mode : AnnotatorViewMode
        a mode for the view

    Methods
    -------
    mode() -> AnnotatorViewMode

    set_mode(mode: AnnotatorViewMode)

    set_num_images(num: int)
        Sets the total images to be annotated.

    set_curr_index(num: int)
        Sets the index of the currently selected image.

    reset_annotations()
        Resets annotation data to empty.

    render_default_values()
        Sets annotation widget values to default.

    render_values(vals: List):
        Sets the values of the annotation widgets to vals.

    get_curr_annots() -> List
        Returns the current annotation values in a list form.

    render_annotations(data : Dict[str,Dict]))
        Renders GUI elements from the dictionary of annotations.
    """

    def __init__(
        self,
        model: AnnotatorModel,
        viewer: Viewer,
        mode: AnnotatorViewMode = AnnotatorViewMode.ADD,
    ):
        super().__init__()
        self._annotator_model = model
        self._annotator_model.image_changed.connect(self._handle_image_changed)
        self._mode = mode
        label = QLabel("Annotations")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.setStyleSheet(Style.get_stylesheet("main.qss"))
        self.annot_list = TemplateList()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.annot_list)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        # self.scroll.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scroll.setStyleSheet(
            """QScrollBar:vertical {
            width:10px;    
            margin: 0px 0px 0px 0px;
        }"""
        )
        style = """QScrollBar::handle:vertical {border: 0px solid red; border-radius: 
        2px;} """
        self.scroll.setStyleSheet(self.scroll.styleSheet() + style)

        self.layout.addWidget(self.scroll)

        self.curr_index: int = None

        # Add widget visible in ADD mode
        self.add_widget = QWidget()
        add_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create Template")
        self.create_btn.setEnabled(True)
        self.import_btn = QPushButton("Import Template (.csv or .json)")
        self.import_btn.setEnabled(True)
        self.annot_input = FileInput(mode=FileInputMode.JSONCSV, placeholder_text="Start Annotating")
        self.annot_input.toggle(False)

        add_layout.addWidget(self.create_btn, stretch=2)
        add_layout.addWidget(self.import_btn, stretch=2)
        self.add_widget.setLayout(add_layout)
        self.layout.addWidget(self.add_widget)

        # view widget visible in VIEW mode
        self.view_widget = QWidget()
        view_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.setToolTip("Edit annotation Template")
        self.cancel_btn = QPushButton("Clear")
        self.cancel_btn.setToolTip("Clear annotation template")
        self.cancel_btn.clicked.connect(self._reset_annotations)
        self.start_btn = QPushButton("Start")
        self.start_btn.setToolTip("Start Annotating Images")
        self.csv_input = FileInput(mode=FileInputMode.CSV)
        self.csv_input.toggle(False)
        self.save_json_btn = FileInput(mode=FileInputMode.JSON, placeholder_text="Save")
        self.save_json_btn.toggle(True)
        self.save_json_btn.setToolTip("Save annotation template \n to JSON file")
        self.start_btn.setEnabled(True)
        self.edit_btn.setEnabled(False)
        view_layout.addWidget(self.cancel_btn, stretch=1)
        view_layout.addWidget(self.edit_btn, stretch=1)
        view_layout.addWidget(self.save_json_btn, stretch=1)
        view_layout.addWidget(self.start_btn, stretch=1)
        self.view_widget.setLayout(view_layout)

        # annot widget visible in ANNOTATE mode
        self.annot_widget = QWidget()
        annot_layout = QGridLayout()
        self.save_btn = QPushButton("Save")
        self.exit_btn = QPushButton("Exit")

        self.prev_btn = QPushButton("< Previous")
        self.next_btn = QPushButton("Next >")
        self.next_btn.setEnabled(True)
        self.progress_bar = QLabel()
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        annot_layout.addWidget(self.progress_bar, 0, 1, 1, 2)
        annot_layout.addWidget(self.save_btn, 1, 1, 1, 1)
        annot_layout.addWidget(self.exit_btn, 1, 0, 1, 1)
        annot_layout.addWidget(self.prev_btn, 1, 2, 1, 1)
        annot_layout.addWidget(self.next_btn, 1, 3, 1, 1)
        self.annot_widget.setLayout(annot_layout)

        self._display_mode()

        self.annots_order: List[str] = []
        self.setLayout(self.layout)
        self.viewer: Viewer = viewer

    @property
    def mode(self) -> AnnotatorViewMode:
        return self._mode

    def set_mode(self, mode: AnnotatorViewMode):
        """
        Set current mode.

        Parameters
        ----------
        mode: AnnotatorViewMode
        """
        self._mode = mode
        self._display_mode()

    def _handle_image_changed(self):
        if self._annotator_model.get_curr_img_index() == -1:
            self.render_default_values()

    def display_current_progress(self):
        """
        display current progres.
        """
        self.progress_bar.setText(
            "{} of {} Images".format(
                self._annotator_model.get_curr_img_index() + 1, self._annotator_model.get_num_images()
            )
        )

    def _reset_annotations(self):
        """Reset annotation data to empty."""
        self.annot_list.clear_all()

        self.annots_order: List[str] = []
        self.scroll.setMaximumHeight(600)

    def render_default_values(self):
        """Set annotation widget values to default."""
        # for curr index if annots exist fill else fill with default
        for item in self.annot_list.items:
            item.set_default_value()

        # TODO why do we need this?
        # self.annot_list.setCurrentItem(self.annot_list.items[0])

    def render_values(self, vals: list[Any]):
        """
        Set the values of the annotation widgets.

        Parameters
        ----------
        vals:List[str]
            the values for the annotations.
        """
        for item, annotation in zip(self.annot_list.items, vals):
            item_data = annotation
            if item_data is None or item_data == "":
                item.set_default_value()
            else:
                item.set_value(item_data)
        # self.annot_list.setCurrentItem(self.annot_list.items[0])

    def get_curr_annots(self) -> List[Any]:
        """
        Return the current annotation values in a list.

        Returns
        ----------
        List
            a list of annotation values.
        """
        annots = []
        for i in self.annot_list.items:
            annots.append(i.get_value())
        return annots

    def _display_mode(self):
        """Render GUI buttons visible depending on the mode."""
        item = self.layout.itemAt(self.layout.count() - 1)
        item.widget().hide()
        self.layout.removeItem(item)
        if self._mode == AnnotatorViewMode.ADD:
            self.add_widget.show()
            self.layout.addWidget(self.add_widget)
        elif self._mode == AnnotatorViewMode.VIEW:
            self.save_json_btn.setEnabled(True)
            self.view_widget.show()
            self.layout.addWidget(self.view_widget)
        elif self._mode == AnnotatorViewMode.ANNOTATE:
            self.annot_widget.show()
            self.layout.addWidget(self.annot_widget)
            self.prev_btn.setEnabled(False)

    def render_annotations(self, data: Dict[str, Key]):
        """
        Read annotation dictionary into individual annotations.

        Parameters
        ----------
        data : Dict[str, Dict[str, Any]]
            The dictionary of annotation names -> a dictionary of types, defaults, and options.
        """
        self.annot_list.clear_all()
        self.annots_order.clear()
        for name, key_info in data.items():
            self._create_annot(name, key_info)
        self.scroll.setMaximumHeight(self.annot_list.height)

    def _create_annot(self, name: str, key: Key):
        """
        Create annotation widgets from dictionary entries.

        Parameters
        ----------
        name : str
            annotation name.
        dct : Dict[str, Any]
            annotation type, default, and options.
        """
        self.annots_order.append(name)
        self.annot_list.add_item(name, key)
