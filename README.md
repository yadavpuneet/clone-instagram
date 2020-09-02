Overview

This application is the replica of Instagram in simpler version. Using this application user can post in their timeline with image as well as text for reference. This application also allows different users can follow and followed by others using the app. They can also see other users posts and can also comment on them.

1	INTRODUCTION
1.1	Purpose and Scope
The purpose of this application is to simple work on the Instagram model. Where different people can meet one another and post as well as comment on their wall.

1.2	Project Requirements
1.	Python 2.7
2.	Google app engine
3.	Git Repository

2	SYSTEM ARCHITECTURE
1.	JINJA ENVIRONMENT:
Jinja helps in defining of global objects as a central object in the template environment. Instances used here are further used to configure and store of the global variables, which are further used to load templates from other locations. It also helps to locate the root directory for google app engine. 
We define member timeline as a global variable which stores the information of posts and comments by their time and date. 
It also helps in initialization of user request login with there user mail id and the task they created.
2.	CLASS MAIN HANDLER
Def get(): Here we only initialize the request pulls out form global variable and checks if the user is logged in with their email id and passes the specific parameters for verifying it. 
3.	CLASS NEW POST HANDLER
Def post(): Here after login and pulling out the main page user can post on their wall with image as well as text. The post will display with time and member key value. Images are stored in blob store to handle the storing and managing of multiple images.
4.	CLASS PROFILE VIEW HANDLER
Def get(): When user clicks on the profile view it initialize the global object and displays the information of user stored as id as parameter.
5.	CLASS SEARCH PROFILE HANDLER
Def post(): It pulls out the form with the help of which user can search other member using the application. After the details form pulls out, if email id of the user exists, then it pulled out and the invitation was success. If the user invited is not exists, then it returns the value and redirected to the same page.
6.	CLASS FOLLOW PROFILE HANDLER
Def get(): Initially it checks weather the user is logged in or not as these functions is depend on ndb key values. If the ndb values are true, then the desired function is called. 
After the information is pulled user can follow the other user. Profile and name work as the key values and if ndb key value is true user get the desired existing user.
7.	CLASS UNFOLLOW PROFILE HANDLER
Def get(): Initially it checks weather the user is logged in or not as these functions is depend on ndb key values. If the ndb values are true, then the desired function is called. 
After the information is pulled user can unfollow the other user. 
8.	CLASS SHOW FOLLOWING HANDLER
Def get(): Checks weather the user is logged in or not. This function also depends on the ndb.key value of the current user logged in. This pulls out the form which shows the user followed by the current user.
9.	CLASS SHOW FOLLOWER HANDLER
Def get(): Checks weather the user is logged in or not. This function also depends on the ndb. Key value of the current user logged in. This pulls out the form which shows the current logged in user followed by the other user.
10.	CLASS POST COMMENT HANDLER
Def post(): Firstly, it checks weather the user is logged in or not after this pulls out the information about the comments done by other user on the post. The comment is saved with user id as ndb key value. 
Then the comment is saved with key stores that information about the user and data time of the comment.
11.	CLASS POST REACT HANDLER
Def post(): It pulls out the information of the user logged in. The parameters of the ndb key value is user id.
Then the reaction on post is saved with reaction key into datastore. Reaction key stores the information about the user comment and data time of the comment.
12.	Webapp2.WSGIApplication
For defining the route access for the user who have specific access to that function. By default, it doesn’t know which page user wants to access therefore, we must define the expected route through routing table in python.

3. DATASTRUCTURE USED (NOSQL) 
This application works on google app engine which supports NoSQL database to store information and don’t rely on traditional database structures and stored more flexible data models. NoSQL database is schema free can handle variety of data even in huge amount, it also helps in replication of data to avoid the single point failure. The data can be store by their key values in the database, all other parameters were stored in wide column structure. This will help us to store huge amount of data with speed development and increased horizontal scalability. 
This data structure is used by google app engine to fully managed the cloud service, which helps replication and handles shredding to ensure the consistent working of the database.

4. DATAMODEL (NDB) 
	This model depicts the structure of the entities stored in the database. Model classes define in the application to indicate the desired entities and their structure. The model is inherited by the given class model can be directly or indirectly inherited from main model. 
NDB model is also used to describe the definition of class declared straightforward used to declare the model class structure. The definition of property helps the system to identify the names and types of field stored in the cloud storage. We used two property of ndb in our application:
1.	String property: is used to store the name of the task boards and tasks created.

2.	Date time property it is used for storing information of date time values according to different time zones.

3.	Key property: it defines and store the task and user information with their key values which help in identifying them at the time of assigning.

4.	Blob key Property: It define the storage system to store photos and large objects in low cost scalable storage.

5. DOCUMENTATION OF USER INTERFACE:
1.	Simple interface is created for end user to operate the application.
2.	Old school but powerful interface to full fill the needs of the user.
3.	Background is clear white with bold black words and text boxes for entering desired entry.
4.	Buttons are clearly visible with there use. All the buttons are perfectly arranged according to their use.
5.	On the screen user can see his email id with which user logged in.
6.	All  the Headings and subheadings are arranged according to the working of application.
7.	The area for new post is clearly visible with explanation.
8.	User can easily post and add images to its post.
9.	On the home page the posts done by user were seen in reverse chronological order.
10.	In the profile section user can see their posts and followers and following of the current user logged in.
11.	All the functions are clearly visible with there explanation what they are doing.
12.	When other user wants to comment on the post in pops out the new window where they can comment on the post.
13.	All the post and reaction on them were saved reverse chronological order with date and time.
14.	At last home and logout buttons placed with one another and clearly visible to the user.

Liscence ©yadavpuneet
