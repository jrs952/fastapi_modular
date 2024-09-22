# fastapi.quickstart/service_registration.py

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type

def register_services(service_folder_name="services") -> Dict[str, Type]:
    """
    Dynamically discover and register services found in the specified service folder.

    :param service_folder_name: The name of the folder containing services.
    :return: A dictionary mapping service names to service classes.
    """
    services_dir = Path(__file__).parent / service_folder_name
    service_registry = {}

    for module_info in pkgutil.iter_modules([str(services_dir)]):
        module_name = module_info.name
        if not module_name.startswith("__"):
            module = importlib.import_module(f".{module_name}", package=f"fastapi.quickstart.{service_folder_name}")
            if hasattr(module, "register_service"):
                service_name, service_class = module.register_service()
                service_registry[service_name] = service_class

    return service_registry
