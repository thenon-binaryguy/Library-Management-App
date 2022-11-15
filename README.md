# Library Management Application
Library Management Application Created for Loopr AI Recruitment

Website is hosted at :

> https://loopr-library-app.herokuapp.com/books

## Overview

This Web Application is a prototype for a Library Management system. It consists of a Dashboard that displays books ,genre wise. The books can be added or removed after the user has logged in. The app uses JWT tokens to authorize the user and , only after the user is logged in , additional functionalitites such as issue/return of books ,Viewing your profile , Editing your profile details and Addtional /Removal of books . 

## Tech Stack Used 

1. Python 3.7
2. FASTAPI framework (for backend)
3. PostgresSQL (database)
4. HTML , CSS and Javascript (for frontend)
5. Bootstrap CSS ( to make frontend better)


## How to Run the app ?

1. Clone the repository to your local storage
2. Navigate to the file and make it your root ( Recommended to use a code editor such as VS Code )
3. Create a virtual Environment on system (Optional But recommended , to avoid messing package versions)

[ If virtual environment is not installed , use `pip install virtualenv` ] 

`python -m venv <Environment name> (Eg. python -m venv env)`

4. Install all the packages using the given command. 

  ` pip install requirements.txt`

5. After the packages are installed , the last step is to start the uvicorn server to run the app

`uvicorn main:app --reload`
( Adding "reload" is recommended as it restarts the server everytime you make changes to your application )

6. The dashboard can be accessed using the following link :

> http://127.0.0.1:8000/books

7. Voila , U are ready to go !


## Screenshots 

1. Dashboard (./books)

![image](https://user-images.githubusercontent.com/68860153/201997090-cf8932ae-6317-431a-9f08-06d0b17b6308.png)

2.  Login / Signup Page (./login)

![image](https://user-images.githubusercontent.com/68860153/201997329-82776c80-ee08-479f-aae8-7f62559e724b.png)

3. Add new Books (./addbook)

![image](https://user-images.githubusercontent.com/68860153/201997537-b572c11c-dc61-4923-ac90-1aee9c8caf37.png)



