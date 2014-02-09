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

- SQLite3 (build-essential, libsqlite3-dev)

- Setuptools (ez_setup.py)

- Pyramid Famework

- virtualenv

Installing and Running
----------------------
	sudo apt-get install python2.7-dev build-essential libsqlite3-dev curl
	wget -c http://peak.telecommunity.com/dist/ez_setup.py
	python ez_setup.py
	sudo easy_install pip
	sudo pip install virtualenv
	mkdir reddit_sfw
	cd reddit_sfw
	sudo virtualenv --no-site-packages env
	cd env
	sudo bin/easy_install pyramid
	bin/pcreate -s alchemy reddit_sfw
	rm reddit_sfw
	git clone git@github.com:danielsnider/reddit_sfw.git
	cd reddit_sfw
	../bin/python setup.py develop
	../bin/initialize_tutorial_db development.ini
	../bin/pserve development.ini --reload

Inspiration:
------------
- https://github.com/Pylons/pyramid/tree/1.3-branch/docs/tutorials/wiki2/src

- https://github.com/Pylons/shootout


Known Issues:
--------------

