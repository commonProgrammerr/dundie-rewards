from tkinter import StringVar, Tk, Label, Entry, Button

window = Tk()

"""Widgets:
- Widgets are the building blocks of a GUI application. They are the elements that make up the user interface.
- Examples of widgets include buttons, labels, text boxes, and menus.
- Widgets can be added to the main window using the pack() method.
"""
label = Label(window, text="Name:")
name = Entry(window)

user_name = StringVar()
message = Label(window, textvariable=user_name)


def button_callback():
    user_name.set("Hello, " + name.get() + "!")


button = Button(window, text="Submit", command=button_callback)
exit_button = Button(window, command=window.quit, text="Exit")


"""Geometry Management:
- Geometry management is the process of arranging widgets on the screen.
- There are several ways to manage the geometry of widgets, including pack(), grid(), and place().
- The pack() method is used to arrange widgets in a vertical or horizontal stack.
- The grid() method is used to arrange widgets in a grid layout.
- The place() method is used to position widgets at specific coordinates.
"""
label.grid(column=1, row=1)
name.grid(column=2, row=1)
message.grid(column=1, row=2)
button.grid(column=1, row=3)
exit_button.grid(column=2, row=3)
"""Event Loop:
- The event loop is the main loop of the program. It is responsible for listening and responding to events.
- An event is an action that is triggered by the user, such as clicking a button, moving the mouse, or pressing a key.
- The event loop listens for these events and calls the appropriate event handler to respond to them.
"""
window.mainloop()
