import reflex as rx 
from ..ui.base import base_page
from .form import blog_post_edit_form
from .state import BlogEditFormState

def blog_post_edit_page() -> rx.Component:
    my_form = blog_post_edit_form()
    my_child =  rx.vstack(
        rx.heading(f"Edit {BlogEditFormState.post.title}", size="9"),
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