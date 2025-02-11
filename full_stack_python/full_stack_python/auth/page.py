import reflex as rx 

from reflex_local_auth.pages.login import login_form, LoginState

from ..ui.base import base_page
from .form import my_register_form
from .state import MyRegisterState

def my_login_page() -> rx.Component:
    return base_page(
        rx.center(
            rx.cond(
                LoginState.is_hydrated,  # type: ignore
                rx.card(login_form()),
            ),
            min_height="85vh"
        ),
        
    )

def my_register_page() -> rx.Component:
    return base_page(
        rx.center(
            rx.cond(
                MyRegisterState.success,
                rx.vstack(
                    rx.text("Registration successful!"),
                ),
                rx.card(my_register_form()),
            ),
            min_height="85vh",
        )
    )


