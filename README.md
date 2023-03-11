# microservice-ecommerce-website
An e-commerce website broken down into 5 microservices written in different languages (TypeScript, Python, Java, ASP.NET, Ruby). Each microservice communicates with each other using RESTful APIs.

### User Management Microservice
Written in TypeScript, built on node.js, and utilizes the Passport.js middleware to handle user signups, authentication, and deletion. JWTs are used for authentication between microservices.

### Product Catalog Microservice
Written in ASP.NET and implements a MySQL database. Supports basic CRUD operations using HTTP methods.

### Shopping Cart Microservice
Written in Python and uses the Flask framework. Interacts mostly with the product catalog microservice to manage each user's inventory.

### Payment Processing Microservice
Written in Java, uses the Spring framework, and implements the Stripe API to handle secure payment processing.

### Order fulfillment microservice
Written in Ruby and implements the Rails framework and also implements the Spree Commerce platform for order management and shipping integration.
