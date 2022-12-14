import tkinter
import tkinter.messagebox
import customtkinter

import coingecko_api
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

api = coingecko_api.CoinGeckoAPI()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("WalletTracker")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.previous_price = 0
        self.update_price_frequency = 5  # seconds

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Wallet Tracker", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # Values from 1s to 10s
        self.frequency_update_menu = customtkinter.CTkOptionMenu(self.radiobutton_frame, values=["1s", "2s", "3s", "4s", "5s"], command=self.change_update_price_frequency)
        self.frequency_update_menu.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        # Default value
        self.frequency_update_menu.set("5s")


        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_1.select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.price = customtkinter.CTkLabel(self.main_frame, text="BTC Price", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.price.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.current_price = customtkinter.CTkLabel(self.main_frame, text="0.00", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.current_price.grid(row=1, column=0, padx=20, pady=20, sticky="n")
        # Get the current price of BTC using the CoinGecko API (in coingecko_api.py)
        self.update_price()

        self.frame_buy_sell = customtkinter.CTkFrame(self)
        self.frame_buy_sell.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def update_price(self):
        print("Updating price...")
        price = api.get_price("bitcoin", "usd")
        print("Price:", price)
        # Format price with thousands separator (add space every 3 digits)
        str_price = f"{price:,}".replace(",", " ") + " $"

        if price > self.previous_price:
            self.current_price.configure(text_color="green")
            self.current_price.configure(text="↑ " + str_price)
        elif price < self.previous_price:
            self.current_price.configure(text_color="red")
            self.current_price.configure(text="↓ " + str_price)
        else:
            self.current_price.configure(text_color="white")
            self.current_price.configure(text=str_price)
        self.previous_price = price
        self.after(self.update_price_frequency * 1000, self.update_price)

    def change_update_price_frequency(self, new_frequency):
        new_frequency = int(new_frequency.replace("s", ""))
        self.update_price_frequency = new_frequency

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()