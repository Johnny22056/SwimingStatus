"""Base service class for Alibaba Cloud Model Studio API clients."""
import logging
from openai import OpenAI

from src.config import ALIBABA_CLOUD_API_KEY, ALIBABA_CLOUD_BASE_URL

logger = logging.getLogger(__name__)


class ServiceInitError(Exception):
    """Raised when an API service client fails to initialize."""
    pass


class AlibabaPlatformService:
    """Base class for services using Alibaba Cloud Model Studio via OpenAI-compatible API.

    Handles client initialization, API key validation, and availability checks.
    Subclasses should set their own model_name when calling super().__init__().
    """

    def __init__(self, model_name: str):
        self.model = model_name
        self._client = None

        if not ALIBABA_CLOUD_API_KEY:
            logger.warning(
                "Alibaba Cloud API key not configured. "
                "Set ALIBABA_CLOUD_API_KEY environment variable to enable %s.",
                self.__class__.__name__
            )
            return

        try:
            self._client = OpenAI(
                api_key=ALIBABA_CLOUD_API_KEY,
                base_url=ALIBABA_CLOUD_BASE_URL
            )
            logger.info(
                "%s client initialized successfully with model '%s'.",
                self.__class__.__name__, self.model
            )
        except Exception as e:
            logger.error(
                "Failed to initialize %s client with model '%s': %s: %s",
                self.__class__.__name__, self.model, type(e).__name__, e
            )
            raise ServiceInitError(
                f"Failed to initialize {self.__class__.__name__} client: "
                f"{type(e).__name__}: {e}"
            ) from e

    @property
    def client(self):
        """The OpenAI client instance, or None if unavailable."""
        return self._client

    @client.setter
    def client(self, value):
        """Allow setting client for backward compatibility."""
        self._client = value

    @property
    def is_available(self) -> bool:
        """Whether the API client is ready for use."""
        return self._client is not None
