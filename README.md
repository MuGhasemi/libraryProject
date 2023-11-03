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
cd libraryProject
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