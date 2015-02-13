# Yelp Review Analyzer

This repository contains the code written for a personal project.

This includes the code for munging the data, training the models (to be added shortly) and running the website.



## Repository structure

```
data/
src/
	analysis/: helper modules for preprocessing, training, etc.
	config/: the global config variables (files to customize).
	review_analyzer/: the main Django app (the website).
	scripts/: scripts for munging the data, training models and deploying the website.
	web/: the Django project folder (main settings, etc.).
```

## First things first

Running the website will require you to edit the files 'src/config/django_config_template.py' and 'src/config/mongo_config_template.py'.
That should be pretty straightforward. 

Then rename these two files into 'src/config/django_config.py' and 'src/config/mongo_config.py'.

Then, you will need to download the raw dataset from [Yelp](http://www.yelp.com/dataset_challenge) 
and unzip its content into the folder 'data/raw/yelp_challenge_dataset/'.

Now, let's munge!
```
cd src/
python scripts/1_munging/1_to_pickle.py
python scripts/1_munging/2_preprocess.py
```

The code for training the different models is coming soon :)

## Testing locally

```
cd src/
python manage.py collectstatic --noinput
python manage.py runserver 127.0.0.1:8000
# change 127.0.0.1 into 0.0.0.0 for the website to be accessible externally
```

The website should now be running on [localhost:8000](http://localhost:8000/).

## Deploying on Apache

Install Apache (tested with version 2.4), then customize and add the following to the config file (/etc/apache2/apache2.conf on my Ubuntu):
```
WSGIScriptAlias / /PATH/TO/CUSTOMIZE/src/web/wsgi.py
WSGIPythonPath /PATH/TO/CUSTOMIZE/src

<Directory /PATH/TO/CUSTOMIZE/src/web>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

Restart the Apache service.
```
sudo service apache2 restart
```

The website should now be running on [localhost](http://localhost/).

## Deploying to Heroku

The website is also ready to be deployed on Heroku.

You will need the following buildpack from 'thenovices' for Numpy and Scipy.
```
heroku config:set BUILDPACK_URL=https://github.com/thenovices/heroku-buildpack-scipy
```

You will also need to collect the static files.
```
heroku run python src/manage.py collectstatic --noinput
```

The website should now be running on [MY_APP_NAME.herokuapp.com](http://MY_APP_NAME.herokuapp.com/)

