# Redis with django
in this small demo we use redis to store ip of
all the users who send request . we define limits to each users to send request to our site if users 
send request above than the defined number of request in a mint
we block those ips from accessing our site . users are divided in to four groups first one are 
unauthrized user they can access the site 5 times in a minut , second ones are golden group users 
they can access 10 times/min third ones are silver they can access 8 times and last group types are 
platinum they can access 6 times/min .All of this logic is implemented in demo apps
middleware . 

## deployment
```bash
    sudo apt install docker.io
    sudo docker run -itp 6379:6379 --name run_reds redis 
    python -m venv django_install
    source ./django_install/bin/active
    git clone https://github.com/ahmadebtisam3/django-redis-demo.git
    cd redisApp
    pip install -r requirements.txt
    python manage.py runserver
```