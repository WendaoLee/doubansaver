from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit,Window
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.controls import BufferControl
from prompt_toolkit.layout.layout import Layout


if __name__ =='__main__':

    def on_text_input(Buff:Buffer):
        msg = Buff.text
        the_output_buffer.insert_text("> " +msg + "\n")
        Buff.reset()

    the_output_buffer = Buffer()
    the_output_buffer.text = "Enter 'help' for more info \n"
    the_input_buffer = Buffer(
        multiline=False,
        enable_history_search=True,
        accept_handler=on_text_input
    )

    kb = KeyBindings()

    @kb.add('c-q')
    def exit_(event):
        """
        Pressing Ctrl-Q will exit the user interface.

        Setting a return value means: quit the event loop that drives the user
        interface and return this value from the `Application.run()` call.
        """
        event.app.exit()

    container = HSplit(
        [
            Window(
                content=BufferControl(buffer=the_output_buffer,focusable=False),
                allow_scroll_beyond_bottom=True,
                wrap_lines=True
            ),
            Window(
                content=BufferControl(buffer=the_input_buffer)
            )
        ]
    )

    application = Application(layout=Layout(container),full_screen=True,key_bindings=kb)
    application.run()


