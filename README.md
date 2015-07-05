# Yelp Review Analyzer

This repository contains the code written for a personal project.

This includes the code for munging the data, training the models and running the website.



## Repository structure

```
data/
	pickle/: the munged datasets are pickled there. 
	raw/: the raw datasets are stored there.
	models/: the various models built for the projects are pickled there.
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

Then we can train and run the different models.
```
python scripts/2_modelling/1_train_topics.py
python scripts/2_modelling/2_train_categories.py
python scripts/2_modelling/3_predict_topics.py
python scripts/2_modelling/4_predict_categories.py
python scripts/2_modelling/5_annotate_topics.py
```

And deploy...
```
python scripts/3_deployment/1_prepare_data.py #coming soon
python scripts/3_deployment/2_insert_database.py
python scripts/3_deployment/3_upload_data_heroku.py
```

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
I am using it with the addons MongoLab (MongoDB database)
and MailGun (email server, to know when bugs/errors occur).

First, you will need the following buildpack from 'thenovices' for Numpy and Scipy.
```
heroku config:set BUILDPACK_URL=https://github.com/thenovices/heroku-buildpack-scipy
```

Now you can deploy the app. As final step, you need to collect the static files.
```
heroku run python src/manage.py collectstatic --noinput
```

The website should now be running on [MY_APP_NAME.herokuapp.com](http://MY_APP_NAME.herokuapp.com/)

