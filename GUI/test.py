from tkinter import *

# Create the main window
window = Tk()
window.title("My First Tkinter App")

# Add a label widget
label = Label(window, text="Hello, Tkinter!")
label.pack()


def myclick():
    mylabel = Label(window, text="You clicked the button!")
    mylabel.pack()


# Add a button widget
button = Button(window, text="Click Me", padx=50, pady=50,
                command=myclick, fg='blue', bg='green')
button.pack()

# Sizing options
# window.geometry("500x500")

# Run the main event loop
window.mainloop()