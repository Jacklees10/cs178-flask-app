# author: Ben Jackels
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of Claude and ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

# Initialize Flask app and enable flash messaging
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flash messages

# Home page route
@app.route('/')
def home():
    return render_template('home.html')

# Add a new country to the MySQL database
@app.route('/add-country', methods=['GET', 'POST'])
def add_country():
    if request.method == 'POST':
        # Get form inputs
        name = request.form['name']
        continent = request.form['continent']
        population = request.form['population']

        # Insert new country into database
        execute_update("""
            INSERT INTO country (Name, Continent, Population)
            VALUES (%s, %s, %s)
        """, (name, continent, population))

        flash('Country added successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('add_country.html')

# Delete a country from the MySQL database
@app.route('/delete-country', methods=['GET', 'POST'])
def delete_country():
    if request.method == 'POST':
        name = request.form['name']

        # Remove country by name
        execute_update("DELETE FROM country WHERE Name = %s", (name,))

        flash('Country deleted successfully!', 'warning')
        return redirect(url_for('home'))
    else:
        return render_template('delete_country.html')
    
# Update population and life expectancy for a country
@app.route('/update-country', methods=['GET', 'POST'])
def update_country():
    if request.method == 'POST':
        name = request.form['name']
        population = request.form['population']
        lifeexpectancy = request.form['lifeexpectancy']

        # Update selected fields in database
        execute_update("""
            UPDATE country
            SET Population = %s, LifeExpectancy = %s
            WHERE Name = %s
        """, (population, lifeexpectancy, name))

        flash('Country updated successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('update_country.html')

# Display all countries sorted by population
@app.route('/display-countries')
def display_countries():
    # Query database for country data
    rows = execute_query("""
        SELECT name, continent, population, lifeexpectancy
        FROM country
        ORDER BY population DESC
    """)

    # Pass formatted data to template
    return render_template('display_countries.html', users=[
        (r['name'], r['continent'], r['population'], r['lifeexpectancy'])
        for r in rows
    ])

# Display countries along with their capital cities (JOIN query)
@app.route('/countries-with-capitals')
def countries_with_capitals():
    rows = execute_query("""
        SELECT country.Name, city.Name AS CapitalCity
        FROM country
        JOIN city ON country.Capital = city.ID
        ORDER BY country.Population DESC
    """)

    return render_template('countries_capitals.html', users=[
        (r['Name'], r['CapitalCity'])
        for r in rows
    ])

# Show all favorite countries from DynamoDB
@app.route('/favorites')
def favorites():
    items = get_favorites()  # Fetch items from DynamoDB
    return render_template('favorites.html', favorites=items)

# Add a favorite country (stored in DynamoDB)
@app.route('/add-favorite', methods=['GET', 'POST'])
def add_favorite_route():
    if request.method == 'POST':
        # Get form inputs
        name = request.form['name']
        population = request.form['population']
        language = request.form['language']

        # Store item in DynamoDB
        add_favorite(name, population, language)

        flash('Country added to favorites!', 'success')
        return redirect(url_for('favorites'))
    else:
        return render_template('add_favorite.html')

# Remove a favorite country from DynamoDB
@app.route('/delete-favorite', methods=['GET', 'POST'])
def delete_favorite_route():
    if request.method == 'POST':
        country_name = request.form['name']

        # Delete item by primary key (CountryName)
        delete_favorite(country_name)

        flash('Country removed from favorites!', 'warning')
        return redirect(url_for('favorites'))
    else:
        return render_template('delete_favorite.html')
    

# Run the Flask app (development mode)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
