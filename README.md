# Restaurant ERP

The application provides tools for restaurant management. The initial plan includes five core features pertaining to the product itself:
* Modifiable list of ingredients currently in use along with their stock levels
* Modifiable list of recipes consisting of ingredients
* Tool to mark ingredients received
* Tool to mark loss/spoilage 
* Tool to mark number of products sold

The application should also ideally have basic reporting capability so a user can see, for example, the top selling product. Additional functionality, such supplier management and shift planning could be implemented if there is sufficient time. 

There are three user roles in the application with increasing levels of access (User/Manager/Admin). Each role includes the functionality of the previous roles.

### Glossary
* A Product is one instance of a Recipe
* A Recipe is comprised of a list of Ingredients and the amount of each Ingredient used
* An Ingredient is a single item with a corresponding stock level. An ingredient can be used in one or more Recipes

### The application should have the following features:
* The user is able to log in and log out
* Users can mark received ingredients into stock
* Users can mark loss/spoilage into stock
* Users can mark number of products sold, which should automatically reduce ingredients in stock
* Managers can add or remove ingredients from the list of ingredients
* Managers can add or remove recipes from the list of recipes
* Managers can see basic analytics from the reporting tool, such as current top selling prodcut
* Admins are able to create, update and remove users
