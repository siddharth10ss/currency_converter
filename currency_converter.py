import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

# Static exchange rates relative to USD (fallback)
STATIC_EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.85,
    'INR': 74.0,
    'GBP': 0.75,
    'JPY': 110.0,
    'AUD': 1.35,
    'CAD': 1.25,
    'CHF': 0.92,
    'CNY': 6.45,
    'SEK': 8.6
}

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Currency Converter")
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Configure grid columns weight for proper resizing
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=3)
        root.columnconfigure(2, weight=1)

        # Title label
        title_label = ttk.Label(root, text="Currency Converter", font=("Helvetica", 16, "bold"))
        title_label.grid(column=0, row=0, columnspan=3, pady=10, sticky='NSEW')

        # Amount label and entry
        self.amount_label = ttk.Label(root, text="Amount:")
        self.amount_label.grid(column=0, row=1, padx=10, pady=5, sticky='E')
        self.amount_var = tk.StringVar()
        self.amount_entry = ttk.Entry(root, textvariable=self.amount_var, font=("Helvetica", 12))
        self.amount_entry.grid(column=1, row=1, padx=10, pady=5, sticky='W')

        # Source currency label and dropdown
        self.source_label = ttk.Label(root, text="From Currency:")
        self.source_label.grid(column=0, row=2, padx=10, pady=5, sticky='E')
        self.source_currency = tk.StringVar()
        self.source_dropdown = ttk.Combobox(root, textvariable=self.source_currency, state='readonly', font=("Helvetica", 12))
        self.source_dropdown['values'] = list(STATIC_EXCHANGE_RATES.keys())
        self.source_dropdown.current(0)
        self.source_dropdown.grid(column=1, row=2, padx=10, pady=5, sticky='W')

        # Swap button
        self.swap_button = ttk.Button(root, text="Swap", command=self.swap_currencies)
        self.swap_button.grid(column=2, row=2, padx=5, pady=5, sticky='EW')

        # Target currency label and dropdown
        self.target_label = ttk.Label(root, text="To Currency:")
        self.target_label.grid(column=0, row=3, padx=10, pady=5, sticky='E')
        self.target_currency = tk.StringVar()
        self.target_dropdown = ttk.Combobox(root, textvariable=self.target_currency, state='readonly', font=("Helvetica", 12))
        self.target_dropdown['values'] = list(STATIC_EXCHANGE_RATES.keys())
        self.target_dropdown.current(1)
        self.target_dropdown.grid(column=1, row=3, padx=10, pady=5, sticky='W')

        # Convert button
        self.convert_button = ttk.Button(root, text="Convert", command=self.convert_currency)
        self.convert_button.grid(column=0, row=4, columnspan=3, padx=10, pady=10, sticky='EW')

        # Clear button
        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_fields)
        self.clear_button.grid(column=0, row=5, columnspan=3, padx=10, pady=5, sticky='EW')

        # Refresh rates button
        self.refresh_button = ttk.Button(root, text="Refresh Rates", command=self.refresh_rates)
        self.refresh_button.grid(column=0, row=7, columnspan=3, padx=10, pady=5, sticky='EW')

        # Status label
        self.status_label = ttk.Label(root, text="Using static rates", font=("Helvetica", 10))
        self.status_label.grid(column=0, row=8, columnspan=3, padx=10, pady=5)

        # Result label
        self.result_label = ttk.Label(root, text="", font=("Helvetica", 12, "bold"))
        self.result_label.grid(column=0, row=6, columnspan=3, padx=10, pady=10, sticky='NSEW')

        # Initialize exchange rates with static rates
        self.exchange_rates = STATIC_EXCHANGE_RATES.copy()

        # Fetch real-time rates in background
        self.refresh_rates()

    def refresh_rates(self):
        """Fetch real-time exchange rates from API in a background thread."""
        def fetch():
            try:
                self.status_label.config(text="Fetching real-time rates...")
                response = requests.get("https://api.exchangerate.host/latest?base=USD", timeout=10)
                response.raise_for_status()
                data = response.json()
                rates = data.get("rates", {})
                # Filter rates to only supported currencies
                filtered_rates = {k: rates[k] for k in self.exchange_rates.keys() if k in rates}
                if filtered_rates:
                    self.exchange_rates.update(filtered_rates)
                    self.status_label.config(text="Rates updated from API")
                else:
                    self.status_label.config(text="API rates unavailable, using static rates")
            except requests.exceptions.RequestException as e:
                self.status_label.config(text=f"Network error fetching rates: {e}. Using static rates.")
            except Exception as e:
                self.status_label.config(text=f"Error fetching rates: {e}. Using static rates.")

        threading.Thread(target=fetch, daemon=True).start()

    def swap_currencies(self):
        """Swap the selected source and target currencies."""
        source = self.source_currency.get()
        target = self.target_currency.get()
        self.source_currency.set(target)
        self.target_currency.set(source)

    def clear_fields(self):
        """Clear all input fields and result label."""
        self.amount_var.set("")
        self.source_currency.set(list(self.exchange_rates.keys())[0])
        self.target_currency.set(list(self.exchange_rates.keys())[1])
        self.result_label.config(text="")

    def convert_currency(self):
        """Convert the amount from source to target currency and display the result."""
        try:
            amount = float(self.amount_var.get())
            source = self.source_currency.get()
            target = self.target_currency.get()

            if source not in self.exchange_rates or target not in self.exchange_rates:
                messagebox.showerror("Error", "Invalid currency selected.")
                return

            # Convert amount to USD first, then to target currency
            amount_in_usd = amount / self.exchange_rates[source]
            converted_amount = amount_in_usd * self.exchange_rates[target]

            self.result_label.config(text=f"{amount:.2f} {source} = {converted_amount:.2f} {target}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()
