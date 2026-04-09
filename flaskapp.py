# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-country', methods=['GET', 'POST'])
def add_country():
    if request.method == 'POST':
        name = request.form['name']
        continent = request.form['continent']
        population = request.form['population']
        execute_update("""
            INSERT INTO country (Name, Continent, Population)
            VALUES (%s, %s, %s)
        """, (name, continent, population))
        flash('Country added successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('add_country.html')

@app.route('/delete-country', methods=['GET', 'POST'])
def delete_country():
    if request.method == 'POST':
        name = request.form['name']
        execute_update("DELETE FROM country WHERE Name = %s", (name,))
        flash('Country deleted successfully!', 'warning')
        return redirect(url_for('home'))
    else:
        return render_template('delete_country.html')
    
@app.route('/update-country', methods=['GET', 'POST'])
def update_country():
    if request.method == 'POST':
        name = request.form['name']
        population = request.form['population']
        lifeexpectancy = request.form['lifeexpectancy']
        execute_update("""
            UPDATE country
            SET Population = %s, LifeExpectancy = %s
            WHERE Name = %s
        """, (population, lifeexpectancy, name))
        flash('Country updated successfully!', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('update_country.html')


@app.route('/display-countries')
def display_countries():
    rows = execute_query("""
        SELECT name, continent, population, lifeexpectancy
        FROM country
        ORDER BY population DESC
    """)
    return render_template('display_countries.html', users=[
        (r['name'], r['continent'], r['population'], r['lifeexpectancy'])
        for r in rows
    ])

@app.route('/countries-with-capitals')
def countries_with_capitals():
    rows = execute_query("""
        SELECT country.Name, country.Continent, country.Population, city.Name AS CapitalCity
        FROM country
        JOIN city ON country.Capital = city.ID
        ORDER BY country.Population DESC
    """)
    return render_template('display_countries.html', users=[
        (r['Name'], r['Continent'], r['Population'], r['CapitalCity'])
        for r in rows
    ])

@app.route('/favorites')
def favorites():
    items = get_favorites()
    return render_template('favorites.html', favorites=items)

@app.route('/add-favorite', methods=['GET', 'POST'])
def add_favorite_route():
    if request.method == 'POST':
        country_name = request.form['name']
        add_favorite(country_name)
        flash('Country added to favorites!', 'success')
        return redirect(url_for('favorites'))
    else:
        return render_template('add_favorite.html')

@app.route('/delete-favorite', methods=['GET', 'POST'])
def delete_favorite_route():
    if request.method == 'POST':
        country_name = request.form['name']
        delete_favorite(country_name)
        flash('Country removed from favorites!', 'warning')
        return redirect(url_for('favorites'))
    else:
        return render_template('delete_favorite.html')
    
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

# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
