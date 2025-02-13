from typing import Optional
import reflex as rx
import reflex_local_auth
import sqlmodel
from reflex_local_auth.pages.components import input_100w, MIN_WIDTH, PADDING_TOP
from ..model import UserInfo


class MyRegisterState(reflex_local_auth.RegistrationState):
    # This event handler must be named something besides `handle_registration`!!!
    def handle_registration_email(self, form_data):
        print(self.router.session.client_ip)
        registration_result = self.handle_registration(form_data)
        if self.new_user_id >= 0:
            with rx.session() as session:
                session.add(
                    UserInfo(
                        email=form_data["email"],
                        user_id=self.new_user_id,
                    )
                )
                session.commit()
        return registration_result
    


class SessionState(reflex_local_auth.LocalAuthState):
    
    @rx.var(cache=True)
    def my_userinfo_id(self) -> str | None:
        if self.authenticated_user_info is None:
            return None
        return self.authenticated_user_info.id

    @rx.var(cache=True)
    def my_user_id(self) -> int:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.id
        
    @rx.var(cache=True)
    def authenticated_username(self) -> str | None:
        if self.authenticated_user.id < 0:
            return None
        return self.authenticated_user.username 
    
    @rx.var(cache=True)
    def authenticated_user_info(self) -> Optional[UserInfo]:
        if self.authenticated_user.id < 0:
            return None
        with rx.session() as session:
            return session.exec(
                sqlmodel.select(UserInfo).where(
                    UserInfo.user_id == self.authenticated_user.id
                ),
            ).one_or_none()    
        
    def on_load(self):
        if not self.is_authenticated:
            return reflex_local_auth.LoginState.redir
        print(self.authenticated_user_info)

    def perform_logout(self):
        self.do_logout()
        return rx.redirect("/")