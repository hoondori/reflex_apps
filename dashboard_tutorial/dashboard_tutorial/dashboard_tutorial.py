"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class User(rx.Base):
    """ User Model """
    name: str
    email: str
    gender: str

class State(rx.State):
    users: list[User] = [
        User(name="hoondori", email="hoondori@gmail.com"),
        User(name="carrottv", email="carrottv@gmail.com"),
    ]

def show_user(user: User) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
        sytle={"bg": rx.color("gray", 3)},
        align="center"
    )

def add_customer_button() -> rx.Component:
    return rx.button(
        rx.icon("plus", size=26),
        rx.text("Add User", size="4"),
    ),
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.vstack(
        add_customer_button(),
        rx.table.root(
            rx.table.header(

            ),
            rx.table.body(

            ),
            variant="surface",
            size="3",
            width="100%"
        ),
        align="center",
        width="100%",
    )


app = rx.App()
app.add_page(index)

