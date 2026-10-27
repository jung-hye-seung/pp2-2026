import tkinter as tk

window = tk.Tk()
window.title("Hello 정혜승")
window.geometry("300x200")

label = tk.Label(window, text="Hello GUI")
label.pack()

window.mainloop()