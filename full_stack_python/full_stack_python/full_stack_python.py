import reflex as rx
from rxconfig import config
from . import pages
from .ui.base import base_page
from .navigation import routes


class State(rx.State):
    """The app state."""
    label = "this is my label"
   
    def handle_title_changed(self, value):
        self.label = value


def index() -> rx.Component:
    # Welcome Page (Index)
    return base_page(
        rx.vstack(
            rx.heading(State.label, size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.input(default_value=State.label,
                on_change=State.handle_title_changed),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            text_align="center",
        ),
    )


app = rx.App()
app.add_page(index)
app.add_page(pages.about_page, route=routes.ABOUT)
app.add_page(pages.pricing_page, route=routes.PRICING)