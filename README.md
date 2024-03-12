# LinkedListing Project Setup Guide

Welcome to the LinkedListing project! This guide will walk you through the initial setup process after you've cloned the repository.

## Prerequisites

- Python installed on your system.
- Git installed on your system.
- Visual Studio Code (VS Code) or your preferred IDE installed.


## Clone the Repository

First, clone the repository to your local machine using Git:

When you open vscode and start a new project, click the clone button and paste the repo link

or, when in a new project enter the command below in your terminal

```bash
git clone <repository-url>
```

## Backend Setup

Navigate to the Backend directory within the cloned repository:

```bash
cd backend
```

Create and activate a Python virtual environment:
```bash
python -m venv venv

source venv/Scripts/activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```
Install requirements:
```bash
pip install -r requirements.txt
```


## Daily Tasks

Everytime you open the project in vscode make sure to go to the GIT tab at the left of VSCODE window and sync your project.

This will pull all the latest changes made by your teammates to your project on your pc.

After that make sure to activate the virtual environment again in the backend folder:

```bash
cd backend

source venv/Scripts/activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```
## Testing

To test the project simply run:

```bash
python unitTests.py
```











