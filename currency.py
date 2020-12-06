import requests
import csv
from flask import Flask, render_template, request
app = Flask(__name__)


class CurrencyData:
    def __init__(self):
        self.currencies = []

    def load_items_from_csv(self):
        self.currencies.clear()
        with open('currency.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                self.currencies.append(row)

    def current_data(self, currency):
        self.load_items_from_csv()
        for c in self.currencies:
            if currency.upper() == c['code']:
                return float(c['bid'])


def get_current_data():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()
    with open('currency.csv', 'w', newline='') as file:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for currency in data[0]['rates']:
            writer.writerow(currency)


@app.route('/currency', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("submit.html")
    elif request.method == 'POST':
        get_current_data()
        currency_data = CurrencyData()
        currency = request.form['currency']
        amount = float(request.form['amount'].replace(',', '.'))
        currency_value = currency_data.current_data(currency)
        new_amount = round(currency_value*amount, 2)

        return render_template("submit.html", currency=currency.upper(), amount=amount, new_amount=new_amount)


if __name__ == "__main__":
    app.run(debug=False)
