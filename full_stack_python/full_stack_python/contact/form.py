import reflex as rx
from .state import ContactState
from ..auth.state import SessionState

def contact_form() -> rx.Component:

    return rx.form(
        rx.vstack(
            rx.hstack(
                rx.cond(
                    SessionState.authenticated_username,
                    rx.input(
                        name="first_name",                
                        placeholder="First Name",
                        required=True,
                        width="100%",
                        value=SessionState.authenticated_username,
                        is_disabled=True,
                        style={"color": "gray", "background-color": "#e0e0e0", "cursor": "not-allowed"}
                    ),
                    rx.input(
                        name="first_name",                
                        placeholder="First Name",
                        required=True,
                        width="100%"
                    )                        
                ),
                rx.input(
                    name="last_name",
                    placeholder="Last Name",
                    width="100%"
                ),
                 width="100%"
            ),
            rx.cond(
                SessionState.authenticated_user_info,
                rx.input(
                    name="email",
                    type="email",
                    placeholder="name@example.com",
                    width="100%",
                    value=SessionState.authenticated_user_info.email,
                    is_disabled=True,
                    style={"color": "gray", "background-color": "#e0e0e0", "cursor": "not-allowed"}
                ),
                rx.input(
                    name="email",
                    type="email",
                    placeholder="name@example.com",
                    width="100%"
                ),                                
            ),
            rx.text_area(
                name="message",
                placeholder="Your message",
                required=True,
                width="100%"
            ),
            rx.button("Submit", type="submit"),
        ),
        on_submit=ContactState.handle_submit,
        reset_on_submit=True,
    )
         