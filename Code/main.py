import os.path
from tkinter import *
from tkinter import filedialog
from tkinter import font as TkFont
from tkinter.ttk import Scale
from PIL import ImageTk, Image, ImageDraw, ImageFont

CANVAS_COLOR = "#9E7777"
BUTTON_COLOR = "#6F4C5B"
BACKGROUND_COLOR = "#F5E8C7"


class UI:

    def __init__(self):
        # Set up ui
        # Window Set_up
        self.main_window = Tk()
        self.main_window.title("Image Watermarking")
        self.main_window.geometry("800x700-250+40")
        self.main_window.config(bg=BACKGROUND_COLOR)
        # Canvas set_up
        self.canvas = Canvas(self.main_window, width=600, height=500)

        # Image Display
        self.image_display = self.canvas.create_image(300, 250)
        # Empty Buttons, initiated on start
        self.font = TkFont.Font(family='FreeMono', size=18, weight=TkFont.BOLD)
        self.button = Button(self.main_window)
        # Stores original image object for pasting purposes
        self.original_image = ""
        # Start program and finish window setup upon running
        self.start_app()
        self.main_window.mainloop()

    def start_app(self):

        self.canvas.grid(column=1, row=1, columnspan=2, padx=100, pady=30)
        self.button.config(command=self.obtain_image, text="Upload Image", bg=BUTTON_COLOR, height=1, width=14,
                           highlightthickness=0)
        self.button.grid(column=1, row=2, columnspan=2)
        self.button["font"] = self.font
        image = Image.open("../Images/start_image.jpg")
        self.show_image(image)

    def obtain_image(self):
        try:
            filename = filedialog.askopenfilenames(title='Select', filetypes=(("All Files", "*.*"),
                                                                              ("JPEG", "*.jpeg"),
                                                                              ("PNG", "*.png"),
                                                                              ("JPG", "*.jpg")),
                                                   defaultextension=".png")
            if filename:
                image = Image.open(filename[0]).convert("RGBA")
                self.original_image = image.copy()
                self.show_image(image)
                self.button.config(text="Apply Watermark", command=self.apply_text)
                self.text_box = Text(self.main_window, height=1, width=30, font=self.font)
                self.text_box.grid(column=1, row=3, columnspan=2)
                self.text_box.insert(INSERT, "Watermark")
                self.x_direction = Scale(self.main_window, orient=HORIZONTAL, length=500, from_=0,
                                         to=self.original_image.size[0], command=self.show_text)
                self.y_direction = Scale(self.main_window, orient=VERTICAL, length=400, from_=0,
                                         to=self.original_image.size[1], command=self.show_text)
                self.canvas.grid_configure(padx=40, pady=10)
                self.x_direction.grid(column=0, row=0, columnspan=3, pady=10)
                self.y_direction.grid(column=0, row=0, rowspan=3, padx=20)
        except IndexError:
            pass

    def show_image(self, image):

        image.thumbnail((600, 500))
        im = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.image_display, image=im)
        self.canvas.image = im

    def show_text(self, event):
        text = self.text_box.get("1.0", END)
        txt_image = Image.new("RGBA", self.original_image.size, (255, 255, 255, 0))
        x = self.x_direction.get()
        y = self.y_direction.get()
        if len(text) > 30:
            self.popup_msg()
        else:
            draw_text = ImageDraw.Draw(txt_image)
            font = ImageFont.truetype("arial.ttf", self.original_image.size[0] // 20)
            draw_text.text((x, y), text, fill=(255, 255, 255, 125), font=font)
            self.new_image = Image.alpha_composite(self.original_image, txt_image)
            self.show_image(self.new_image)

    def apply_text(self):
        save_file = filedialog.asksaveasfile(mode="w", title='Select', initialfile="watermarked_image.png",
                                             filetypes=(("All Files", "*.*"),
                                                        ("JPEG", "*.jpeg"),
                                                        ("PNG", "*.png"),
                                                        ("JPG", "*.jpg")), defaultextension=".png")
        if save_file:
            abs_path = os.path.abspath(save_file.name)
            try:
                self.new_image.save(abs_path)
            except OSError:
                save_image = self.new_image.convert("RGB")
                save_image.save(abs_path)
            self.button.config(text="Upload Image", command=self.obtain_image)
            self.text_box.destroy()
            self.x_direction.destroy()
            self.y_direction.destroy()
            self.start_app()
        else:
            return

    def popup_msg(self):
        self.popup = Tk()
        self.popup.geometry("300x250-150+90")
        self.popup.wm_title("Too Many Characters")
        self.x_direction.config(state="disabled")
        self.y_direction.config(state="disabled")
        label = Label(self.popup, text="You have exceeded the character count.\nA maximum of 30 characters is allowed.")
        label.pack(side="top", fill="x", pady=10)
        button_close = Button(self.popup, text="Okay", command=self.destroy_popup)
        button_close.pack()
        self.popup.mainloop()

    def destroy_popup(self):
        self.popup.destroy()
        self.x_direction.config(state="normal")
        self.y_direction.config(state="normal")


ui = UI()
