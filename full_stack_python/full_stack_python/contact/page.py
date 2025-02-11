import reflex as rx 
from ..ui.base import base_page
from .. import contact
from ..contact.model import ContactEntryModel

def contact_entry(entry: ContactEntryModel) -> rx.Component:
    return rx.vstack(
        rx.heading(entry.first_name, size="3"),
        rx.text(entry.message),
        padding="1em",
    )

def contact_entry_list_page() -> rx.Component:
    return base_page(
        rx.vstack(
            rx.heading("Contact Entries", size="7"),
            rx.foreach(contact.ContactState.entries, contact_entry),
            spacing="5",
            align="center",
            min_height="85vh",
        )
    )

def contact_page() -> rx.Component:
    my_form = contact.contact_form()
    return base_page(
        rx.vstack(
            rx.heading("Contact Us", size="9"),
            rx.cond(contact.ContactState.did_submit, contact.ContactState.thank_you, ""),
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