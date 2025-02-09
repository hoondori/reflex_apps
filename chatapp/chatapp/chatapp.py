"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from chatapp import style
from rxconfig import config
import asyncio


class State(rx.State):
    """The app state."""
    # current question being asked
    question: str

    # keep track of chat history as a list of (question, answer)
    chat_history: list[tuple[str, str]]

    @rx.event
    async def answer(self):
        answer = "I don't know"
        
        # clear before answer is about to being streamed
        self.chat_history.append((self.question, "")) 
        self.question = ""
        yield

        for i in range(len(answer)):
            # pause to show streaming effect
            await asyncio.sleep(0.1)

            # modify last answer part in chat history
            self.chat_history[-1] = (
                self.chat_history[-1][0], # leave question untouch
                answer[: i+1],
            )
            yield

    @rx.event
    def set_question(self, question):
        self.question = question

def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=style.question_style),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=style.answer_style),
            text_align="left",
        ),
        margin_y="1em",
        width="100%"
    )

def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1])
        )
    )    

def chat_input() -> rx.Component:
    return rx.hstack(
        rx.input(value=State.question,
                 placeholder="Ask a question", 
                 on_change=State.set_question,
                 style=style.input_style),
        rx.button("Ask", 
                  on_click=State.answer,
                  style=style.button_style)
    )

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        chat(),
        chat_input(),
    )


app = rx.App()
app.add_page(index)
