import tkinter
import tkinter.messagebox
import customtkinter

import coingecko_api

import pandas as pd
import datetime
from PIL import Image

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

api = coingecko_api.CoinGeckoAPI()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("WalletTracker")
        self.geometry(f"{1500}x{800}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.previous_price = 0
        self.update_price_frequency = 5  # seconds
        self.buy_amount = 0
        self.buy_sell_amount_currency = customtkinter.StringVar(value="USD")  # set initial value
        self.wallet_balance_usd_value = 0
        self.wallet_balance_btc_value = 0
        self.order_history = pd.DataFrame(columns=["Date", "Type", "Amount", "Price", "Total"])
        self.order_history_frame_row = 2

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_image = customtkinter.CTkImage(light_image=Image.open("logo.png"), dark_image=Image.open("logo.png"), size=(100, 42))
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Wallet Tracker", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.label_img = customtkinter.CTkLabel(self.sidebar_frame, image=self.logo_image, text="")
        self.label_img.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        
        # Values from 1s to 10s
        self.frequency_update_label = customtkinter.CTkLabel(self.sidebar_frame, text="Update Price Frequency:", anchor="w")
        self.frequency_update_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.frequency_update_menu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["1s", "2s", "3s", "4s", "5s"], command=self.change_update_price_frequency)
        self.frequency_update_menu.grid(row=6, column=0, pady=10, padx=20)
        # Default value
        self.frequency_update_menu.set("5s")

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))

        # create order history frame
        self.order_history_frame = customtkinter.CTkFrame(self)
        self.order_history_frame.grid(row=0, column=3, rowspan=4, padx=(20, 20), pady=(20, 0), sticky="n")
        # Add a label
        self.label_order_history = customtkinter.CTkLabel(master=self.order_history_frame, text="Order history", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.label_order_history.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")
        # Add heading of the table
        self.heading_order_history = customtkinter.CTkFrame(self.order_history_frame)
        # Use grid to place the frame
        self.heading_order_history.grid(row=1, column=0, padx=50, pady=10, sticky="ew")
        # Add infos
        self.heading_order_history_type = customtkinter.CTkLabel(master=self.heading_order_history, text="Type", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.heading_order_history_type.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.heading_order_history_amount = customtkinter.CTkLabel(master=self.heading_order_history, text="Amount", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.heading_order_history_amount.grid(row=0, column=1, padx=5, pady=10, sticky="n")
        self.heading_order_history_price = customtkinter.CTkLabel(master=self.heading_order_history, text="Price / BTC", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.heading_order_history_price.grid(row=0, column=2, padx=5, pady=10, sticky="n")
        self.heading_order_history_total = customtkinter.CTkLabel(master=self.heading_order_history, text="Total", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.heading_order_history_total.grid(row=0, column=3, padx=5, pady=10, sticky="n")
        self.heading_order_history_date = customtkinter.CTkLabel(master=self.heading_order_history, text="Date", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.heading_order_history_date.grid(row=0, column=4, padx=10, pady=10, sticky="n")
        self.heading_order_history.columnconfigure(0, weight=1)
        self.heading_order_history.columnconfigure(1, weight=2)
        self.heading_order_history.columnconfigure(2, weight=2)
        self.heading_order_history.columnconfigure(3, weight=1)
        self.heading_order_history.columnconfigure(6, weight=4)

        
        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, columnspan=2, padx=(20, 20), pady=(20, 20))
        self.main_frame.grid_columnconfigure(2, weight=1)

        self.price = customtkinter.CTkLabel(self.main_frame, text="Current BTC Price", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.price.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        self.current_price = customtkinter.CTkLabel(self.main_frame, text="0.00", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.current_price.grid(row=1, column=0, padx=20, pady=20, sticky="n")

        # Add label with wallet balance in USD and BTC at the right of the main frame
        self.wallet_balance = customtkinter.CTkLabel(self.main_frame, text="Wallet Balance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wallet_balance.grid(row=0, column=2, padx=20, pady=20, sticky="n")
        self.wallet_balance_usd = customtkinter.CTkLabel(self.main_frame, text="0.00 USD", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wallet_balance_usd.grid(row=1, column=2, padx=20, pady=20, sticky="n")
        self.wallet_balance_btc = customtkinter.CTkLabel(self.main_frame, text="0.00000000 BTC", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.wallet_balance_btc.grid(row=2, column=2, padx=20, pady=20, sticky="n")
        # Add virtual total balance in USD (sum of USD wallet balance and BTC wallet balance converted to USD)
        self.total_balance = customtkinter.CTkLabel(self.main_frame, text="Total Virtual Balance", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.total_balance.grid(row=0, column=3, padx=20, pady=20, sticky="n")
        self.total_balance_usd = customtkinter.CTkLabel(self.main_frame, text="0.00 USD", font=customtkinter.CTkFont(size=20, weight="bold"))   
        self.total_balance_usd.grid(row=1, column=3, padx=20, pady=20, sticky="n")



        self.frame_buy_sell = customtkinter.CTkFrame(self)
        self.frame_buy_sell.grid(row=1, column=1, columnspan=2, padx=(20, 20), pady=(20, 20))
        # Add a title to the frame
        self.buy_sell_title = customtkinter.CTkLabel(self.frame_buy_sell, text="Buy/Sell", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.buy_sell_title.grid(row=0, column=0, padx=0, pady=20, sticky="n")
        # Create an input field for the amount of BTC to buy
        self.buy_amount = customtkinter.CTkEntry(self.frame_buy_sell, width=140)
        self.buy_amount.grid(row=1, column=0, padx=20, pady=20, sticky="n")

        # Add CtkSegmentedButton to change from USD to BTC
        self.buy_amount_currency_btn = customtkinter.CTkSegmentedButton(self.frame_buy_sell, values=["USD", "BTC"], variable=self.buy_sell_amount_currency)
        self.buy_amount_currency_btn.grid(row=1, column=1, padx=20, pady=20, sticky="n")
        self.buy_amount_currency_btn.set("USD")
        # Add two buttons to buy and sell BTC (green and red)
        self.buy_button = customtkinter.CTkButton(self.frame_buy_sell, text="Buy BTC", command=self.buy_callback, text_color="white", fg_color="green")
        self.buy_button.grid(row=2, column=0, padx=5, pady=20, sticky="n")
        self.sell_button = customtkinter.CTkButton(self.frame_buy_sell, text="Sell BTC", command=self.sell_callback, text_color="white", fg_color="red")
        self.sell_button.grid(row=2, column=1, padx=5, pady=20, sticky="n")


        self.retrieve_wallet_balance_from_csv()
        self.retrieve_order_history_from_csv()
        self.update_wallet_balance()
        self.update_order_history_frame()
        self.update_price()


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

        self.update_wallet_balance()

        self.after(self.update_price_frequency * 1000, self.update_price)

    def change_update_price_frequency(self, new_frequency):
        new_frequency = int(new_frequency.replace("s", ""))
        self.update_price_frequency = new_frequency

    def retrieve_wallet_balance_from_csv(self):
        print("Retrieving wallet balance from balance.csv with pandas...")
        df = pd.read_csv("balance.csv")
        self.wallet_balance_usd_value = df["USD"][0]
        self.wallet_balance_btc_value = df["BTC"][0]

    def write_balance_to_csv(self):
        print("Writing wallet balance to balance.csv with pandas...")
        df = pd.DataFrame({"USD": [self.wallet_balance_usd_value], "BTC": [self.wallet_balance_btc_value]})
        df.to_csv("balance.csv", index=False)

    def update_wallet_balance(self):
        print("Updating wallet balance...")
        self.wallet_balance_usd.configure(text=f"{self.wallet_balance_usd_value:.2f}".replace(",", " ") + " $")
        self.wallet_balance_btc.configure(text=f"{self.wallet_balance_btc_value:.8f} BTC")
        self.update_virtual_balance()

    def update_virtual_balance(self):
        text = f"~ {self.wallet_balance_usd_value + self.wallet_balance_btc_value * self.previous_price:.2f}".replace(",", " ") + " $"
        self.total_balance_usd.configure(text=text)

    def retrieve_order_history_from_csv(self):
        print("Retrieving order history from order_history.csv with pandas...")
        df = pd.read_csv("order_history.csv", parse_dates=["date"])
        self.order_history = df.to_dict("records")

    def write_order_history_to_csv(self):
        print("Writing order history to order_history.csv with pandas...")
        dp = pd.DataFrame(self.order_history)
        dp.to_csv("order_history.csv", index=False)

    def update_order_history_frame(self):
        for order in self.order_history:
            self.add_order_to_order_history_frame(order)
    
    def add_order_to_order_history_frame(self, order):
        # Create a frame for the order
        order_frame = customtkinter.CTkFrame(self.order_history_frame, width=300, height=100)
        # Use grid to place the frame
        order_frame.grid(row=self.order_history_frame_row, column=0, padx=5, pady=5, sticky="n")
        # Increment row
        self.order_history_frame_row += 1
        # Add infos on columns
        order_type = customtkinter.CTkLabel(order_frame, text=order["type"], width=50, corner_radius=8, text_color="white", bg_color="green" if order["type"] == "BUY" else "red")
        order_type.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        order_amount = customtkinter.CTkLabel(order_frame, text=f"{order['amount']:.8f} BTC", text_color="white")
        order_amount.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        order_price = customtkinter.CTkLabel(order_frame, text=f"{order['price']:,}".replace(",", " ") + " $", text_color="white")
        order_price.grid(row=0, column=2, padx=5, pady=5, sticky="n")
        order_total = customtkinter.CTkLabel(order_frame, text=f"{order['total']:,}".replace(",", " ") + " $", text_color="white")
        order_total.grid(row=0, column=3, padx=5, pady=5, sticky="n")
        order_date = customtkinter.CTkLabel(order_frame, text=order["date"], text_color="white")
        order_date.grid(row=0, column=4, padx=5, pady=5, sticky="n")
        

    def add_order_to_order_history_csv(self, order):
        self.order_history.append(order)
        self.write_order_history_to_csv()

    def buy_callback(self):

        # Check if valid amount (float)
        try:
            float(self.buy_amount.get())
        except ValueError:
            print("Invalid amount")
            return 

        self.previous_price = api.get_price("bitcoin", "usd")
        amount = float(self.buy_amount.get())

        order = {}

        if self.buy_sell_amount_currency.get() == "USD":
            print(self.wallet_balance_usd_value)
            if self.wallet_balance_usd_value < amount:
                print("Not enough money in wallet")
                return
            price = self.previous_price
            total = amount / price
            self.wallet_balance_usd_value -= amount
            self.wallet_balance_btc_value += total
            order = {
                "type": "BUY",
                "amount": total,
                "price": price,
                "total": amount,
                "date": pd.to_datetime(datetime.datetime.now())
            }
            print(f"Buying {total:.8f} BTC for {amount:,}".replace(",", " ") + " $")

        elif self.buy_sell_amount_currency.get() == "BTC":
            print(amount)
            print(self.previous_price)
            usd_value = amount * self.previous_price
            # Keep only 2 decimals
            usd_value = float("{:.2f}".format(usd_value))
            if self.wallet_balance_usd_value < usd_value:
                print("Not enough money in wallet")
                return
            price = self.previous_price
            self.wallet_balance_usd_value -= usd_value
            self.wallet_balance_btc_value += amount
            order = {
                "type": "BUY",
                "amount": amount,
                "price": price,
                "total": usd_value,
                "date": pd.to_datetime(datetime.datetime.now())
            }
            print(f"Buying {amount:.8f} BTC for {usd_value:,}".replace(",", " ") + " $")

        self.update_wallet_balance()
        self.add_order_to_order_history_csv(order)
        self.write_balance_to_csv()
        self.add_order_to_order_history_frame(order)


    def sell_callback(self):
        # Check if valid amount (float)
        try:
            float(self.buy_amount.get())
        except ValueError:
            print("Invalid amount")
            return
        
        self.previous_price = api.get_price("bitcoin", "usd")
        amount = float(self.buy_amount.get())

        order = {}
        if self.buy_sell_amount_currency.get() == "USD":
            print(self.wallet_balance_btc_value)
            if self.wallet_balance_btc_value < amount / self.previous_price:
                print("Not enough money in wallet")
                return
            price = self.previous_price
            amount_btc = amount / price
            self.wallet_balance_usd_value += amount
            self.wallet_balance_btc_value -= amount_btc
            order = {
                "type": "SELL",
                "amount": amount_btc,
                "price": price,
                "total": amount,
                "date": pd.to_datetime(datetime.datetime.now())
            }
            print(f"Selling {amount / price:.8f} BTC for {amount:,}".replace(",", " ") + " $")

        elif self.buy_sell_amount_currency.get() == "BTC":
            print(self.wallet_balance_btc_value)
            if self.wallet_balance_btc_value < amount:
                print("Not enough money in wallet")
                return
            price = self.previous_price
            total = amount * price
            self.wallet_balance_usd_value += total
            self.wallet_balance_btc_value -= amount
            order = {
                "type": "SELL",
                "amount": amount,
                "price": price,
                "total": total,
                "date": pd.to_datetime(datetime.datetime.now())
            }
            print(f"Selling {amount:.8f} BTC for {total:,}".replace(",", " ") + " $")

        self.update_wallet_balance()
        self.add_order_to_order_history_csv(order)
        self.write_balance_to_csv()
        self.add_order_to_order_history_frame(order)

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