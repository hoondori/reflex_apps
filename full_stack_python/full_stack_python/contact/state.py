from typing import List
import reflex as rx 
import asyncio
from .. model import ContactEntryModel
from ..auth.state import SessionState
from sqlmodel import select

class ContactState(SessionState):
    form_data: dict = {}
    entries: List['ContactEntryModel'] = []
    did_submit: bool = False

    @rx.var(cache=True)
    def thank_you(self) -> str:
        first_name = self.form_data.get('first_name') or ""
        return f"Thank you {first_name.strip()}" + "!"

    async def handle_submit(self, form_data: dict):
        data = form_data.copy()
        # add userinfo if loggined
        if self.my_userinfo_id is not None:
            data['userinfo_id'] = self.my_userinfo_id
        for k, v in data.items():
            if v == "" or v is None:
                continue
            data[k] = v

        with rx.session() as session:
            db_entry = ContactEntryModel(
                **data
            )
            session.add(db_entry)
            session.commit()
            self.did_submit = True
            yield 

        await asyncio.sleep(2)
        self.did_submit = False
        yield

    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(
                select(ContactEntryModel)
            ).all()
            self.entries = entries
        print(self.entries)
