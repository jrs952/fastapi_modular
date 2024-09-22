# fastapi.quickstart/plugin_registration.py

import importlib
import pkgutil
from pathlib import Path

def register_plugins(app, plugin_folder_name="plugins", service_container=None):
    """
    Dynamically register plugins found in the specified plugin folder.

    :param app: The FastAPI application instance.
    :param plugin_folder_name: The name of the folder containing plugins.
    :param service_container: The service container instance.
    """
    plugins_dir = Path(__file__).parent / plugin_folder_name

    for module_info in pkgutil.iter_modules([str(plugins_dir)]):
        module_name = module_info.name
        if not module_name.startswith("__"):
            module = importlib.import_module(f".{module_name}", package=f"fastapi.quickstart.{plugin_folder_name}")
            if hasattr(module, "setup_routes"):
                router = module.setup_routes(service_container)
                app.include_router(router)
