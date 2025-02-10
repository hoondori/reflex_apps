import reflex as rx 
from ..ui.base import base_page

def pricing_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Pricing", size="9"),
            rx.text(
                "Something about Pricing"
            ),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        )
    )