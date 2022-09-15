from re import I
from app import App

window = App()
window.read_file()
window.flip_timer = window.after(3000, window.flip_card)
window.next_word()

window.mainloop()