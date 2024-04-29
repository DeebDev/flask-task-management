# flask-task-management
Its a Task Management API using flask, Python, SQLAlchemy, and PostgreSQL

Setting Up the Application

1. Environment Setup:
    -  Ensure Python is installed on your system.
    -  Install PostgreSQL and create a database for your application.
    -  Install Flask and other dependencies by running pip install -r requirements.txt in your project directory.
  
2. Configure Environment Variables:
    -  Create a .env file in your project root directory.
    -  Add the following environment variables:

           DB_URI=postgresql://username:password@localhost/databasename
       
           SECRET_KEY=your_secret_key
       
           DB_NAME=databasename
       
           DB_USER=username
       
           DB_PASSWORD=password
       
           DB_HOST=localhost
       
           DB_PORT=5432
     -  Replace username, password, databasename, and your_secret_key with your actual PostgreSQL credentials and a secret key for Flask.

  3. Database Initialization:
     -  With Flask application context, run db.create_all() to create the database schema based on your models. This step is already included in your app.py file within the with app.app_context(): block.
    
Running the Application

       -  In your terminal, navigate to your project directory.
       -  Activate your virtual environment if you're using one.
       -  Run the application with flask run or python app.py (if you have the appropriate if __name__ == '__main__': block uncommented).
       -  Access the application in your web browser at http://127.0.0.1:5000/.
       -  Visit http://127.0.0.1:5000/admin to access the Flask-Admin interface.

Additional Notes


       - If you encounter database connection issues, verify your .env file's database credentials and ensure your PostgreSQL server is running.
       - For changes in your models, you might need to rerun db.create_all() or use a migration tool like Flask-Migrate for versioning your database schema.
       - Ensure your requirements.txt file is up to date with all the necessary packages.
