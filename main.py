# main.py

import csv
import random

class Restaurant:
    def __init__(self, id_code, latt, long, cuisines, avg_cost, min_order,
                 rating, votes, reviews, cook_time):
        self.id = id_code
        self.latt = latt
        self.long = long
        self.cuisines = cuisines
        self.avg_cost = avg_cost
        self.min_order = min_order
        self.rating = rating
        self.votes = votes
        self.reviews = reviews
        self.cook_time = cook_time

    def get_summary(self):
        to_return = "ID: " + self.id + "\n"
        to_return += "Lattitude: " + str(self.latt) + "\n"
        to_return += "Longitude: " + str(self.long) + "\n"
        to_return += "Cuisines: "
        for i in range(len(self.cuisines)):
            if i < len(self.cuisines) - 1:
                to_return += self.cuisines[i] + ", "
            else:
                to_return += self.cuisines[i] + "\n"
        to_return += "Average Cost: $" + str(self.avg_cost) + "\n"
        to_return += "Minimum Order: $" + str(self.min_order) + "\n"
        to_return += "Rating: " + str(self.rating) + "\n"
        to_return += "Votes: " + str(self.votes) + "\n"
        to_return += "Reviews: " + str(self.reviews) + "\n"
        to_return += "Cook Time: " + str(self.cook_time) + " minutes"
        return(to_return)

csv_file = open('2020-Xtern-DS.csv')
reader = csv.reader(csv_file)
rows = []
for row in reader:
    rows.append(row)
csv_file.close()

restaurants = []
rows = rows[1:]
for row in rows:
    cuisines = [c.strip() for c in row[3].split(",")]

    rating = -1.0
    if row[6] != "-" and row[6] != "NEW" and row[6] != "Opening Soon":
        rating = float(row[6])

    votes = -1
    if row[7] != "-":
        votes = int(row[7])

    reviews = -1
    if row[8] != "-":
        reviews = int(row[8])

    avg_cost = -1.0
    try:
        avg_cost = float(row[4][1:])
    except ValueError:
        pass

    min_order = -1.0
    try:
        min_order = float(row[4][1:])
    except ValueError:
        pass

    cook_time = int(row[9].split()[0])
    restaurants.append(Restaurant(row[0], float(row[1]), float(row[2]), cuisines,
                                  avg_cost,  min_order, rating, votes,
                                  reviews, cook_time))




def get_random_restaurant(restaurant_data):
    return restaurant_data[random.randint(0,len(restaurant_data) - 1)]

def get_trending_score(restaurant):
    if restaurant.reviews < 10 or restaurant.rating == -1 or restaurant.votes == -1:
        return 0
    else:
        return (restaurant.rating*100) + (restaurant.votes * 0.01) + (restaurant.reviews * 0.001)

def find_trending_restaurants(restaurant_data, count):
    top_restaurants = restaurant_data[:count]
    top_scores = [get_trending_score(r) for r in top_restaurants]
    lowest_score = min(top_scores)
    for restaurant in restaurant_data:
        score = get_trending_score(restaurant)
        if score <= lowest_score:
            continue
        for i in range(len(top_restaurants)):
            if top_scores[i] < score:
                top_restaurants[i] = restaurant
                top_scores[i] = score
                break
    return top_restaurants

f = open("./out/top_10_trending.txt", "w+")
f.write("TOP 10 TRENDING RESTAURANTS: \n\n")
for r in find_trending_restaurants(restaurants, 10):
    f.write(r.get_summary() + "\n\n")
f.close()

cuisine_types = set()
for restaurant in restaurants:
    for cuisine in restaurant.cuisines:
        cuisine_types.add(cuisine)

def find_best_restaurants_by_cuisine(restaurant_data, cuisine, count):
    cuisine_stops = []
    for restaurant in restaurant_data:
        if cuisine in restaurant.cuisines:
            cuisine_stops.append(restaurant)

    to_return = find_trending_restaurants(cuisine_stops, count)
    return to_return

for c in cuisine_types:
    f = open("./out/best_restaurants_by_cuisine/" + c + ".txt", "w+")
    r_list =  find_best_restaurants_by_cuisine(restaurants, c, 5)
    f.write("Top " + str(len(r_list)) + " Restaurants for " + c +  ": \n\n")
    for r in r_list:
        f.write(r.get_summary() + "\n\n")
    f.close()

def find_restaurants_with_most_cuisines(restaurant_data):
    r_list = [restaurant_data[0]]
    cuisine_count = len(restaurant_data[0].cuisines)
    for r in restaurant_data:
        if len(r.cuisines) > cuisine_count:
            cuisine_count = len(r.cuisines)
            r_list = [r]
        elif len(r.cuisines) == cuisine_count:
            r_list.append(r)
    return r_list

f = open("./out/most_cuisines.txt", "w+")
f.write("Restaurants with the greatest number of cuisines: \n\n")
for r in find_restaurants_with_most_cuisines(restaurants):
    f.write(r.get_summary() + "\n\n")
f.close()

def find_restaurants_with_best_rating_to_avgcost_ratio(restaurant_data, count):
    top_restaurants = restaurant_data[:count]
    top_ratios = [(r.rating / r.avg_cost) for r in top_restaurants]
    lowest_ratio = min(top_ratios)
    for restaurant in restaurant_data:
        ratio = restaurant.rating / restaurant.avg_cost
        if ratio <= lowest_ratio:
            continue
        for i in range(len(top_restaurants)):
            if top_ratios[i] < ratio:
                top_restaurants[i] = restaurant
                top_ratios[i] = ratio
                break
    return top_restaurants

f = open("./out/best_ratios.txt", "w+")
f.write("Top 10 Restaurants with the Best Rating to Cost Ratio: \n\n")
for r in find_restaurants_with_best_rating_to_avgcost_ratio(restaurants, 10):
    f.write(r.get_summary() + "\n\n")
f.close()
