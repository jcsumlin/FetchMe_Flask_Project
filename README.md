# FetchMe Driver Rewards Tracking Application Alpha



## FetchMe the points project

![](https://www.fetchmedelivery.com/editable/templates/default/images/logo.png)

![](https://img.shields.io/github/stars/jcsumlin/FetchMe_Flask_Project.svg) ![](https://img.shields.io/github/forks/jcsumlin/FetchMe_Flask_Project.svg) ![](https://img.shields.io/github/tag/jcsumlin/FetchMe_Flask_Project.svg) ![](https://img.shields.io/github/issues/jcsumlin/FetchMe_Flask_Project.svg) [![GitHub license](https://img.shields.io/github/license/jcsumlin/FetchMe_Flask_Project.svg)](https://github.com/jcsumlin/FetchMe_Flask_Project/blob/master/LICENSE)



## Usage

First, pull the lastest code from the repository to your hosting platform:

```sh
$ git pull https://github.com/jcsumlin/FetchMe_Flask_Project.git
```
The develop branch contains the newest more unstable features of the project and it is reccomended that you stick to the master branch for live versions.


## Run the application
This application runs on python and some other packages. We need to install all of them.
To install Python 3 on Linux

Check to see if Python is already installed:



    $ python --version
*Note*:
> If your Linux distribution came with Python, you may need to install the Python developer package in order to get the headers and libraries required to compile extensions and install the AWS CLI. Install the developer package (typically named python-dev or python-devel) using your package manager.

If Python 3.6 or later is not installed, install Python with your distribution's package manager. The command and package name varies:

On Debian derivatives such as Ubuntu, use APT:

    $ sudo apt-get install python3

On Red Hat and derivatives, use yum:

    $ sudo yum install python
On SUSE and derivatives, use zypper:

    $ sudo zypper install python3
Open a command prompt or shell and run the following command to verify that Python installed correctly:

    $ python3 --version
    Python 3.6.2

### Now that Python is confirmed installed
We need to install all the packages that are required by our project so in the CLI type:
pip install -r requirements.txt


    pip install -r requirements.txt
    

Once the repository is cloned on a server and all the packages have been installed you can start the web server by issuing the following commands on the servers CLI:
```
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=80
```
If this is a windows server replace `export` with `set`

This will run the application on the public side so that it can be accessed from outside the local machine.
Now you can go log into the app and poke around as an admin. Please keep in mind this is an Alpha and the publicly accessable features are very limited.
### **Test Credentials: ** 
email: admin@admin.com
password: testing

# What about the database?
The database is actually running side by side with the web application. We decided to not use a 3rd party database for better security and ease of use. We have included the site.db file in the gitignore file so that your database will never be pushed to the repository by accident.

