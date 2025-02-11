import reflex as rx

from . import routes

class NavState(rx.State):
    def to_home(self):
        return rx.redirect(routes.HOME)
    def to_blog(self):
        return rx.redirect(routes.BLOG)    
    def to_about(self):
        return rx.redirect(routes.ABOUT)
    def to_pricing(self):
        return rx.redirect(routes.PRICING)
    def to_contact(self):
        return rx.redirect(routes.CONTACT_US)            