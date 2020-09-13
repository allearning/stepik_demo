import random

from flask import Flask, render_template

import data

MAX_CARDS_NUM = 6

app = Flask(__name__)


@app.route('/')
def render_index():
    cards_num = MAX_CARDS_NUM if len(data.tours) > MAX_CARDS_NUM else len(data.tours)
    rh = []
    rand_tours = {}
    while len(rh) < cards_num:
        candidate = random.randrange(1, len(data.tours) + 1)
        if candidate not in rh:
            rh.append(candidate)
    for i in rh:
        rand_tours[i] = data.tours[i]
    output = render_template("index.html", tours=rand_tours, departures=data.departures)
    return output


@app.route('/departures/<departure>/')
def render_departure(departure):
    dt = [tour for tour in data.tours.keys() if data.tours[tour]["departure"] == departure]
    dep_tours = {}
    for i in dt:
        dep_tours[i] = data.tours[i]
    output = render_template("departure.html", tours=dep_tours, departure=departure, departures=data.departures)
    return output


@app.route('/tours/<int:tour_id>/')
def render_tour(tour_id):
    output = render_template("tour.html", tour=data.tours[tour_id], departures=data.departures)
    return output


@app.route('/data/')
def render_data():
    output = "\n".join([f'<p>{data.tours[tour]["country"]}: <a href="/tours/{tour}/">{data.tours[tour]["title"]} {data.tours[tour]["price"]} {data.tours[tour]["stars"]}*</a></p>' for tour in data.tours])
    return output


@app.route('/data/departures/<departure>')
def render_data_departure(departure):
    output = f"<h1>Туры {data.departures[departure][0].lower() + data.departures[departure][1:]}:</h1>"
    output += "\n".join([f'<p>{data.tours[tour]["country"]}: <a href="/tours/{tour}/">{data.tours[tour]["title"]} {data.tours[tour]["price"]} {data.tours[tour]["stars"]}*</a></p>' for tour in data.tours if data.tours[tour]["departure"] == departure])
    return output


@app.route('/data/tours/<int:tour_id>/')
def render_data_tour(tour_id):
    output = (
                f"<h1>{data.tours[tour_id]['country']} {data.tours[tour_id]['title']} {data.tours[tour_id]['price']}:</h1>\n"
                f"<p>{data.tours[tour_id]['nights']} ночей</p>\n"
                f"<p>Стоимость: {data.tours[tour_id]['price']} Р</p>\n"
                f"<p>{data.tours[tour_id]['description']}</p>"
            )

    return output


if __name__ == '__main__':
    app.run()
