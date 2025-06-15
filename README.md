# JoinHands
#### Video Demo:  <https://youtu.be/NFTl0gQ0Ff0?si=-iNnNuAmaxLt4hQQ>
#### Description:
Web application made with Python, HTML, CSS, and SQL for CS50x course final project. 
JoinHands is community focused platform where individuals can connect with people who aims to make an impact in the world by volunteering. 
It's purpose is to make happen as many events as possible and make use of as many human power as possible to together act towards a better society. 
##### Design:
This web application required the 2 basic folder, 2 python files, and a database. These are static folder containing styles.css, templates folder containing a bunch of different html files, app.py, helpers.py and joinhands.db. I will be going deeper into each of this. 
###### styles.css:
This file contain all the aesthetic purposes which in my case aren't much as I kept the web app simple. They include the font size for the navigation bar, and the green and blue colors for the JoinHands logo. 
###### layout.html:
This file is within the templates folder. It is the foundation of all the other file in the templates folder (all the other files are an extension to this folder which is declared in the first line of each of those files) acting as a template for each of them and hence reducing redundancy of lines. 
These are what this file contain in order:
- meta tag so the web would work in different devices ie. laptop, phones, and ipad. 
- getting bootstrap features into the web app.
- title tag for the template of each title for each page.
- nav tag with other tags inside it to create a navigation menu on top which includes: the JoinHands logo itself, navigation to the post page, signup page, log in page, log out page, and sign up page
- container for the html files that will use this template.
###### apology.html:
This file is within the templates folder. It contains an image tag containing a source from api.memegen.link and a background from a jpg link of my choosing. This produces the apology web page (a message on top of a background) that alert users whenever they make an error or did something unpreferrable such as: emptying an input field, trying to register with a username that already exists, putting different input when asked to confirm their password, inputing the wrong password to a username, trying to register for the same event more than once, not following the required datatype and more. 
###### index.html:
This file is within the templates folder. It acts as the homepage of the web application. The file contains 2 table tags with different attributes for spacing purposes using bootstrap features. One table shows the events a user has registered for and the date of the event while the other table keeps tabs of the usernames that registered for the event the user has posted. It uses a for loop to fill in the tbody tag for both tables using jinjja features ({%-%}). 
###### login.html:
This file is within the templates folder. It contains a form tag with nested input tags for users to input a text of their username and the corresponding password, and a nested button tag that's labeled Log In. This form, when submitted, is given an action to go to the login route by post method. It also has an image tag of a link i chose for aesthetic purposes under the button. 
###### post.html:
This file is within the templates folder. It also contains a form tag with 3 input fields for event name, the date, and the number of people they need for the event. Once submitted, the form goes to the post route. Under it is a button to submit aka post the event to the server. 
###### register.html:
This file is within the templates folder. It's structure is similar to post.html yet the fields are all of text datatypes for a username, password, and a confirmation of that same password. Instead of to post, the button in this file is labeled register and it's action is to go to the register route. 
###### signup.html:
This file is within the templates folder. It contains a form tag with select tag inside. The options for this select tag are produced from a for loop to show all the events that have been posted and are not full yet. The button in this file is simply to submit. 
###### app.py:
This python file is where all the other files are connected. It is what's run and contains the logic that makes the web application work. The web application requires several libraries which is imported in this file. These include cs50, flask, flask_session, and werkzeug.security. It also imports from another python file in the folder named helpers.py which will be covered further down this description. On the very top of the file, it displays what's required for flask run to work, session to specifically identify whose currently in the page, and uses SQL from cs50 to work or connect with the joinhands database. After all that, it declares all the different routes that the app can take. Several of these routes requires login before the function can run because some datas should be accessible to some but not others. 
Every input that users sent in are put into a variable. If any of these variables are empty, an error message is sent.
The first route contain some logic in order to obtain the datas required to render index.html: information about the events they registered and posted. The second route, with get, runs register.html. With post, it ensures the password field and the confirmation field are the same, insert the approved username and password into the database, and assign a session id for the user. The rest of this file detail each of the routes as such.
