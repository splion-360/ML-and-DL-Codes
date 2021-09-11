# Calorie Counter
##### A machine learning based and [heroku](https://www.heroku.com/) hosted calorie counter application which takes in certain parameters and gives an approximate measure of the total calories burnt after workout

#### Dataset:
The [fmendes-DAT263x-demos](https://www.kaggle.com/fmendes/fmendesdat263xdemos) dataset is used for this simple application. This dataset was created with the notion of establishing correlations between calories burnt, exercise duration and body type.


* Look at the [app](https://energy-calorie.herokuapp.com/) here 

#### App Interface 
The app interface is shown below
<p align="center">
  <img src="./Flask_app.png" width = "300" height = "200"/>
</p>

##### **Fields**:
* **_male_**:         Enter `1` if True or `0` if not
* ***female***:        Enter `1` if True or `0` if not
* ***age***:           Enter the age
* ***weight***:        Enter the weight in kilograms
* ***height***:        Enter the height in centimeters
* ***duration***:      Enter the duration of workout
* ***heartbeat***:     Enter the average heartbeat (bpm) during workout
* ***body_temp***:    Enter the body temperature in celcius

##### **Output**:
The output of the application is shown below

<p align="center">
  <img src="./Outcome_flask.png" width = "500" height = "250"/>
</p>
