![example workflow](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-7/actions/workflows/build.yaml/badge.svg)

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9334112&assignment_repo_type=AssignmentRepo)

# Containerized App Exercise

## Introduction

This web application translates a person's facial expression into words. The user would be able to view their emotion history and receive a random text depending on their latest emotion. We serve to support and journal your emotions!

## SetUp

1. Our machine-learning-client requires camera access. Check to see if your computer's camera is fully functional.
2. Flask login is used for access, thus in order to access the functionalities of the app, an account must be created after running the project.

## Run the Project

1. The current port that the containers use for the app is 5000. Verify that no other app is running on that port before running the project.
2. At the root folder of the project run using the command `docker compose up`
3. Head to [localhost](http://127.0.0.1:5000/) to register as a new user
4. At the root folder of the project run the machine learning client using `python machine-learning-client/emotion_recog.py`
5. provide the username you used to register on the webapp and make sure your face is visible to your device's camera
6. Return to [localhost](http://127.0.0.1:5000/) and login using your account

## Run the Project Without Containers
1. Move to the `web-app` folder using `cd` command
2. Run using the command
```
flask run
```

## Run Tests

- The app consist of two separate test groups (web-app and the machine-learning-client)
- At the root of the project run the commands

```(python)
python -m pytest web-app/tests
python -m pytest machine-learning-client/tests

```

## Authors

- Brandon Chen: [Github](https://github.com/b-chen00)
- Adam Sidibe: [Github]()
- Alexander Chen: [Github]()
- Wuji Cao: [Github]()
- John Kolibachuk: [Github](https://github.com/jkolib)
- Seok Tae Kim: [Github](https://github.com/seoktaekim)
