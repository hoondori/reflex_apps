import reflex as rx 
from sqlmodel import Field
import sqlalchemy
from datetime import datetime
from ..utils import timing

class ContactEntryModel(rx.Model, table=True):
    first_name: str
    last_name: str | None = None
    email: str = Field(nullable=True)
    message: str 
    created_at: datetime = Field(
        default_factory=timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )