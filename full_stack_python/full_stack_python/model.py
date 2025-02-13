from typing import Optional, List
import reflex as rx 
from sqlmodel import Field, Relationship
import sqlalchemy
from datetime import datetime
from .utils import timing
from reflex_local_auth import LocalUser

class UserInfo(rx.Model, table=True):
    # to localuser
    user_id: int = Field(foreign_key='localuser.id')
    user: LocalUser | None = Relationship() # local user instance

    # to blog post
    posts: List['BlogPostModel'] = Relationship(
        back_populates='userinfo'
    )

    # to contact
    contact_entries: List['ContactEntryModel'] = Relationship(
        back_populates='userinfo'
    )

    email: str
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


class BlogPostModel(rx.Model, table=True):
    # user
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="posts")

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

class ContactEntryModel(rx.Model, table=True):
    # id: int -> primary key
    user_id: int | None = None
    userinfo_id: int = Field(default=None, foreign_key="userinfo.id")
    userinfo: Optional['UserInfo'] = Relationship(back_populates="contact_entries")

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