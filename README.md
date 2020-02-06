<h1 align="center">relisterine.py</h1>

<p align="center"><b>Automatically renews all of a user's Craislist posts.</b></p>

<p align="center">
  <img src="https://raw.github.com/Wingman4l7/relisterine/master/relisterine_successful.png"/>
</p>

## About ##
I was posting a lot of stuff to Craigslist pretty regularly, and working on browser automation projects using Selenium, so this seemed like a natural quick practice script that would be a personally useful tool.

There are several similar scripts on Github, using different languages and dependencies, all in various stages of polish and functionality.  As of my initial commit, it has been running daily for several months now with no issues.

It currently only supports a single Craigslist user -- it is not intended for "commercial" use -- but it would be trivial to extend this script to support multiple user accounts via a config file modification and an additional function in the script that would iterate across the multiple logins provided.

As usual, credit goes to [AlliedEnvy](https://github.com/AlliedEnvy) for the clever name.

## Installation ##
This was written for [Python 2.7.x](https://www.python.org/downloads/).  It will likely work in Python 3.x.

### Dependencies ###
The dependencies are `configparser` *(for reading your account login info from your config file)*, `selenium` *(for browser automation)*, and `colorama` *(for nice pretty colored console text that is also Windows-compatible)*.

You can use `pip` to install these dependencies from the project folder:

 - `pip install -r requirements.txt`

Tested & working on several versions of Chrome, up to 69.x.

### Chromedriver ###
You will also need to install the [chromedriver binary](https://chromedriver.chromium.org/).  A couple things to pay attention to:
* You may get an error if the version of Chrome doesn't match up with the version of chromedriver.  Reference the [Version Selection](https://chromedriver.chromium.org/downloads/version-selection) page if you suspect you're getting errors related to this when running the script.
* If you're getting the error `'chromedriver' executable needs to be in PATH`, you will need to fix where the script looks for the chromedriver binary.  This path is hard-coded in the declaration of the `chromedriver` variable in `main()`.

## How to Run ##
For now, this is as simple as:

	python relisterine.py

If there are no listings that need to be renewed, it will output that message and complete.  The way it is written, it should not leave any spawned console or browser windows open upon successful completion.

It is most useful when scheduled to run via cron / Windows Task Scheduler / etc.  If run via a scheduler, you may need to change the `config.read()` line to be an abolute path instead of a relative path, for it to work properly.  

### Config File ###
Simply add in your Craigslist username and password to the config file, and you should be good to go!

**WARNING:** If you clone this repo so you can use it or modify it, BE CAREFUL and DO NOT UPLOAD a commit of your config file with your Craigslist username & password in it!

## How It Works ##
This uses Selenium to hook directly into a Chrome window and seeks out elements in the page DOM to find and renew any and all Craigslist ads up for renewing.

It's possible you could run this headless *(without a browser window spawning)* -- take a look at the options for a commented-out example -- but I haven't really tested this.  A quick hack that will get much the same result is to modify the spawned window dimensions to be negative values; this will place it offscreen.

## License ##
I haven't bothered to formally declare which license this is going to be under, but it's obviously open-source, and it will probably be some flavor of [Creative Commons](http://creativecommons.org/licenses/), or maybe [GPL](http://www.gnu.org/licenses/licenses.html).
