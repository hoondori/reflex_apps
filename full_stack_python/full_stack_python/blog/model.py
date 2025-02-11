import reflex as rx 
from sqlmodel import Field
import sqlalchemy
from datetime import datetime
from ..utils import timing

class BlogPostModel(rx.Model, table=True):
    # user
    title: str
    content: str
    created_at: datetime = Field(
        default_factory=timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            'onupdate': sqlalchemy.func.now(),
            'server_default': sqlalchemy.func.now()
        },
        nullable=False
    )    
    publish_active: bool = False
    publish_date: datetime = Field(
        default=None,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={},
        nullable=True
    )
    # publish_time