# libraryProject

To start a Django project, you need to create a virtual environment first.
You can do this by running the following command in your terminal:
    `python -m venv yourVenvName`

Replace "yourVenvName" with the name you want to give to your virtual environment.

Once your virtual environment is created, activate it by running:
    `yourVenvName/Scripts/activate`

Now, you can install all the required packages for your project using the pip package manager. 
To do this, navigate to the directory where your project is located and run the following command:
    `pip install -r requirements.txt`

Make sure that the "requirements.txt" file is present in the directory. This command will install all the packages listed in the file and make them available for use in your project.

After installing all the required packages, you can run your Django project using the `python manage.py runserver` command. To do this, navigate to the directory where your project is located and enter the above command in your terminal or command line.

Once the command is executed, the development server will start running at http://127.0.0.1:8000/. You can open this URL in your web browser to see the homepage of your Django project.