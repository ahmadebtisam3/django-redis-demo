# Redis with django
in this small demo we use redis to store ip of
all the users who send request above than the define number of request in a mint and finnaly
we block those ips from accessing our site . All of this logic is implemented in demo apps
middleware

## deployment
```bash
    sudo apt install docker.io
    sudo docker run -itp 6379:6379 --name run_reds redis 
    python -m venv django_install
    source ./django_install/bin/active
    pip install django
    pip install redis
    git clone https://github.com/ahmadebtisam3/django-redis-demo.git
    cd redisApp
    python manage.py runserver
```