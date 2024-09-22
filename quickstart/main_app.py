# fastapi.quickstart/main_app.py

from fastapi import FastAPI
from .config import Config
from .plugin_registration import register_plugins
from .service_registration import register_services
from .service_container import ServiceContainer
from .services.logging_service import LoggingService

app = FastAPI()
logger = LoggingService.get_logger("MainApp")

def initialize_app(custom_plugins=None, custom_services=None):
    """
    Initialize the application, optionally registering custom plugins and services.

    :param custom_plugins: A list of custom plugin modules to register.
    :param custom_services: A dictionary of custom services to register.
    """
    logger.info("Initializing application.")

    # Initialize the service container
    service_container = ServiceContainer()

    # Register core services
    core_services = register_services()
    for service_name, service_class in core_services.items():
        service_container.register(service_name, service_class)

    # Register custom services
    if custom_services:
        for service_name, service_class in custom_services.items():
            service_container.register(service_name, service_class)
            logger.info(f"Registered custom service: {service_name}")

    # Register default plugins, passing the service container
    register_plugins(app, plugin_folder_name="plugins", service_container=service_container)

    # Register custom plugins
    if custom_plugins:
        for plugin in custom_plugins:
            app.include_router(plugin.setup_routes(service_container))
            logger.info(f"Registered custom plugin: {plugin.__name__}")

# Initialize the app with default settings
initialize_app()
