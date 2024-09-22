# config.py

import yaml
import os
from pathlib import Path

class Config:
    """
    Configuration management class to load and provide configurations from config.yaml.
    """

    _config = None

    @classmethod
    def load_config(cls, config_path=None):
        """
        Load the configuration from config.yaml and apply any environment variable overrides.
        
        :param config_path: Optional path to a custom config.yaml file.
        """
        if cls._config is None:
            if config_path:
                # Use the specified config_path
                config_file = Path(config_path)
            else:
                # Look for config.yaml in the current working directory
                config_file = Path.cwd() / "config.yaml"
                if not config_file.exists():
                    # Fall back to the package's config.yaml
                    config_file = Path(__file__).parent / "config.yaml"
            
            if not config_file.exists():
                raise FileNotFoundError(f"Configuration file not found at {config_file}")
            
            with open(config_file, "r") as f:
                cls._config = yaml.safe_load(f)
            
            # Apply overrides from environment variables
            cls._override_with_env_vars()
        return cls._config

    @classmethod
    def _override_with_env_vars(cls):
        """
        Override configurations with environment variables if they are set.
        """
        services = cls._config.get("services", {})

        # Override Azure OpenAI service configuration
        azure_openai = services.get("azure_openai", {})
        azure_openai["endpoint"] = os.getenv("AZURE_OPENAI_ENDPOINT", azure_openai.get("endpoint"))
        azure_openai["api_key"] = os.getenv("AZURE_OPENAI_API_KEY", azure_openai.get("api_key"))
        azure_openai["deployment_name"] = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", azure_openai.get("deployment_name"))
        azure_openai["api_version"] = os.getenv("AZURE_OPENAI_API_VERSION", azure_openai.get("api_version"))
        services["azure_openai"] = azure_openai

        # Override ChromaDB service configuration
        chromadb = services.get("chromadb", {})
        chromadb["persist_directory"] = os.getenv("CHROMADB_PERSIST_DIRECTORY", chromadb.get("persist_directory"))
        chromadb["collection_name"] = os.getenv("CHROMADB_COLLECTION_NAME", chromadb.get("collection_name"))
        services["chromadb"] = chromadb

        # Override Neo4j service configuration
        neo4j = services.get("neo4j", {})
        neo4j["uri"] = os.getenv("NEO4J_URI", neo4j.get("uri"))
        neo4j["username"] = os.getenv("NEO4J_USERNAME", neo4j.get("username"))
        neo4j["password"] = os.getenv("NEO4J_PASSWORD", neo4j.get("password"))
        services["neo4j"] = neo4j

        cls._config["services"] = services

        # Override logging configuration
        logging_config = cls._config.get("logging", {})
        logging_config["level"] = os.getenv("LOGGING_LEVEL", logging_config.get("level"))
        logging_config["format"] = os.getenv("LOGGING_FORMAT", logging_config.get("format"))
        cls._config["logging"] = logging_config

    @classmethod
    def get_service_config(cls, service_name: str, config_path=None):
        """
        Retrieve the configuration for a specific service.

        :param service_name: The name of the service.
        :param config_path: Optional path to a custom config.yaml file.
        :return: A dictionary containing the service's configuration.
        """
        config = cls.load_config(config_path)
        services_config = config.get("services", {})
        service_config = services_config.get(service_name)
        if service_config is None:
            raise ValueError(f"Configuration for service '{service_name}' not found.")
        return service_config

    @classmethod
    def get_logging_config(cls, config_path=None):
        """
        Retrieve the logging configuration.

        :param config_path: Optional path to a custom config.yaml file.
        :return: A dictionary containing the logging configuration.
        """
        config = cls.load_config(config_path)
        logging_config = config.get("logging", {})
        return logging_config
