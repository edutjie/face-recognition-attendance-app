<h1>Face Recognition Attendance App</h1>
<h3>This is a CS50 Final Project</h3>
<h4>Tools:</h4>
<table style="border: 1px solid">
  <tr>
    <td>OpenCV</td>
    <td>Pillow</td>
    <td>SQtdte3</td>
    <td>Numpy</td>
    <td>tkinter</td>
    <td>werkzeug.security</td>
  </tr>
</table>
<h4>Description:</h4>
This is a Python-based Face Recognition Attendance application that was made using OpenCV. The use of this application is to record user attendance after being verified by the Face Recognition Log in feature.

<h4>Features:</h4>
<ul>
  <li><b>UI</b></li>
  This app uses tkinter library from python for its front-end UI.
  <br>
  <img src="https://user-images.githubusercontent.com/69960893/147261567-dbb59e53-5a03-4305-96db-9b635c8ce141.png" />
  <li><b>Sign Up</b></li>
  Ask username and password from user and validates it. After that, it will insert user's username and password to the database (the password will be hashed first using the werkzeug.security generate_password_hash) and take 200 pictures of the user and train it behind the screen, it will produce <i>face-train.xml</i>.
  <br>
  <img src="https://user-images.githubusercontent.com/69960893/147261560-356aa568-ca59-4d3c-8363-514b6050cc1e.png" />
  <li><b>Log In</b></li>
  Check if the username exists and the password is correct. Scan user face and if the user face recognized, it will redirect user to the logged in page.
  <br>
  <img src="https://user-images.githubusercontent.com/69960893/147261563-ce2ba4e8-3267-45ed-9aa1-d93a23891859.png" />
  <li><b>Select Cam</b></li>
  The user will have the ability to change the camera that will be used for the face recognition in the main menu, the default value of the camera is 0 (usually the default camera).
  <br>
  <img src="https://user-images.githubusercontent.com/69960893/147261557-0e84fdd2-03ec-4e61-85b6-318f17c77a84.png" />
  <li><b>Database</b></li>
  This app uses SQLite3 as its database.
  <li><b>Logged In</b></li>
  In the logged in page, the user will be able to submit attendance (the user attendance will be inserted in the SQLite3 table) and see the attendance list which consists all the attendance record.
  <br>
  <table>
    <tr>
      <td><img src="https://user-images.githubusercontent.com/69960893/147261552-9f005fcd-9f78-4ef3-b816-8b33e9f687f7.png" /></td>
      <td><img src="https://user-images.githubusercontent.com/69960893/147261574-d6af863d-40c3-47bc-ae75-af98af362626.png" /></td>
    </tr>
  </table>
</ul>

<h4>How it Works:</h4>
<ul>
  <li>Using the OpenCV library we can access our camera using VideoCapture and do something with it.</li>
  <li>This program uses haarcascade_frontalface_default cascade from OpenCV to detect faces in the VideoCapture.</li>
  <li>First we select the region of interest of the face and we can do things with it such as save it, scan it, etc.</li>
  <li>To train the faces, first we have to save the region of interest in our local directory (I set it to <i>images/[username]/</i>) and then <i>train.py</i> will train it using OpenCV LBPHFaceRecognizer and then export it to xml file (mine <i>face-train.xml</i>).</li>
  <li>To scan the face, we have to read the <i>face-train.xml</i> file and then predict the region of interest with it. Using the LBPHFaceRecognizer prediction we can get the confidence of the prediction.</li>
  <li>Confidence is the percentage we can get to tell that the face is recognized or not.</li>
  <img src="https://user-images.githubusercontent.com/69960893/147265224-aec2f66e-e5c5-4e62-b853-c0dacdc7b804.png" style="width:400px" />
</ul>

<h4>Files:</h4>
<ul>
  <li><i>cascades</i> (folder): collection of the OpenCV cascades</li>
  <li><i>images</i> (folder): will be automaticly created to store user's face png for the training process</li>
  <li><i>src</i> (folder): contain the source code</li>
  <ul>
    <li><i>main.py</i> (file): the main application (OPEN THIS)</li>
    <li><i>face.py</i> (file): store the functions to scan face and take pictures</li>
    <li><i>train.py</i> (file): Store the function to train the face</li>
  </ul>
  <li><i>face-train.xml</i> (file): will be automaticly created that contains the face training data</li>
  <li><i>face.db</i> (file): a database file that contain the SQLite3 tables that stores all the user and attendance data needed in the application</li>
</ul>

<h4>How to run and use the app?</h4>
<ol>
  <li>Run <code>python -m pip install -r requirements.txt</code> to install prerequisites.</li>
  <li>Go inside the src directory and open main.py or run <code>python src/main.py</code>.</li>
  <li>If you don't have an account yet, register by clicking the Sign Up button and fill the form and it will register your face also.</li>
  <li>Log in, fill the log in form. After that, the app will scan your face.</li>
  <li>After you've logged in, you can submit attendance or see the attendance list.</li>
  <li>Note: If your camera is blank or black, you can change your camera by clicking the Select Cam in the main menu and select the available camera.</li>
</ol>
