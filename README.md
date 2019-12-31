# Sample Project Pinochio's Pizza

Web Programming with Python and JavaScript

Pinochio's Pizza and Subs

A website for a pizza restaurant. The website is designed to add and manage orders for a pizza restaurant in Cambridge Mas. USA. The home page gives details of the business and how to contact them. The menu page allows a logged in user to access the restaurant menu and add items to their basket should they so wish. The basket icon takes the user to a basket page where they can choose any toppings or additional fillings for their order. Once these have been selected they can complete the order.
Once completed the user is able to see if their order has been cooked via the My Orders page. This allows the user to look at any orders made that day and also gives access to their ordering history where they can see all the items they have previously ordered.
A user marked as a member of staff is given access to the Order List page which gives details of all orders made today. The orderlist is used to mark items as completed once they are ready for collection. Once all items in an order are ready for completion the user is sent an email letting them know their order is ready to collect.

In order to run this project install the requirements in requirements.txt. Then set the following environment variables:

# For security:
SECRET_KEY = a random secret key for the app

# For the database:
DATABASE_ENGINE = django database engine of choice eg. django.db.backends.postgresql
DATABASE_NAME = name of the database
DATABASE_USER = database username
DATABASE_PASSWORD = database password
DATABASE_HOST = database host address
DATABASE_PORT = database port

# For emails
EMAIL_HOST = the host address of your email service
EMAIL_PORT = the port used by your email service
EMAIL_ADDRESS = your email address
EMAIL_APP_PASSWORD = the app password for your email address