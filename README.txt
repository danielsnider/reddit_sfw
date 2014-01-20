Reddit_sfw
========

Reddit_sfw (Safe For Walls) is a digital picture frame web app built with the pyramid framework. With it you can view reddit SFW pictures in full screen.

Concepts demonstrated in the code include:

- SQLAlchemy based models 

- Url dispatch mechanism

- Built-in authentication and authorization mechanism

- Built-in session mechanism

- Retrieved JSON from reddit is cached for 15 minutes 

Requirements
--------------------
- Python 2.7 (python2.7-dev)

- SQLite3 (build-essentials, libsqlite3-dev)

- Setuptools (ez_setup.py)

- Pyramid Famework

- virtualenv

Installing and Running
----------------------
	virtualenv --no-site-packages env
	cd env
	bin/easy_install pyramid
	git clone git@github.com:danielsnider/reddit_sfw.git
	cd tutorial
	python setup.py develop
	../bin/initialize_tutorial_db development.ini
	../bin/pserve development.ini --reload

Inspiration:
------------
- https://github.com/Pylons/pyramid/tree/1.3-branch/docs/tutorials/wiki2/src

- https://github.com/Pylons/shootout
