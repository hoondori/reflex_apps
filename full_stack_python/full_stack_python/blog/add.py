import reflex as rx 
from ..ui.base import base_page
from . import form


def blog_post_add_page() -> rx.Component:
    my_form = form.blog_post_add_form()
    my_child =  rx.vstack(
        rx.heading("New Blog Post", size="9"),
        rx.desktop_only(
            rx.box(my_form, width="50vw")),
        rx.tablet_only(
            rx.box(my_form, width="80vw")),
        rx.mobile_only(
            rx.box(my_form, width="95vw")),
        spacing="5",
        justify="center",
        align="center",
        min_height="95vh",
    )

    return base_page(
        my_child,
    )