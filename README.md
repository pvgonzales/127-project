# DineReview: Establishment and Food Review System
#### Group Members:
Asiddao, Dale Martin <br/>
Gonzales, Paula Victoria <br/>
Irapta, John Ryan <br/>

### Description
Explore the world of dining with DineReview, your ultimate guide to food and establishment reviews. Whether you’re a seasoned foodie or just looking for a great place to eat, this program offers a seamless experience to find, review, and share your food journeys. <br/>

This project is an application using Python and MariaDB, and is in partial fulfillment for CMSC 127 <br/>

### Project Features and Usage Guidelines
 - User Authentication
    - Registration: Users can create an account by providing a valid email address and setting a password. During the registration process, users might also need to verify their email address through a confirmation link sent to their inbox.
    - Login: Once registered, users can log in to the application using their email address and password. Successful login grants access to the application’s features.
    - Access Control: Only authenticated users can access the application's features, ensuring that all actions (e.g., adding, updating, and deleting establishments and food items) are performed by registered users.
 - Find, Share, Update, and Delete an Establishment
    - Find: Users can search for establishments within the application. The search functionality allows users to find establishments by name.
    - Share (Add): Users can add new establishments that are not already in the database. This involves providing necessary details such as the establishment's name, address, capacity, and other relevant information.
    - Update: Users can update the information of an existing establishment. This includes editing details like the name, address, contact information, and capacity of an establishment.
    - Delete: Users can remove an establishment from the database. This action is restricted to ensure that only authorized users can delete entries to prevent misuse.
 - Find, Share, Update, and Delete a Food Item from an Establishment
    - Find: Users can search for food items available at various establishments. The search can be filtered by item name, food type, or the price.
    - Share (Add): Users can add new food items to an establishment's menu. This requires providing details such as the item’s name, description, price, and any relevant information.
    - Update: Users can update details of an existing food item. This might include changes to the item’s name, description, price, or food type.
    - Delete: Users can delete a food item from an establishment’s menu. This ensures the menu remains up-to-date and accurate.
 - View, Share, Edit, and Delete a Review
    - View: Users can search and read reviews written by other users to gather insights and make informed decisions.
    - Share (Add): Users can write and submit reviews for establishments or specific food items. Reviews typically include a rating, comments, and possibly media such as photos.
    - Edit: Users can edit their previously submitted reviews. This allows them to update their feedback based on new experiences or corrections.
    - Delete: Users can delete their own reviews. This gives users control over their contributions and helps maintain the accuracy and relevance of reviews within the application.