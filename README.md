# Recipe Finder Web App

## Description

This is a simple web application that helps users find recipes based on either a list of ingredients they have or a keyword describing a meal. It uses the Spoonacular API to fetch recipe information and displays it in an easy-to-read format.

The app is designed with a clean and cute interface, featuring a pink-yellow ombre background and the playful "Amatic SC" font for a friendly user experience.

## How It Works

1. When you open the app, you are asked to choose how you want to search for recipes:  
   - By **Ingredients** (e.g., tomato, cheese, bread)  
   - By **Keyword** (e.g., pasta, sandwich)

2. After selecting the search type, you enter the actual ingredients or keyword on the next page.

3. When you submit your input, the app sends a request to the Spoonacular API using your input to get matching recipes.

4. The app then displays the first recipe result with its title and a link to the full recipe.

## Code Overview

- **app.py**:  
  This file runs the Flask web server and handles routing between pages:  
  - `/` displays the choice page  
  - `/input` asks for user input based on their choice  
  - `/results` shows the recipe result fetched from the API  

- **functions.py**:  
  Contains the function that builds the API request URL, sends it, parses the JSON response, and returns recipe data.

- **Templates (`.html` files)**:  
  - `choose.html` - lets users pick search by ingredients or keyword  
  - `input.html` - form to input ingredients or keyword  
  - `results.html` - shows the recipe information  

## API Used

This project uses the **Spoonacular Recipe API** to find recipes. Spoonacular provides a large database of recipes and food-related information.

- API endpoint used: `https://api.spoonacular.com/recipes/complexSearch`
- The API request includes parameters such as the search query (ingredients or keyword), diet filters (optional), and API key.
- Results are returned as JSON and parsed in Python to get recipe titles and IDs.
- Recipe URLs are built using the recipe ID for linking users to full recipes.

## Setup and Running

1. Make sure you have Python and Flask installed.
2. Clone this repository.
3. Put your Spoonacular API key in `functions.py`.
4. Run the app with `python app.py`.
5. Open `http://127.0.0.1:5000` in your browser.

---

**Note:** This project is for educational purposes and uses the free tier of the Spoonacular API which has usage limits.
