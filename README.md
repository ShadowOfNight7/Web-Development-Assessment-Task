# Web Development Task - Leaf & Lush
Leaf & Lush will be an online store focused on selling homegrown vegetables and sharing fresh, garden-to-table recipes. The platform will connect local growers to customers and inspire healthy cooking.
## Functional & Non-Functional Requirements
### Functional Requirements
- Users can view recipes and products.
- Users can add items to their cart.
- Users can use a checkout to pay for the goods.
- Recipes link to ingredients available in-store.
- Users can login as well as add and remove credit card information.
- Users can add listings and sell produce.
- Database and front-end must be able to communcate.
### Non-Functional Requirements
- A green theme that is pleasant to the eye.
- A well designed layout that is easy to navigate.
- Smooth transitions between pages.
- Users can view order history.
- Should not take excessive time to load.
- Users can rate recipes and goods. 
## Scope
Due to time constraints the scope of the project will be limited three simple but core parts browsing what the website has to offer, logging in, be able to buy produce. Additionally, if time permits also a way for users to add listing and sell produce.
## UI Design Wireframe
| Choices | Description |
| ----------- | ----------- |
| Colour Palette | The colour theme I chose was white, pastel green and other variations. The white gives a clean and semi-professional look. While on the other hand, the pastel green also gives gives the website welcoming look. The various shades of green can be used to highlight certain aspects of the UI such as button, textboxes, etc. |
| Typography | I chose a combination of the fonts Newsreader and Inter. They are both clear and professional fonts perfect for my goal of trying to create a casual professional website. |
| Images | The images I chose for the recipes and products are all eye-catching, straight to the point, and appealing. These images will allow the user to see recipes and products before they make or buy them. |
### Images Of Wireframe
![](Assets/UIDesignWireframe1.png)
![](Assets/UIDesignWireframe2.png)
![](Assets/UIDesignWireframe3.png)
You can view the wireframe in better detail [here](https://www.figma.com/design/GM4gpWhBxVio2TyjBGHUlF/Leaf---Lush---2025-Computer-Technology-Assessment-3---Yi-Ping?node-id=1669-162202&t=JQH6FRsWkqxtmnar-1).
## Alternate Wireframe Design
| Choices | Description |
| ----------- | ----------- |
| Colour Palette | The colour theme I chose was white, pastel green and other variations. The white gives a clean and semi-professional look. While on the other hand, the pastel green also gives gives the website welcoming look. The various shades of green can be used to highlight certain aspects of the UI such as button, textboxes, etc. |
| Typography | I chose a combination of the fonts Newsreader and Inter. They are both clear and professional fonts perfect for my goal of trying to create a casual professional website. I also decreased the amount of writing to make the descriptions and recipes less tedious to read. |
| Images | The images I chose for the recipes and products are all eye-catching, straight to the point, and appealing. These images will allow the user to see recipes and products before they make or buy them. I also increased the amount of images to make the website more visually appealing. |
### Feedback Incorporated
Following my client's feedback I reduced the amount of text on the pages by making the descriptions shorter and the instructions more concise. The recipes also have more images to break up the text more. Additionally, I resized the product displays, which were previously unnecessarily large. Furthermore, I reduced the scrolling required on all pages, as per the client's request, especially on the homepage and increased image sizes for better user engagement. 
### Images Of Alternate Wireframe
![](Assets/UIAlternateDesignWireframe1.png)
![](Assets/UIAlternateDesignWireframe2.png)
![](Assets/UIAlternateDesignWireframe3.png)
![](Assets/UIAlternateDesignWireframe4.png)
You can view the wireframe in better detail [here](https://www.figma.com/design/GM4gpWhBxVio2TyjBGHUlF/Leaf---Lush---2025-Computer-Technology-Assessment-3---Yi-Ping?node-id=1669-162202&t=JQH6FRsWkqxtmnar-1).
## Flowchart
Flowchart of the login page and the account creation. 
![](Assets/LogInPageFlowchart.png)
### Test Case 1
**Test Case ID:** 001

**Test Case Name:** Logging In

**Prediction:** User will sucessfully login, see their account info, and log out.
### Steps
1. Code checks if database is accessable. Code will reload until the database is accessable.
2. Prompt the user to enter login details.
3. User will enter details.
4. The code will check if the details match the database.
5. The details will be correct and the code will pull the user's data from the database.
6. The code will display the information.
7. The user will log out and the code will end.

### Test Case 2
**Test Case ID:** 002

**Test Case Name:** Failing To Login And Creating Account

**Prediction:** User will fail to log in, create an account, and there will be a new account in the database.
### Steps
1. Code checks if database is accessable. Code will reload until the database is accessable.
2. Prompt the user to enter login details.
3. User will enter details.
4. The code will check if the details match the database.
5. The details will be incorrect and the code will prompt the user to try again or create an account.
6. Code will prompt user to enter details for a new account. 
7. The code will check if the username is taken. If it is then the code will prompt the user to try again.
8. If all the info are valid then the new account will be created.
9. The code will then pull the account info from the database.
10. The code will display the information.
11. The user will log out and the code will end.