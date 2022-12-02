![example workflow](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-7/actions/workflows/build.yaml/badge.svg)

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9334112&assignment_repo_type=AssignmentRepo)
# Containerized App Exercise
## Introduction
This web application translates a person's facial expression into words. The user would be able to view their emotion history and receive a random text depending on their latest emotion. We serve to support and journal your emotions!

## SetUp
1. Our machine-learning-client requires camera access. Check to see if your computer's camera is fully functional.
2. Flask login is used for access, thus in order to access the functionalities of the app, an account must be created after running the project.

## Run the Project
1. At the root folder of the project run using the command
```
docker compose up
```

## Run Tests
- The app consist of two separate test groups (web-app and the machine-learning-client)
1. At the folder of either web-app or machine-learning-client run the command
```
python -m pytest
```
## Authors
- Brandon Chen: [Github]()
- Adam Sidibe: [Github]()
- Alexander Chen: [Github]()
- Wuji Cao: [Github]()
- John Kolibachuk: [Github]()
- Seok Tae Kim: [Github](https://github.com/seoktaekim)