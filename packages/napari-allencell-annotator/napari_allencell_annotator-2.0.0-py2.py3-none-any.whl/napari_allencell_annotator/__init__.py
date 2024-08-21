try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "2.0.0"

from ._dock_widget import napari_experimental_provide_dock_widget  # noqa # pylint: disable=unused-import
