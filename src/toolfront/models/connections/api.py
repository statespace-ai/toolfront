import logging

from pydantic import Field

from toolfront.models.api import API
from toolfront.models.connection import Connection
from toolfront.models.spec import Spec

logger = logging.getLogger("toolfront")


class APIConnection(Connection):
    """API connection."""

    url: str = Field(..., description="Clean API URL.")

    async def connect(self) -> API:
        from toolfront.cache import load_from_env

        # The spec should always be cached since save_connections already processed it
        spec_url = load_from_env(self.url)
        spec = Spec.from_spec_url(spec_url)
        return API(spec=spec)
