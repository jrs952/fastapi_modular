# fastapi.quickstart/service_container.py

from typing import Dict, Type, Any

class ServiceContainer:
    """
    A container for managing services.
    """

    def __init__(self):
        self.services: Dict[str, Any] = {}

    def register(self, service_name: str, service_class: Type):
        """
        Register a service with a given name and class.

        :param service_name: The name of the service.
        :param service_class: The class of the service.
        """
        self.services[service_name] = service_class()

    def get(self, service_name: str) -> Any:
        """
        Retrieve a service instance by name.

        :param service_name: The name of the service.
        :return: The service instance.
        """
        service = self.services.get(service_name)
        if service is None:
            raise ValueError(f"Service '{service_name}' not found.")
        return service
