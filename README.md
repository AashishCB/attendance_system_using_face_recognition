Simple Attendance system using face recognition using opencv, python and flask.

To run this project
install anaconda
open cmd in that location
run the below command:

		$conda env create -f environment.yml
	

This will create a conda environment named 'attendance' with all necessary packages
Now to activate the environment, run the below command:

		$conda activate attendance


Then run the below command:

		$python app.py

now you will see link like 'http://127.0.0.1:5000/' or something like that, open the link in browser


The project has following functions
 collect sample for any student with their names
 recognize face and mark the present for that day