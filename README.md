# NETS213, Final Project: Truck Tracker
### Sam Davis, Gabriel Ruimy, William Spence, Michael Zhou

## Major Components of Project

### 1. Crowdsourcing data collection (4)

The back-end, which will encompass all of our data collection about the food trucks in our target area, will be built with the use of a general crowdsourcing platform (AMTurk, Figure-Eight, if possible create our own survey model for students at Penn). While utilizing a standardized survey model on the platforms we have used thus far for this class is the easiest way to collect data, it might not be applicable to our direct customer base. This is because most of the food trucks in our area, such as Bui's, Chez Yasmine, etc., don't necessarily post prices and menu options online so that non-local agents (i.e. India-based Turkers) could scrape them accurately. Hence, we will most likely implement a Google Form crowdsourcing format where the link will be open to all those who can enter an accurate @upenn.edu email.

Milestone 1:
Create survey questions so that users can input what meal options are present at a particular truck and the accompanying prices.

Milestone 2:
Design reach-out campaign so that form can reach a maximum number of students and faculty within the local area.

Milestone 3:
Collect information in CSV format for data clean-up method to parse through and pass to user interface.

Milestone 4 (optional):
Implement a "take a photo" of menu option that enables Penn affiliates to take photos of food truck menus, upload them to our back-end that will then make queries on AMTurk/Figure-Eight for photo-text conversion so that we can then implement it onto our UI.

### 2. Data clean up method (3)

Once we receive all the data in CSV format, both as an amalgam of Penn affiliates uploading text information and the photo-text conversion from online Turkers, we will need to apply one of the quality control methods we implemented in the last assignment to make sure the right prices and menu options are put up.

Milestone 1:
Implement majority vote method. This is quite straightforward: as long as an agent submits a price/food item that others have, that agent won't be marked as a corrupting data input and their data will be internalized for our user UI.

Milestone 2:
Confidence-weighted vote. Some of our group members will go out and get a few food truck price/menu informations and use them as a gold standard. Provided a user manages to write down the correct prices, or a Turker (given the correct photo) can transcribe the prices and menu items correctly, they will be given preferential weight in a majority vote.

### 3. Data link (4)

After we have collected the data, formatted it accurately and quality checked it so as not to feed incorrect information to our users, we will need to create a link between our CSV information and an HTML webpage so as to display the information back to end-users. We will most likely be using the MEAN stack to create the webpage and the appropriate routes, how we host the website will be decided on cost/appropriateness.

Milestone 1:
Create routes and back-end connection to convert CSV data into appropriate HTML information for webpage to display.

### 4. User interface/display (3)

With everything ready, we'll need to create a visually appealing interface so that end-users are enticed into using our platform. Furthermore, it'll need to integrate the data in a streaming format; while prices shouldn't be fluctuating too severely, some prices could be going up/down alongside menu offerings or promotions. On top of that, more trucks will be added on a day to day basis as our crowdworkers find more trucks to input into our platform.

Milestone 1:
Create visual design on paper to appropriately display the information and convert into HTML webpage.

Milestone 2:
Connect with data routes from step 3 to have appropriate information displayed in live feed method.

Milestone 3:
Establish hosting/marketing so that it can reach our end-user base.

### 5. Incentive driving mechanism (4)

To power this entire idea, we need to create initial incentives so that users populate the food truck data structure sufficiently to provide valuable information. There are multiple ways to accomplish this, but we must devise the best one, if any at all. While we have considered giving rewards to active users such as allowing them to order through our webpage, it'll be extremely difficult to implement. Also, multiple crowdsourcing platforms, such as Wikipedia, succeed on the benevolence of their users (since everyone stands to benefit).

Milestone 1:
Devise incentive rewarding mechanism.

Milestone 2:
Implement it accordingly.



### Quality Control and Aggregation (deliverable 2)

#### Locations of Requested Files:

Raw data for possible mturk tasks:
/data/menu_images/*

Aggregation Input:
/data/nets213sampleprojectdata.csv

Aggregation Output:
/data/menu.csv

Quality Control Input:
/data/nets213sampleprojectdata.csv

Quality Control Output:
/data/quality.csv

Code for Quality Conotrol and Aggregation:
/src/QC:Aggregation.py


#### Aggregation Description:

The aggregation module takes in a csv with a users id, the restaurants name, address, fooditems, and prices. The module creates a three level dictionary structure. The key of the first is the food truck name, the key to the second is the name of the food itself, and the key to the last is the price of the meal. For the last dictionary, the value is how many times that price has been input for that meal at that food truck. The dictionary is created by iterating through all food and price cells for every row in the table adding dictionaries to the structure when they do not exist. This overall dictionary structure is then iterated through and using majority vote the data is output as a list of tuples of the form (Truck, Food, Price). This module also outputs a dictionary that becomes an input for quality control. This dictionary is of the form {truck Food: price}.

#### Quality Control Description:

This module takes in the dictionary from aggregation and the same csv as aggregation. It matches to see if individuals were correct or incorrect for every data point they input related to food and price. The number correct is then divided by the number provided by the individual to give a quality score out of 1. The quality is output along with the user_id as a list of tuples of the form (user_id, quality).


#### Going Forward:

Some things with this design will definitely change as the project moves forward. We plan to move to weighed majority vote and not include data in our output set when there are no other users to corroborate it. We are also going to find a way to impliment addresses into the system which will most likely be somewhat challanging. This is because trucks can move rendering correct data seemingly incorrect. If this is factored into weighted quality control it could skew the scores and artificially lower the quality of some. Further, we will need to find a way of balancing new data collection with existing data and getting rid of outdated data. If a food truck takes an offering off their menu this will be difficult to identify and rectify. 

### Code for Milestone 3

Added within this milestone are a few changes. First, the quality control method has been updated. We have changed to a two round process when it comes to our HIT. We will put out a first HIT with known answers, once this hit comes back we will compare it with the answers we have generated. Any worker that has over a ninety percent accuracy rating will be given a special qualification to do the real HITs. The HITs consist of a picture with thirty slots to put food items and prices. Once that data is collected we aggregate and use the script upload_menu.py to upload the data to dynamodb. We then take the data given from users taking photos to upload location data to dynamodb as well. Our website takes data from the location table to put out pins on a google map giving truck locations and names. If the user presses the menu button in a markers popup window, they will be taken to a page with food items and prices for a given truck. On the main page, there is a button to upload truck data from users to add new trucks to our system. 
