# Jeff Chen SEO
Jeff Chen SEO is a website built for anyone to vote for their favorite (the best) Jeff Chen on www.jeffchenseo.com.

This is the code for a fully functioning Django website built for deployment on AWS Elastic Beanstalk (with lots of interesting features - Environment Variables! CSV Exports! Debug tools!).

It could be potentially modified for anyone to create a website where anyone could vote for the best person for a specific name.

However, these instructions will currently only cover how to get this running on your local environment. Getting a fully functioning website requires instructions far beyond just knowing Django with things like configuring AWS EB, S3, RDS, Route 53, ElasticSearch, ElasticCache, DNS Servers, CDN, SSL certificates etc. There are many guides online which should help you do this and you too can become an AWS master (watch out for those pesky Access Policies)!

Note: This might not be for beginners, I won't be explaining much as I go along, but simply the exact steps you need to get started. If you have never created a Django project before, you may want to do the tutorial to understand (Currently Django is on 2.0, but jeffchenseo was built on 1.11 so I recommend the 1.11 tutorial): https://docs.djangoproject.com/en/1.11/intro/install/.

## Getting started
1) Clone this repo onto your desktop using Terminal
```angular2html
cd desktop
git clone git@github.com:thejeffchen/jeff-chen-seo.git
cd jeffchenseo
```

2) Install virtualenv and create a new virtual environment
```angular2html
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

3) Install the requirements from the environment
```angular2html
pip3 install -r requirements.txt
```

4) Change into main Django directory 

```
cd src
```

5) Create a new environment variable file and set the Django Secret Key variable and fake variables

```angular2html
touch .env
nano .env
```
Now you should be in the .env file

Generate a new secret key here: https://www.miniwebtool.com/django-secret-key-generator/

Paste this information into the .env file
```angular2html
DJANGO_SECRET_KEY='zp7ywipy7k--$^b85s#5dl(u_7z(0k(o%blo6$wq&d33-2a=0%'

# S3 settings
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''

# Mailgun settings
MAILGUN_ACCESS_KEY=''

# Keen
KEEN_PROJECT_ID=''
KEEN_WRITE_KEY=''
```

Press ctrl+x to exit and 'y' to save changes

6) Download Postgres.
I recommend this site: https://postgresapp.com/

7) Create a new database called jeffchenseo

So here I like just using a GUI to create the database: https://macpostgresclient.com/. I like this one the most, but it costs $40 (worth it imho). 

You could use the free one: https://www.pgadmin.org/, but I find the interface more confusing than useful. 

Lastly, you can use the terminal for any changes you make to the database: https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb (I've done it before, but over time I find it incredibly time consuming. Using a GUI is simpler)

8) Migrate the Django tables to Postgres
```angular2html
python3 manage.py makemigrations
python3 manage.py migrate
```

9) Run the server!
```angular2html
python3 manage.py runserver
```

Open 127.0.0.1:8000 and the website should now open

10) Create an admin user
```angular2html
python3 manage.py createsu
```

11) Login to the admin panel

Navigate to: http://127.0.0.1:8000/admin/

Username: admin

Password: admin123



Congrats! You should have now installed a fully functioning version of JeffChenSEO on your local development server!

Feel free to let me know if there were any errors or if there are any questions!