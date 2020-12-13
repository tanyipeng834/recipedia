from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required,search,instructions




# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///users.db")

# Make sure API key is set

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        username=request.form.get("uname")
        password=request.form.get("psw")
        rows = db.execute("SELECT * FROM users1 WHERE username = :username",
                          username=username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("Wrong Credentials")
            return render_template("login.html")

        else:
             session["user_id"] = rows[0]["id"]
             return redirect("/")




@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        username=request.form.get("uname")
        password=request.form.get("psw")

        hash=generate_password_hash(password)
        users=db.execute("SELECT * FROM users1 WHERE username=:id",id=username)
        if len(users)==0:
            db.execute("INSERT INTO users1 (username, hash) VALUES(:username, :hash)",
                                 username=username,
                                 hash=hash)
            return redirect("/login")
        else:
            flash("Username is Taken")

            return render_template("register.html")






@app.route("/",methods=['POST','GET'])
@login_required
def addIngredient():
    if request.method=="GET":
        return render_template("addIngredient.html")


    else:
        ingredient=request.form.get("Ingredient")
        quanity=request.form.get("Quanity")
        db.execute("INSERT INTO ingredient1 (users_id,ingredient,quanity) VALUES (:user_id,:ingredient,:quanity)",user_id=session["user_id"],ingredient=ingredient,
        quanity=quanity)

        return redirect("/fridge")
@app.route("/fridge",methods=['POST','GET'])
@login_required
def fridge():
    if request.method=="GET":
        ingredient=db.execute("SELECT * FROM ingredient1 WHERE users_id=:id",id=session["user_id"])
        entry=len(ingredient)


        return render_template("fridge.html",ingredient=ingredient,entry=entry)

    else:
        food=request.form.get("delete_food")
        db.execute("DELETE FROM ingredient1 WHERE id=:id",id=food)
        return redirect("/fridge")


@app.route("/findRecipe")
@login_required
def findRecipe():

    ingredients=db.execute("SELECT ingredient FROM ingredient1 WHERE users_id=:id",id=session["user_id"])
    allIngredients=[]
    for ingredient in ingredients:
        allIngredients.append(ingredient["ingredient"])
    try:
        food=search(allIngredients)

        mealImage=food["mealImage"]
        session["title"]=food["title"]
        session["recipeId"]=food["id"]
        return render_template("findRecipe.html",food=food,mealImage=mealImage,title=session["title"])
    except(KeyError, TypeError, ValueError,IndexError):
        flash("Invalid Ingredient")
        return render_template("fridge.html")

@app.route("/recipe")
@login_required
def recipe():

    instruction=instructions(session["recipeId"])
    return render_template("recipe.html",instruction=instruction,title=session["title"])











@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
