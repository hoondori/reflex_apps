import reflex as rx 
from ..ui.base import base_page
import reflex_local_auth

@reflex_local_auth.require_login
def protected_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Protected Content !!", size="9"),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        )
    )