# Restaurant ERP

A REST API backend for an application that provides tools for restaurant management. The initial plan includes five core features pertaining to the product itself:
* Modifiable list of ingredients currently in use along with their stock levels
* Modifiable list products
* Modfiable list of product versions, consisting of ingredients
* Tool to mark ingredients received
* Tool to mark number of products sold

The application should also ideally have basic reporting capability so a user can see, for example, the top selling product. Additional functionality, such supplier management and shift planning could be implemented if there is sufficient time. 

There are two user roles in the application with increasing levels of access (User/Manager). Manager role includes functionality of the user role.

### Glossary
* A Product is a friendly name for a product being sold
* A Product version is comprised of a list of Ingredients and the amount of each Ingredient used
* An Ingredient is a single item with a corresponding stock level. An ingredient can be used in one or more Product versions
* A purchase is an event where multiple products may be ordered
* A product sale is the amount of a given product sold in one purchase
* A Replenishment is a list of received ingredients

### The application has the following features:
* Can create a user
* User is able to log in and log out
* Users can mark received replenishments, automatically updating ingredients in stock
* Users can mark purchases, automatically reducing ingredients in stock
* Managers can add ingredients
* Managers can create products
* Managers can create versions of products
* Managers can query product sales by purchase
* Managers can query product versions by version number
* Manager can query all of the relevant resources as is to be expected from a REST API

### Installation and setup
1. Clone the git repository
``` 
git clone git@github.com:veetihytonen/restaurant-ERP-backend.git
```
2. Create and activate virtual environment
``` 
python3 -m venv venv && source venv/bin/activate
```
3. Install dependencies
```
pip install -r requirements.txt
```
4. Create .env file and add these rows
```
DATABASE_URI=<database-local-address>
SECRET_KEY=<your-secret-key>
```
5. Start your local postgres database
6. Initialise database by running init script
```
python3 init_db.py
```
7. Run the app with command
```
flask run
```
