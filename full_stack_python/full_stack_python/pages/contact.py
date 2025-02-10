import reflex as rx 
import asyncio
from ..ui.base import base_page
from .. import navigation

class ContactState(rx.State):
    form_data: dict = {}

    did_submit: bool = False

    timeleft: int = 5

    @rx.var(cache=True)
    def timeleft_label(self) -> str:
        if self.timeleft < 1:
            return "Times up!!"
        return f"{self.timeleft} seconds"

    @rx.var(cache=True)
    def thank_you(self) -> str:
        first_name = self.form_data.get('first_name') or ""
        return f"Thank you {first_name.strip()}" + "!"

    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        self.did_submit = True
        yield 

        await asyncio.sleep(2)
        self.did_submit = False
        yield

    async def start_timer(self):
        while self.timeleft > 0:
            await asyncio.sleep(1)
            self.timeleft -= 1
            yield

@rx.page(
    route=navigation.routes.CONTACT_US,
    on_load=ContactState.start_timer,
)
def contact_page() -> rx.Component:
    my_form = rx.form(
        rx.vstack(
            rx.hstack(
                rx.input(
                    name="first_name",                
                    placeholder="First Name",
                    required=True,
                    width="100%"
                ),
                rx.input(
                    name="last_name",
                    placeholder="Last Name",
                    required=True,
                    width="100%"
                ),
                 width="100%"
            ),
            rx.input(
                name="email",
                type="email",
                placeholder="name@example.com",
                width="100%"
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
     
    return base_page(
        rx.vstack(
            rx.heading("Contact Us", size="9"),
            rx.text(ContactState.timeleft_label),
            rx.cond(ContactState.did_submit, ContactState.thank_you, ""),
            rx.desktop_only(
                rx.box(my_form, width="50vw")),
            rx.tablet_only(
                rx.box(my_form, width="80vw")),
            rx.mobile_only(
                rx.box(my_form, width="95vw")),
            spacing="5",
            justify="center",
            align="center",
            min_height="85vh",
        )
    )