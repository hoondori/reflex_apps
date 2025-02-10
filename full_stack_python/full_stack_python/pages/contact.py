# import reflex as rx 
# from ..ui.base import base_page
# from .. import navigation
# from .. import contact

# @rx.page(
#     route=navigation.routes.CONTACT_US,
# )
# def contact_page() -> rx.Component:
#     my_form = contact.contact_form()
#     return base_page(
#         rx.vstack(
#             rx.heading("Contact Us", size="9"),
#             rx.cond(contact.ContactState.did_submit, contact.ContactState.thank_you, ""),
#             rx.desktop_only(
#                 rx.box(my_form, width="50vw")),
#             rx.tablet_only(
#                 rx.box(my_form, width="80vw")),
#             rx.mobile_only(
#                 rx.box(my_form, width="95vw")),
#             spacing="5",
#             justify="center",
#             align="center",
#             min_height="85vh",
#         )
#     )