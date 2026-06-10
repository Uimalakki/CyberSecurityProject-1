### Repo for MOOC course Cybersecurity project 1 assigment 
#### Construct a software with security flaws 

Setting up: 

Clone the repository to your local computer.

Create virtual environment and install dependencies:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install pip
$ python3 -m pip install -r requirements.txt
```

To initialize the database and populate it with some demo data, run commands: 
```
python manage.py migrate
python manage.py seed_data
````

The script creates two default users, both of whom are assigned the same weak password. The weak password is used to demonstrate a vulnerability in a brute force attack in flaw 5.
```
username: john 
password: password49
```
```
username: maureen 
password: password49
```

Start the server:
```
python manage.py runserver
```



