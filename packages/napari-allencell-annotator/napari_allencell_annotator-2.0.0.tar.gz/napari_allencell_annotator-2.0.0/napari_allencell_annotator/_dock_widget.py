from napari_plugin_engine import napari_hook_implementation
from napari_allencell_annotator.view.main_view import MainView


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    # you can return either a single widget, or a sequence of widgets
    return [(MainView, {"name": "Annotator"})]
