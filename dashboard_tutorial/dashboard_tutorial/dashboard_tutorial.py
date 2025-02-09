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
        User(name="hoondori", email="hoondori@gmail.com", gender="Male"),
        User(name="rabbittv", email="rabbittv@gmail.com", gender="Female"),
        User(name="carrottv", email="carrottv@gmail.com", gender="Male"),
    ]

    users_for_graph: list[dict] = []

    def transform_data(self):
        """Transform user gender group data into a format of bar chart"""
        from collections import Counter

        gender_counts = Counter( user.gender for user in self.users)

        self.users_for_graph = [
            {
                'name': gender_name,
                'value': cnt
            }
            for gender_name, cnt in gender_counts.items()
        ]

    def add_user(self, form_data: dict):
        print("add user")
        self.users.append(User(**form_data))
        self.transform_data()


def graph():
    """visualize bar chart of gender distribution"""
    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key="value",
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
        ),
        rx.recharts.x_axis(data_key="name"),
        rx.recharts.y_axis(),
        data=State.users_for_graph,
        width="100%",
        height=250,
    )

def show_user(user: User) -> rx.Component:
    return rx.table.row(
        rx.table.cell(user.name),
        rx.table.cell(user.email),
        rx.table.cell(user.gender),
        sytle={"bg": rx.color("gray", 3)},
        align="center"
    )

def add_customer_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add User", size="4"),
            ),
        ),
        rx.dialog.content(
            rx.dialog.title("Add New User"),
            rx.dialog.description("Fill the form with the user's info"),
            rx.form(
                rx.flex(
                    rx.input(placeholder="User Name", name="name", required=True),
                    rx.input(placeholder="user@reflex.dev", name="email"),
                    rx.select(["Male", "Female"], placeholder="male", name="gender"),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Cancel"), varient="soft", color_scheme="gray"
                        ),
                        rx.dialog.close(
                            rx.button("Submit", type="submit")
                        ),
                        spacing="3",
                        justify="end"
                    ),
                    direction="column",
                    spacing="4"
                ),
                on_submit=State.add_user,
                reset_on_submit=False
            ),
            max_width="450px"
        )
    )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.vstack(
        add_customer_button(),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("이름"),
                    rx.table.column_header_cell("이메일"),
                    rx.table.column_header_cell("성별")
                )
            ),
            rx.table.body(
                rx.foreach(
                    State.users, show_user
                )
            ),
            variant="surface",
            size="3",
            width="100%"
        ),
        graph(),
        align="center",
        width="100%",
    )


app = rx.App(
    theme=rx.theme(
        radius="full", accent_color="purple"
    )
)
app.add_page(
    index,
    title="Customer Data App",
    description="A simple app to manage customer data.",
    on_load=State.transform_data,
)

