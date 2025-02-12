import reflex as rx 
from reflex.style import toggle_color_mode

from .. import navigation
from ..auth.state import SessionState

def sidebar_user_item() -> rx.Component:
    user_info_obj = SessionState.authenticated_user_info
    username_via_user_obj = rx.cond(
        SessionState.authenticated_username, 
        SessionState.authenticated_username,
        "Unknown Account",
        )
    return rx.cond(
        user_info_obj,
        rx.hstack(
            rx.icon_button(
                rx.icon("user"),
                size="3",
                radius="full",
            ),
            rx.vstack(
                rx.box(
                    rx.text(
                        username_via_user_obj,
                        size="3",
                        weight="bold",
                    ),
                    rx.text(
                        user_info_obj.email,
                        size="2",
                        weight="medium",
                    ),
                    width="100%",
                ),
                spacing="0",
                align="start",
                justify="start",
                width="100%",
            ),
            padding_x="0.5rem",
            align="center",
            justify="start",
            width="100%",
        ),
        rx.fragment(""),
    )

def sidebar_logout_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("log-out"),
            rx.text("Log out", size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer", 
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
                "color": rx.color("accent", 11),
            },
        ),
        on_click=SessionState.perform_logout,
        as_="button",
        underline="none",
        weight="medium",
        width="100%",
    )

def sidebar_dark_mode_item() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.color_mode_cond(
                light=rx.icon("moon"),
                dark=rx.icon("sun"),
            ),
            rx.text(
                rx.color_mode_cond(
                    light="Turn dark mode on",
                    dark="Turn light mode on",
                ),
                size="4",
            ),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "cursor": "pointer", 
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
                "color": rx.color("accent", 11),
            },
        ),
        on_click=toggle_color_mode,
        as_="button",
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_item(
    text: str, icon: str, href: str
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4"),
            width="100%",
            padding_x="0.5rem",
            padding_y="0.75rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("accent", 4),
                    "color": rx.color("accent", 11),
                },
                "border-radius": "0.5em",
            },
        ),
        href=href,
        underline="none",
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        sidebar_item("Dashboard", "layout-dashboard", navigation.routes.HOME),
        sidebar_item("Blog", "square-library", navigation.routes.BLOG),
        sidebar_item("Create Post", "square-pen", navigation.routes.BLOG_ADD),
        sidebar_item("Contact", "mail", navigation.routes.CONTACT_US),
        sidebar_item("Contact History", "mailbox", navigation.routes.CONTACT_ENTRIES),        
        spacing="1",
        width="100%",
    )


def sidebar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Reflex", size="7", weight="bold"
                    ),
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        sidebar_dark_mode_item(),
                        sidebar_logout_item(),
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    sidebar_user_item(),
                    width="100%",
                    spacing="5",
                ),
                spacing="5",
                # position="fixed",
                # left="0px",
                # top="0px",
                # z_index="5",
                padding_x="1em",
                padding_y="1.5em",
                bg=rx.color("accent", 3),
                align="start",
                # height="100%",
                # height="650px",
                height="100vh",
                width="16em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.icon("align-justify", size=30)
                ),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(
                                    rx.icon("x", size=30)
                                ),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    sidebar_dark_mode_item(),
                                    sidebar_logout_item(),
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                sidebar_user_item(),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg=rx.color("accent", 2),
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )
    