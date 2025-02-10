import reflex as rx 
from ..ui.base import base_page

def about_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("About Us", size="9"),
            rx.text(
                "Something about us"
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        )
    )