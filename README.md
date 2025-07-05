# Currency Converter App

This is a simple Python Currency Converter application with a Tkinter GUI. It converts an amount from a source currency to a target currency using real-time exchange rates fetched from an API, with fallback to static rates.

## Features

- User-friendly GUI with input field and dropdowns for currency selection.
- Real-time exchange rates fetched from [exchangerate.host](https://exchangerate.host).
- Swap and Clear buttons for convenience.
- Manual refresh of exchange rates.
- Error handling for invalid inputs and network issues.

## Requirements

- Python 3.x
- `requests` library (install via `pip install requests`)

## Usage

1. Run the application:

   ```bash
   python currency_converter.py
   ```

2. Enter the amount, select source and target currencies.
3. Click **Convert** to see the converted amount.
4. Use **Swap** to switch currencies.
5. Use **Clear** to reset inputs.
6. Use **Refresh Rates** to update exchange rates manually.

## License

This project is open source and free to use.
