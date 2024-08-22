import napari_allencell_annotator

from pathlib import Path


class Directories:
    """
    Provides safe paths to common module directories
    """

    _module_base_dir = Path(napari_allencell_annotator.__file__).parent

    @classmethod
    def get_test_assets_dir(cls) -> Path:
        """
        Path to the assets directory
        """
        return cls._module_base_dir / "_tests/assets"

    @classmethod
    def get_style_dir(cls) -> Path:
        """
        Path to the stylesheet directory
        """
        return cls._module_base_dir / "styles"
