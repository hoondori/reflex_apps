"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
import dataclasses

@dataclasses.dataclass
class Person:
    full_name: str
    email: str
    group: str

    def dict(self):
        _dict = self.__dict__.copy()
        return _dict    

class TableForEachState(rx.State):
    people:list[Person] = []

    sort_value: str = ""
    search_value: str = ""

    # pagination
    total_items: int 
    offset: int = 0
    limit: int = 3

    @rx.event
    def load_entries(self) -> list[Person]:
        people = [
            Person(
                full_name="Danilo Sousa",
                email="danilo@example.com",
                group="Developer",
            ),
            Person(
                full_name="Zahra Ambessa",
                email="bahra@example.com",
                group="Admin",
            ),
            Person(
                full_name="Jasper Eriks",
                email="zjasper@example.com",
                group="B-Developer",
            ),  
            Person(
                full_name="ZZZZ BBBB",
                email="ZZZZ@example.com",
                group="C-Developer",
            ),                    
            Person(
                full_name="DDD EEE",
                email="DDD@example.com",
                group="F-Developer",
            ),                                
        ]

        # apply search(or filter)
        if self.search_value != "":
            search_value = self.search_value.lower()
            people = [ p
                for p in people 
                if search_value in p.full_name.lower() or
                   search_value in p.email.lower() or
                   search_value in p.group.lower()
            ]
        
        # apply sort
        if self.sort_value != "":
            if self.sort_value == 'full_name':
                people = sorted(people, key=lambda p: p.full_name)
            elif self.sort_value == 'email':
                people = sorted(people, key=lambda p: p.email)                
            elif self.sort_value == 'group':
                people = sorted(people, key=lambda p: p.group) 
            else:
                pass               

        self.people = people

        # update total number of people for pagination
        self._get_total_items()

        # apply pagination
        self.people = self.people[self.offset:self.offset+self.limit]

    ### For sort & search
    @rx.event
    def set_sort_value(self, sort_value):
        self.sort_value = sort_value
        self.load_entries()

    @rx.event
    def set_search_value(self, search_value):
        self.search_value = search_value
        self.load_entries()

    ### For pagination
    @rx.var(cache=True)
    def page_number(self) -> int:
        return (
            (self.offset // self.limit)
            + 1
            + (1 if self.offset % self.limit else 0) 
        )

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return self.total_items // self.limit + (
            1 if self.total_items % self.limit else 0
        )

    @rx.event
    def prev_page(self):
        self.offset = max(self.offset - self.limit, 0)
        self.load_entries()

    @rx.event
    def next_page(self):
        if self.offset + self.limit < self.total_items:
            self.offset += self.limit
        self.load_entries()

    def _get_total_items(self):
        self.total_items = len(self.people)

    ### For export or download
    def _convert_to_csv(self) -> str:
        """Convert the data to CSV format"""        
        if not self.people:
            self.load_entries()

        # define header
        fieldnames = ['full_name', 'email', 'group']

        # create string buffer to hold the CSV data
        import io
        import csv
        output = io.StringIO()
        writer = csv.DictWriter(
            output, fieldnames=fieldnames
        )
        writer.writeheader()
        for p in self.people:
            writer.writerow(p.dict())

        # Get the CSV data a a string
        csv_data = output.getvalue()
        output.close()
        return csv_data
    
    @rx.event
    def download_csv_data(self):
        csv_data: str = self._convert_to_csv()
        return rx.download(
            data=csv_data,
            filename="data.csv"
        )


def show_person(person: Person):
    """Show a person in a table row."""
    return rx.table.row(
        rx.table.cell(person.full_name),
        rx.table.cell(person.email),
        rx.table.cell(person.group),
    )


def show_table() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button("Prev", on_click=TableForEachState.prev_page),
            rx.text(f"Page {TableForEachState.page_number}/{TableForEachState.total_pages}"),
            rx.button("Next", on_click=TableForEachState.next_page),
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    rx.table.column_header_cell("Full name"),
                    rx.table.column_header_cell("Email"),
                    rx.table.column_header_cell("Group"),
                ),
            ),
            rx.table.body(
                rx.foreach(
                    TableForEachState.people, show_person
                )
            ),
            on_mount=TableForEachState.load_entries,
            width="100%",
        ),
        rx.hstack(
            rx.button(
                "Download as JSON",
                on_click=rx.download(
                    data=TableForEachState.people,
                    filename="data.json",
                ),
            ),
            rx.button(
                "Download as CSV",
                on_click=TableForEachState.download_csv_data,
            ),
            spacing="7",
        ),        
        width="100%",            
    )

def index() -> rx.Component:
    return rx.vstack(
        rx.select(
            ['full_name', "email", "group"],
            placeholder="Sort By: full_name",
            on_change=lambda value: TableForEachState.set_sort_value(value)
        ),
        rx.input(
            placeholder="Search here...",
            on_change=lambda value: TableForEachState.set_search_value(value)
        ),
        show_table(),
        width="100%"
    )


app = rx.App()
app.add_page(index)
