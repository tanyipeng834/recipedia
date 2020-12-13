import requests
import urllib.parse
import os

from flask import redirect, render_template, request, session,flash
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def search(ingredient):
    ingredients= (",").join(ingredient)
    try:
        api_key = os.environ.get("API_KEY")
        response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={api_key}",params={
        "ingredients":ingredients,"number":1  })


        response.raise_for_status()

    except requests.RequestException:

        return None





    try:
        quote = response.json()
        return {
            "ingredient":quote[0]["missedIngredients"],
            "unusedIngredient":quote[0]["usedIngredients"],

            "mealImage":quote[0]["image"],
            "title":quote[0]["title"],
            "id":quote[0]["id"]
        }
    except (KeyError, TypeError, ValueError,IndexError):

        return None



def instructions(id):
    try:

        response=requests.get(f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions?apiKey=5a7a54e11156421fbce85fbc14cb3f33")
        response.raise_for_status()

    except requests.RequestException:

        return None
    try:
        quote=response.json()
        return(quote[0]["steps"])
    except (KeyError, TypeError, ValueError,IndexError):

        return None








