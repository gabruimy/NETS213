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
