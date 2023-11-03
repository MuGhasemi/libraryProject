# libraryProject

Hello, this project named `libraryProject` has been designed and developed. It enables students to
rent books.

## Features

- Create, read, update, and delete (CRUD) operations for books
- User authentication system
- Efficient image management using the Pillow package
- User-friendly messages and notifications with the Sweetify package
- Conversion of dates from the Gregorian calendar to the solar calendar using the Django-Jalali-Date package

## Models

- Author: Represents an author of a book.
- Genre: Represents a genre or category of books.
- User: Represents a user of the application. It is used for user authentication and authorization.
- Book: Represents a book in the library. It contains information such as the title, author, genre, and availability status.
- BookInstance: Represents an instance of a specific book. It contains information about the book's status, due date, and borrower.

## Installation and Setup

1. Clone the project from the GitHub repository:

```
git clone https://github.com/MuGhasemi/libraryProject.git
```

2. Navigate to the project directory and activate the virtual environment:

```
cd Library
python -m venv venv
source venv/bin/activate
```

3. Install project dependencies:

```
pip install -r requirements.txt
```

4. Run the migrations:

```
python manage.py migrate
```

5. Start the development server:

```
python manage.py runserver
```

## Contributing

If you are interested in contributing to the project, feel free to share feedback, ideas, and bug reports through the Issues section and submit Pull Requests on GitHub.

## Contributors:

If you have any questions or requests, you can contact me:

- Backend Developer: [Muhammad Ghasemi](https://github.com/MuGhasemi)
- Frontend Developer: [Reza Mohammadzade](https://github.com/reza-sdo)













To start a Django project, you need to create a virtual environment first.
    You can do this by running the following command in your terminal:
    `python -m venv yourVenvName`

Replace "yourVenvName" with the name you want to give to your virtual environment.

Once your virtual environment is created, activate it by running:
    `yourVenvName\Scripts\activate`
To exit from yourVenvName, you can use the command `yourVenvName\Scripts\deactivate` in your terminal or command line.
    This will deactivate the virtual environment and return you to your normal system environment.

Now, you can install all the required packages for your project using the pip package manager. 
    To do this, navigate to the directory where your project is located and run the following command:
    `pip install -r requirements.txt`

Make sure that the "requirements.txt" file is present in the directory.
    This command will install all the packages listed in the file and make them available for use in your project.

After installing all the required packages, you can run your Django project using the `python manage.py runserver` command.
    To do this, navigate to the directory where your project is located and enter the above command in your terminal or command line.

Once the command is executed, the development server will start running at http://127.0.0.1:8000/.
    You can open this URL in your web browser to see the homepage of your Django project.

Contributors:
- Backend Developer: [Muhammad Ghasemi](https://github.com/MuGhasemi)
- Frontend Developer: [Reza Mohammadzade](https://github.com/reza-sdo)