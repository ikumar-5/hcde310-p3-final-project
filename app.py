## app

import re
import urllib.request
import urllib.parse
import json
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

API_KEY = "009edfd2e46b42bdbc2e967ccdd22486"

# Utility function to create URL-safe slug
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return urllib.parse.quote(text)

def get_recipes(query, query_type):
    base_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "number": 5,
        "addRecipeInformation": True,
        "apiKey": API_KEY
    }

    if query_type == "ingredients":
        params["includeIngredients"] = query
        params["fillIngredients"] = True
    elif query_type == "keyword":
        params["query"] = query

    url = base_url + "?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": "Mozilla/5.0"}

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            result = json.loads(data)
            recipes = []

            if "results" in result:
                for r in result["results"]:
                    missed = []
                    if query_type == "ingredients" and "missedIngredients" in r:
                        missed = [i["name"] for i in r["missedIngredients"]]

                    title_slug = slugify(r.get("title", ""))
                    recipe_url = f"https://spoonacular.com/recipes/{title_slug}-{r.get('id')}"

                    recipes.append({
                        "title": r.get("title"),
                        "image": r.get("image"),
                        "readyInMinutes": r.get("readyInMinutes", "N/A"),
                        "sourceUrl": recipe_url,
                        "missingIngredients": missed
                    })

            return recipes
    except Exception as e:
        print("Error fetching recipes:", e)
        return None  # indicate error

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/input', methods=['GET', 'POST'])
def input_page():
    input_type = request.args.get('type')
    if input_type not in ['ingredients', 'keyword']:
        return redirect(url_for('choose'))

    error_msg = None
    user_input = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()

        if not user_input:
            error_msg = "Please enter something."
        elif len(user_input) > 100:
            error_msg = "Input is too long, please shorten it."

        if error_msg:
            return render_template('input.html', input_type=input_type, error=error_msg, user_input=user_input)

        return redirect(url_for('results', query=user_input, qtype=input_type))

    return render_template('input.html', input_type=input_type, user_input=user_input)

@app.route('/results')
def results():
    query = request.args.get('query', '').strip()
    qtype = request.args.get('qtype', '')

    if not query or qtype not in ['ingredients', 'keyword']:
        return redirect(url_for('choose'))

    recipes = get_recipes(query, qtype)

    if recipes is None:
        error_msg = "Sorry, there was an error fetching recipes. Please try again later."
        return render_template('results.html', recipes=[], error=error_msg)

    if len(recipes) == 0:
        error_msg = "No recipes found for your input. Try again with different keywords or ingredients."
        return render_template('results.html', recipes=[], error=error_msg)

    return render_template('results.html', recipes=recipes, error=None)

if __name__ == '__main__':
    app.run(debug=True)
