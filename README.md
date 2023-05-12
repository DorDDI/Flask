#Movie and Music Blogs Using Python Flask

In this blog you can search for movies and music live and up to date.
The blog have an account management with a login and register options, update the user account including forget password option that send to the selected email a mail with reset password with uniqe token.
Movie blog contains movie and TV serias information using info which are taken from IMDB.
Music blog - is still under maintenance
In every section there is an about page that will give information on the section.
All the pages are display using paging system
##Requirements
Python 3.7 or higher
Using environ variables using os library (os.environ.get):
	need to have an 'EMAIL_USER' that represent the email username
	need to have an 'EMAIL_PASS' that represent the email password

##Installation

1. Create a python environment
2. Install pip packages:
	pip install -r requirements.txt

##Movie blog section

In the main page of the movie blog we can see all the post and review that was posted by the users. in every post we can see the post author, the date the post was created and the content of the post.
If clicked on the user name, a page with all the user post will be display. Additionally there is an option to look on the user watchlist.
If the user is the author of the post, the user can update and delete the post.

On the side there is the Movie Sidebar that contain the following options:

###My Watchlist:
In this options we can see the user watchlist that was added.
Every item contain the name of the movie/TV seria, the time added to the watchlist and info: year, actors, watching status of the user and the rate of the user.
If the user is the owner of the watchlist, he can update his watch status and rate and delete the item if wanted.

The watchlist option can help users see the other users watchlist to get recommendation based on their opinion.

###My Search:
The search option provide a search option of a movie to TV seria in a text input.
After the user press the search button, the five closest option will be show. Each option will show the option name, year and actors.
When an option was selected it will show more info of the item with a add to watchlist button.

###My Popular Movie/TV Seria:
In this option we will get the most popular movie/TV seria.
In the main page of the popular movie/TV seria we can select how much items to show, the genre of the items and from which index (if selected 10 items to show and index 5 it will show the most popular from the fifth to the fifteenth most popular items)
After the search it will show all the items that found. When click on one of the options it will display the search page of the movie like the search option.

###My Upcoming Movies:
In this option we will get upcoming movie.
We can select the number of upcoming movies to show. After select the number of the movies to show, it will display the movies divided by date of release.
When click on one of the options it will display the search page of the movie like the search option.

##Music blog section

In the main page of the music blog we can see all the post and review that was posted by the users. in every post we can see the post author, the date the post was created and the content of the post.
If clicked on the user name, a page with all the user post will be display.
If the user is the author of the post, the user can update and delete the post.

This section is still under maintenance.