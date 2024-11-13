from flask import Flask, render_template, request
from mbta_helper import find_stop_near

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route('/nearby_station', methods=['POST'])
def nearby_station():
    place_name = request.form['place']
   
    station_name, accessible, coffee_shops = find_stop_near(place_name)
    accessible_message = "is wheelchair friendly" if accessible else "is not wheelchair friendly"

    if station_name == "Something went wrong, please enter a new location":
        return render_template('error.html', error_message="Something went wrong, please enter a new location")
    
    return render_template(
        'mbta_helper.html', 
        place=place_name, 
        station_name=station_name,
          accessible_message=accessible_message, 
          coffee_shops=coffee_shops
    )

if __name__ == "__main__":
    app.run(debug=True)
