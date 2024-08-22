import importlib_metadata

metadata = importlib_metadata.metadata("iup")

__version__ = metadata['version']
