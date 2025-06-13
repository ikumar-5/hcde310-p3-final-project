## functions

import urllib.request
import urllib.parse
import json

API_KEY = "009edfd2e46b42bdbc2e967ccdd22486"


# Search recipes by ingredients
def get_recipes_by_ingredients(ingredient_list):
    base_url = "https://api.spoonacular.com/recipes/findByIngredients"

    query_params = {
        "ingredients": ingredient_list,
        "number": 5,
        "ranking": 1,
        "apiKey": API_KEY
    }

    url = base_url + "?" + urllib.parse.urlencode(query_params)
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            result = json.loads(data)

            recipes = []
            for item in result:
                title = item.get("title")
                recipe_id = item.get("id")
                image = item.get("image")
                missed = [i["name"] for i in item.get("missedIngredients", [])]
                link = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe_id}"

                recipes.append({
                    "title": title,
                    "id": recipe_id,
                    "image": image,
                    "missingIngredients": missed,
                    "link": link
                })

            return recipes
    except Exception as e:
        print("Error:", e)
        return []


# Search recipes by keyword (like "pasta")
def get_recipes_by_keyword(keyword):
    base_url = "https://api.spoonacular.com/recipes/complexSearch"

    query_params = {
        "query": keyword,
        "number": 5,
        "apiKey": API_KEY
    }

    url = base_url + "?" + urllib.parse.urlencode(query_params)
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            result = json.loads(data)

            recipes = []
            for item in result.get("results", []):
                title = item.get("title")
                recipe_id = item.get("id")
                image = item.get("image")
                link = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe_id}"

                recipes.append({
                    "title": title,
                    "id": recipe_id,
                    "image": image,
                    "link": link
                })

            return recipes
    except Exception as e:
        print("Error:", e)
        return []
