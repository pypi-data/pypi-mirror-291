from typing import Annotated, Optional

from pydantic_settings import BaseSettings
from pydantic import Field


class KeeperLoginItemBase(BaseSettings):
    username: Annotated[str, Field(alias="login")]
    password: Annotated[str, Field(alias="password")]


class AzureAppRegistrationSecretsBase(BaseSettings):
    client_id: str
    tenant_id: str
    client_secret: str
    resource_app_id: Optional[str] = None
