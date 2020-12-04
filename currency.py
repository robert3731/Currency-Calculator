import requests
import csv
from flask import Flask, render_template, request
app = Flask(__name__)
response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
currencies = []


def get_current_data():
    with open('currency.csv', 'w', newline='') as file:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for currency in data[0]['rates']:
            writer.writerow(currency)


def load_items_from_csv():
    currencies.clear()
    with open('currency.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            currencies.append(row)


def current_data(i):
    load_items_from_csv()
    for c in currencies:
        if i.upper() == c['code']:
            return float(c['bid'])


@app.route('/currency', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("submit.html")
    elif request.method == 'POST':
        get_current_data()
        currency = request.form['currency']
        amount = float(request.form['amount'].replace(',', '.'))
        new_amount = round(current_data(currency)*amount, 2)

        return render_template("submit.html", currency=currency.upper(), amount=amount, new_amount=new_amount)
