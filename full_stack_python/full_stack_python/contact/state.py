import reflex as rx 
import asyncio
from .model import ContactEntryModel

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
        data = {}
        for k, v in form_data.items():
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

    # async def start_timer(self):
    #     while self.timeleft > 0:
    #         await asyncio.sleep(1)
    #         self.timeleft -= 1
    #         yield