# Recipedia Summary
```
Modern web application that intends to reduce food wastage by maximising the leftover ingredients in the fridge.
```
# Features
- Fridge Feature (Allows users to save all their ingredients in a virtual fridge and also delete when applicable.)
- Find Recipe( Uses Spoonacular Api to find a recipe that utilises most of the ingredients that are in the virtual fridge
               and get the recipe instructions)
               
               
# Development
```
BackEnd:
Uses Python flask for the backend of this web application  and to connect with a sqlite (RDBMS) database and connect to 
the spoonacular API to parse out recipe which has the most leftover ingredients and returns the recipe instructions also.

FrontEnd:
Uses javascipt to display alerts when facing exceptions from invalid input from the user.Furthermore ,it is also used for validation logic for the registration
page if the password doesn't match the comfirm password section to reduce runtime.For the static design , HTML and 
CSS are utilised with responsive web design principles applied such as flexbox  and grid  which are used to make the website responsive.
```
## API that is being called :
[Spoonacular API](https://spoonacular.com/food-api)



# Deployment
Please click on the image to be redirected to the yotube link of this web application
[![Recipedia Video](http://img.youtube.com/vi/RurqXAiLmqE/0.jpg)](http://www.youtube.com/watch?v=RurqXAiLmqE "Recipedia")]

Shows the 2 main functions of the Recipedia.
1. Find Recipe for leftover ingredients in fridge.
2. Store and delete ingredients in your virtual fridge for tracking purposes.

