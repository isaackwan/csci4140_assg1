# Web Instagram

Assignment 1, CSCI4140

## Live Demo URL

[https://vanilla-csci4140-rocks.a3c1.starter-us-west-1.openshiftapps.com](https://vanilla-csci4140-rocks.a3c1.starter-us-west-1.openshiftapps.com)

## OpenShift Instructions

Although the default Python S2I image is used, a [special image](https://github.com/isaackwan/python27-s2i-with-imagemagick) that I built is used instead because ImageMagick is not available.

When configuring OpenShift, one should select "Build From Docker Image" and enter image "isaackwan/python27-s2i-with-imagemagick" under the "Image Configuration" section.

Furthermore, the environmental variable `CSCI4140_URL` is set to the URL of the instance.

## What each directory stores and their corresponding functionality
- upload_temp - photos that have just been uploaded / is being edited
- uploads permanently stored photos
- static - CSS, template file, resources for ImageMagick
- .idea / python-cgi-example.iml - IntelliJ IDE files
- insta.db SQLite database
- HTML files on 'root' directory - static HTML forms
- cgi-bin - collection of Python CGIs
	- Self explanatory: change_password.py, editor.py, index.py, login.py, logout.py, register.py, reset.py, upload.py
	- Finish.py - screen to show URL after upload finishes
	- html_helpers.py - store the header & footer
	- init.py - Python module specification
	
### Briefly introduce the procedure of building your system, including some key components, e.g. which database package you use.

There is no need to 'build' because Python is an interpreted language and there is no external dependency (pip etc.)

SQLite3 is used as DBMS. It is a flat-file DB and does not require a server daemon.

Bootstrap, a popular CSS library, is used for formatting for some pages.

For built-in Python modules used, `CGI` is used very heavily for parsing input parameters. `Cookies` are also used for generating headers for cookies. Of course `sqlite3` module is also used.

### Which parts you finish very well and want to request for some bonus and which parts you have not fully completed and give some reason.

None