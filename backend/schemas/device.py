from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class DeviceResponse(BaseModel):
    device_id: UUID

    device_name: str

    device_type: str

    device_os: str

    last_active: datetime

    is_current: bool

    created_at: datetime

    class Config:
        from_attributes = True


class DeviceListResponse(BaseModel):
    devices: list[DeviceResponse]