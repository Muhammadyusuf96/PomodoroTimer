import tkinter as tk
from tkinter.messagebox import askyesno, showinfo


class Gui:
    def __init__(self, master):
        self.root = master
        self.lastClickX = 0
        self.lastClickY = 0
        self.last_image = 0

        self.timer_working = False

        self.root.image = tk.PhotoImage(file=self.image_name(self.last_image))
        self.label = tk.Label(self.root, image=self.root.image, bg='white')

        self.root.overrideredirect(True)
        self.root.geometry("+250+250")  # "hxw+pastga+o'ngga"
        self.root.lift()
        self.root.wm_attributes("-topmost", False)
        self.root.wm_attributes("-disabled", False)
        self.root.wm_attributes("-transparentcolor", "white")
        self.label.pack()

        self.root.bind('<Return>', self.timer)
        self.root.bind('<Control-q>', self.quit_if)
        self.root.bind('<Button-1>', self.SaveLastClickPos)
        self.root.bind('<B1-Motion>', self.Dragging)
        self.root.bind_all('<MouseWheel>', lambda event: self.on_scroll(
            'scroll',
            int(-1 * (event.delta / 120)), 'units'))  # windows only

    def timer(self, event=None):
        print(self.last_image)
        if self.last_image > 0:
            self.timer_working = True
            self.last_image -= 1
            self.check()
            self.update_image()
            # schedule next update 1 second later
            self.root.after(1000, self.timer)
        else:
            self.timer_working = False
            print("Time is up!")
            showinfo(title="PomodoroTimer", message="Time is up!")

    def SaveLastClickPos(self, event):
        self.lastClickX = event.x
        self.lastClickY = event.y

    def Dragging(self, event):
        x = event.x - self.lastClickX + self.root.winfo_x()
        y = event.y - self.lastClickY + self.root.winfo_y()
        self.root.geometry(f"+{x}+{y}")

    def on_scroll(self, *args):
        if not self.timer_working:
            self.last_image += args[1]
            self.check()
            self.update_image()
        print(args[1], "showing", self.last_image, "st/nd/rd/th image")

    def update_image(self):
        # https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
        self.root.image = tk.PhotoImage(file=self.image_name(self.last_image))
        self.label.configure(image=self.root.image)
        # self.label.image = self.root.image

    def check(self):
        if self.last_image > 59:
            self.last_image = self.last_image - 60
        elif self.last_image < 0:
            self.last_image = self.last_image + 60

    def quit_if(self, event):
        if askyesno(title='Confirmation',
                    message='Are you sure that you want to quit?'):
            self.root.destroy()

    def image_name(self, number):
        number = str(number)
        n = len(number)
        return f"images/{'0' * (4 - n) + number}.png"


if __name__ == "__main__":
    root = tk.Tk()
    gui = Gui(root)
    root.mainloop()
