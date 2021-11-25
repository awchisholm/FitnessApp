##############################
#           Imports          #
##############################
import base64
from guizero import App, Window, Text, PushButton, TextBox, info, Box, ButtonGroup, Picture, CheckBox, ListBox
import os
import os.path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
#####################
#     Constants     #
#####################
# constants that are defined at the start of the program.
temp3 = 0
count = 0
count2 = 0
database_file = "FitnessApp.db"
global_image_location = 'matplotlib_images/'
image_location = f'{global_image_location}TrackingSteps.png'
image_location2 = f'{global_image_location}TrackingWeight.png'
image_location3 = f'{global_image_location}GroupTracking.png'

#####################################
#           Signout Button          #
#####################################
# signout button if the user wants to sign out of their account.
def SignOut():
    # emptys the textboxes on login and signup
    textbox1.value = ""
    textbox2.value = ""
    textbox3.value = ""
    textbox4.value = ""
    textbox5.value = ""
    textbox6.value = ""
    textbox7.value = ""
    textbox8.value = ""
    textbox9.value = ""
    # unchecks checkbox for terms and conditions
    checkbox1.value = 0
    LoginPage.hide()
    SignupPage.hide()
    FitnessAppHomePage.hide()
    FitnessAppEatingPage.hide()
    FitnessAppWorkoutPage.hide()
    SubscriptionsPage1.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.hide()
    FitnessAppWorkoutPage.hide()
    WorkoutCreationPage.hide()
    app.show()

################################
#           Dark Mode          #
################################

def DarkMode():
    # creates a dark theme for users with bad eyesight or too bright for them
    FitnessAppHomePage.bg = "#808080"
    FitnessAppEatingPage.bg = "#808080"
    FitnessAppWorkoutPage.bg = "#808080"
    SubscriptionsPage1.bg = "#808080"
    SubscriptionsPage2.bg = "#808080"
    TrackingPage.bg = "#808080"
    GroupPage.bg = "#808080"
    FitnessAppWorkoutPage.bg = "#808080"
    WorkoutCreationPage.bg = "#808080"
    app.bg = "#808080"
    LoginPage.bg = "#808080"
    SignupPage.bg = "#808080"

#################################
#           Light Mode          #
#################################

def LightMode():
    # lighter theme for users with eyesight that means they cant look at a dark screen.
    FitnessAppHomePage.bg = "#F4F4F4"
    FitnessAppEatingPage.bg = "#F4F4F4"
    FitnessAppWorkoutPage.bg = "#F4F4F4"
    SubscriptionsPage1.bg = "#F4F4F4"
    SubscriptionsPage2.bg = "#F4F4F4"
    TrackingPage.bg = "#F4F4F4"
    GroupPage.bg = "#F4F4F4"
    FitnessAppWorkoutPage.bg = "#F4F4F4"
    WorkoutCreationPage.bg = "#F4F4F4"
    app.bg = "#F4F4F4"
    LoginPage.bg = "#F4F4F4"
    SignupPage.bg = "#F4F4F4"

###############################################
#           Procedures and Functions          #
###############################################

def EncryptPassword(Password):
    # encrypts the password
    Encrypted_Password = base64.b64encode(Password.encode("utf-8"))
    print(Encrypted_Password)
    # converts encrypted password from binary to a string
    String_Encrypted_Password = Encrypted_Password.decode("utf-8")
    print(String_Encrypted_Password)
    return String_Encrypted_Password

def DecryptPassword(Password):
    # makes read in string into a binary number to be decrypted
    Encrypted_Password = Password.encode("utf-8")
    print(Encrypted_Password)
    # decrypts it.
    Decrypted_Password = base64.b64decode(Encrypted_Password.decode("utf-8"))
    print(Decrypted_Password)
    # makes it a string from binary
    String_Decrypted_Password = Decrypted_Password.decode("utf-8")
    print(String_Decrypted_Password)
    return String_Decrypted_Password

# replaces the images that are already there with the new ones that have just been created.
def ReplaceImages():
    image1.value = image_location
    image2.value = image_location2
# inputting the weight and steps on the tracking page.
def InputWeightAndSteps():
    global temp3
    global NewUserID
    # global possible userids
    # hides the boxes that were just created.
    InputsBox.visible = False
    InputButton.visible = False
    # grabs todays date and formats it as DD/MM/YYYY
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%Y")
    # valdiation of the textboxes.
    if Steps_TextBox.value == "":
        info("Error", "Enter Your Weight and Steps in KG and Meters")
    elif Weight_TextBox.value == "":
        info("Error", "Enter Your Weight and Steps in KG and Meters")
    # taking the answers
    steps = str(Steps_TextBox.value)
    weight = str(Weight_TextBox.value)
    # grab userid
    # if userid temp3 = 0 then that means they have signed up to the system and not logged in. this is because in the login button function temp3 gets defined. so if not defined then must be the other userid variable "NewUserID"
    if temp3 == 0:
        # inserts the tracking info they just entered to the database then creates 2 graphs and replaces the old ones
        # this happens only once but depending on how you logged in it will be diffrent userid names.
        print(NewUserID)
        InsertDataSQL = ("INSERT INTO Tracking(DateAdded, Weight, Steps, UserID) VALUES ('"+ str(formatted_now)  + "', '" + str(weight) + "','"+ str(steps) + "','"+ str(NewUserID)+ "')")
        Insert_Data(database_file, InsertDataSQL)
        ShowGraphs()
        ReplaceImages()
    else:
        print(temp3)
        InsertDataSQL = ("INSERT INTO Tracking(DateAdded, Weight, Steps, UserID) VALUES ('"+ str(formatted_now)  + "', '" + str(weight) + "','"+ str(steps) + "','"+ str(temp3)+ "')")
        Insert_Data(database_file, InsertDataSQL)
        # creates 2 graphs and puts them in 2 seperate locations
        ShowGraphs()
        # replaces whatever image was in there with the 2 new ones.
        ReplaceImages()


def InputsBoxShow():
    # shows input boxes when you want to enter the info.
    InputsBox.visible = True
    InputButton.visible = True

def RefreshGroupChart():
    # refreshes the group chart with new image
    Graph1.value = image_location3

def GroupGraph():
    #connects to the database
    conn = sqlite3.connect('FitnessApp.db')
    c= conn.cursor()
    # grab formatted date and then query for names and todays date and plot bar graph
    now = datetime.now()
    formatted_now = now.strftime("%d/%m/%Y")
    c.execute("SELECT Forename, Steps FROM User_Table, Tracking WHERE Tracking.UserID = User_Table.UserID AND DateAdded = '"+ str(formatted_now) +"' ")
    # create pandas dataframe for the info.
    df = pd.DataFrame(c.fetchall(), columns = ['Name', 'Steps'])
    print(df)
    # plots a bar graph with correct labels.
    plt.bar(df['Name'], df['Steps'].astype(int))  
    plt.xlabel('Name')
    plt.ylabel('Steps')
    plt.title('Tracking Groups Steps')
    plt.savefig(image_location3)
    plt.close(1)
    plt.show()
    RefreshGroupChart()

######################################
#           Plotting Graphs          #
######################################

def ShowGraphs():
    conn = sqlite3.connect('FitnessApp.db')
    c= conn.cursor()

    c.execute("SELECT DateAdded, Steps FROM Tracking WHERE UserID = '"+ str(temp3) + "'")
    df = pd.DataFrame(c.fetchall(), columns = ['Date', 'Steps'])
    print(df)
    # plots a graph with correct labels.
    plt.plot(df['Date'], df['Steps'].astype(int))  
    plt.xlabel('Date')
    plt.ylabel('Steps')
    plt.title('Tracking Steps')
    # saves them to the location image_location
    plt.savefig(image_location)
    plt.close(1)
    plt.show()

    conn = sqlite3.connect('FitnessApp.db')
    c= conn.cursor()

    c.execute("SELECT DateAdded, Weight FROM Tracking WHERE UserID = '"+ str(temp3) + "'")
    df = pd.DataFrame(c.fetchall(), columns = ['Date', 'Weight'])
    print(df)
    # plots a graph with correct labels.
    plt.plot(df['Date'], df['Weight'].astype(int))  
    plt.xlabel('Date')
    plt.ylabel('Weight')
    plt.title('Tracking Weight')
    # saves them to the location image_location2
    plt.savefig(image_location2)
    plt.close(1)
    plt.show()

# put in df
#plot
# save image
# get inserts to work
 
###############################################
#           Diffrent Custom Workouts          #
###############################################
def MStrongWorkout():
    #creates Male Strong Workout
    text = Text(Title_Box, text = "  Male Strong Workout Routine                                                                                                                                                                         ", grid=[0,0], align="left", size=20)
    WorkoutImage1 = Picture(Workouts_Box, image= "1_Running.gif", grid=[0,0])
    WorkoutImage2 = Picture(Workouts_Box, image= "2_Forward_Lunge.gif", grid=[1,0])
    WorkoutImage3 = Picture(Workouts_Box, image= "3_Backward_Lunge.gif", grid=[2,0])
    WorkoutImage4 = Picture(Workouts_Box, image= "4_Jump.gif", grid=[3,0])
    WorkoutImage5 = Picture(Workouts_Box, image= "5_Burpee.gif", grid=[0,2])
    WorkoutImage6 = Picture(Workouts_Box, image= "6_Pushup.gif", grid=[1,2])
    WorkoutImage7 = Picture(Workouts_Box, image= "7_Abworkout.gif", grid=[2,2])
    WorkoutImage8 = Picture(Workouts_Box, image= "8_ButtBridge.gif", grid=[3,2])
    text = Text(Workouts_Box, text= "30 Seconds - High Stepping", grid=[0,1], size=15)
    text = Text(Workouts_Box, text= "15 Forward Lunges", grid=[1,1], size=15)
    text = Text(Workouts_Box, text= "15 Backwards Lunges", grid=[2,1], size=15)
    text = Text(Workouts_Box, text= "30 Seconds - Jumping", grid=[3,1], size=15)
    text = Text(Workouts_Box, text= "15 Burpees", grid=[0,3], size=15)
    text = Text(Workouts_Box, text= "15 Pushups", grid=[1,3], size=15)
    text = Text(Workouts_Box, text= "15 Abdominal Crunches", grid=[2,3], size=15)
    text = Text(Workouts_Box, text= "15 Butt Bridges", grid=[3,3], size=15)

def MLeanWorkout():
    #creates Male Lean Workout
    text = Text(Title_Box, text = "  Male Lean Workout Routine                                                                                                                                                                         ", grid=[0,0], align="left", size=20)
    WorkoutImage1 = Picture(Workouts_Box, image= "1_Running.gif", grid=[0,0])
    WorkoutImage2 = Picture(Workouts_Box, image= "4_Jump.gif", grid=[1,0])
    WorkoutImage3 = Picture(Workouts_Box, image= "6_Pushup.gif", grid=[2,0])
    WorkoutImage4 = Picture(Workouts_Box, image= "5_Burpee.gif", grid=[3,0])
    WorkoutImage5 = Picture(Workouts_Box, image= "2_Forward_Lunge.gif", grid=[0,2])
    WorkoutImage6 = Picture(Workouts_Box, image= "3_Backward_Lunge.gif", grid=[1,2])
    WorkoutImage7 = Picture(Workouts_Box, image= "7_Abworkout.gif", grid=[2,2])
    WorkoutImage8 = Picture(Workouts_Box, image= "10_LegsUp.gif", grid=[3,2])
    text = Text(Workouts_Box, text= "30 Seconds - High Stepping", grid=[0,1], size=15)
    text = Text(Workouts_Box, text= "30 Seconds - Jumping", grid=[1,1], size=15)
    text = Text(Workouts_Box, text= "15 Pushups", grid=[2,1], size=15)
    text = Text(Workouts_Box, text= "15 Burpees", grid=[3,1], size=15)
    text = Text(Workouts_Box, text= "15 Forward Lunges", grid=[0,3], size=15)
    text = Text(Workouts_Box, text= "15 Backwards Lunges", grid=[1,3], size=15)
    text = Text(Workouts_Box, text= "15 Abdominal Crunches", grid=[2,3], size=15)
    text = Text(Workouts_Box, text= "15 Leg Ups", grid=[3,3], size=15)

def MSkinnyWorkout():
    #creates Male Skinny Workout
    text = Text(Title_Box, text = "  Male Skinny Workout Routine                                                                                                                                                                         ", grid=[0,0], align="left", size=20)
    WorkoutImage1 = Picture(Workouts_Box, image= "10_LegsUp.gif", grid=[0,0])
    WorkoutImage2 = Picture(Workouts_Box, image= "7_Abworkout.gif", grid=[1,0])
    WorkoutImage3 = Picture(Workouts_Box, image= "8_ButtBridge.gif", grid=[2,0])
    WorkoutImage4 = Picture(Workouts_Box, image= "5_Burpee.gif", grid=[3,0])
    WorkoutImage5 = Picture(Workouts_Box, image= "6_Pushup.gif", grid=[0,2])
    WorkoutImage6 = Picture(Workouts_Box, image= "4_Jump.gif", grid=[1,2])
    WorkoutImage7 = Picture(Workouts_Box, image= "1_Running.gif", grid=[2,2])
    WorkoutImage8 = Picture(Workouts_Box, image= "3_Backward_Lunge.gif", grid=[3,2])
    text = Text(Workouts_Box, text= "15 Leg Ups", grid=[0,1], size=15)
    text = Text(Workouts_Box, text= "15 Abdominal Crunches", grid=[1,1], size=15)
    text = Text(Workouts_Box, text= "15 Butt Bridges", grid=[2,1], size=15)
    text = Text(Workouts_Box, text= "15 Burpees", grid=[3,1], size=15)
    text = Text(Workouts_Box, text= "15 Pushups", grid=[0,3], size=15)
    text = Text(Workouts_Box, text= "30 Seconds - Jumping", grid=[1,3], size=15)
    text = Text(Workouts_Box, text= "30 Seconds - High Stepping", grid=[2,3], size=15)
    text = Text(Workouts_Box, text= "15 Backwards Lunges", grid=[3,3], size=15)

def FStrongWorkout():
    #creates Female Strong Workout
    text = Text(Title_Box, text = "  Female Strong Workout Routine                                                                                                                                                                         ", grid=[0,0], align="left", size=20)
    WorkoutImage1 = Picture(Workouts_Box, image= "Woman_Forward_Lunge.gif", grid=[0,0])
    WorkoutImage2 = Picture(Workouts_Box, image= "Woman_One_Legged_Squat.gif", grid=[1,0])
    WorkoutImage3 = Picture(Workouts_Box, image= "Woman_Hip_Workout.gif", grid=[2,0])
    WorkoutImage4 = Picture(Workouts_Box, image= "Woman_MountainClimber.gif", grid=[3,0])
    WorkoutImage5 = Picture(Workouts_Box, image= "Woman_Abdominal_Crunches.gif", grid=[0,2])
    WorkoutImage6 = Picture(Workouts_Box, image= "Woman_Dumbell_Lifts.gif", grid=[1,2])
    WorkoutImage7 = Picture(Workouts_Box, image= "Woman_Hammers.gif", grid=[2,2])
    WorkoutImage8 = Picture(Workouts_Box, image= "Woman_Wall_Pushups.gif", grid=[3,2])
    text = Text(Workouts_Box, text= "15 Forward Lunges", grid=[0,1], size=15)
    text = Text(Workouts_Box, text= "15 One-Leg Squats", grid=[1,1], size=15)
    text = Text(Workouts_Box, text= "15 Side Hip Raise", grid=[2,1], size=15)
    text = Text(Workouts_Box, text= "30 Seconds - Mountain Climber", grid=[3,1], size=15)
    text = Text(Workouts_Box, text= "15 Abdominal Crunches", grid=[0,3], size=15)
    text = Text(Workouts_Box, text= "15 Dumbell Lifts", grid=[1,3], size=15)
    text = Text(Workouts_Box, text= "15 Hammer Lifts", grid=[2,3], size=15)
    text = Text(Workouts_Box, text= "15 Wall Pushups", grid=[3,3], size=15)

def FLeanWorkout():
    #creates Female Lean Workout
    text = Text(Title_Box, text = "  Female Lean Workout Routine                                                                                                                                                                         ", grid=[0,0], align="left", size=20)
    WorkoutImage1 = Picture(Workouts_Box, image= "Woman_MountainClimber.gif", grid=[0,0])
    WorkoutImage2 = Picture(Workouts_Box, image= "Woman_Abdominal_Crunches.gif", grid=[1,0])
    WorkoutImage3 = Picture(Workouts_Box, image= "Woman_Wall_Pushups.gif", grid=[2,0])
    WorkoutImage4 = Picture(Workouts_Box, image= "Woman_Hip_Workout.gif", grid=[3,0])
    WorkoutImage5 = Picture(Workouts_Box, image= "Woman_One_Legged_Squat.gif", grid=[0,2])
    WorkoutImage6 = Picture(Workouts_Box, image= "Woman_Forward_Lunge.gif", grid=[1,2])
    WorkoutImage7 = Picture(Workouts_Box, image= "Woman_Dumbell_Lifts.gif", grid=[2,2])
    WorkoutImage8 = Picture(Workouts_Box, image= "Woman_Hammers.gif", grid=[3,2])
    text = Text(Workouts_Box, text= "30 Seconds - Mountain Climber", grid=[0,1], size=15)
    text = Text(Workouts_Box, text= "15 Abdominal Crunches", grid=[1,1], size=15)
    text = Text(Workouts_Box, text= "15 Wall Pushups", grid=[2,1], size=15)
    text = Text(Workouts_Box, text= "15 Side Hip Raise", grid=[3,1], size=15)
    text = Text(Workouts_Box, text= "15 One-Leg Squats", grid=[0,3], size=15)
    text = Text(Workouts_Box, text= "15 Forward Lunges", grid=[1,3], size=15)
    text = Text(Workouts_Box, text= "15 Dumbell Lifts", grid=[2,3], size=15)
    text = Text(Workouts_Box, text= "15 Hammer Lifts", grid=[3,3], size=15)

def FSkinnyWorkout():
    #creates Female Skinny Workout
    text = Text(Title_Box, text = "  Female Skinny Workout Routine                                                                                                                                                                         ", grid=[0,0], align="left", size=20)
    WorkoutImage1 = Picture(Workouts_Box, image= "Woman_Dumbell_Lifts.gif", grid=[0,0])
    WorkoutImage2 = Picture(Workouts_Box, image= "Woman_Hammers.gif", grid=[1,0])
    WorkoutImage3 = Picture(Workouts_Box, image= "Woman_Wall_Pushups.gif", grid=[2,0])
    WorkoutImage4 = Picture(Workouts_Box, image= "Woman_Legsup.gif", grid=[3,0])
    WorkoutImage5 = Picture(Workouts_Box, image= "Woman_Abdominal_Crunches.gif", grid=[0,2])
    WorkoutImage6 = Picture(Workouts_Box, image= "Woman_MountainClimber.gif", grid=[1,2])
    WorkoutImage7 = Picture(Workouts_Box, image= "Woman_Hip_Workout.gif", grid=[2,2])
    WorkoutImage8 = Picture(Workouts_Box, image= "Woman_One_Legged_Squat.gif", grid=[3,2])
    text = Text(Workouts_Box, text= "15 Dumbell Lifts", grid=[0,1], size=15)
    text = Text(Workouts_Box, text= "15 Hammer Lifts", grid=[1,1], size=15)
    text = Text(Workouts_Box, text= "15 Wall Pushups", grid=[2,1], size=15)
    text = Text(Workouts_Box, text= "15 Leg Lifts", grid=[3,1], size=15)
    text = Text(Workouts_Box, text= "15 Abdominal Crunches", grid=[0,3], size=15)
    text = Text(Workouts_Box, text= "30 Seconds - Mountain Climber", grid=[1,3], size=15)
    text = Text(Workouts_Box, text= "15 Side Hip Raise", grid=[2,3], size=15)
    text = Text(Workouts_Box, text= "15 One-Leg Squats", grid=[3,3], size=15)
###############################################
#           Login Navigation Buttons          #
###############################################

def LoginPageNavigation():
    # closes login/signup and takes you to login page
    app.hide()
    LoginPage.show()

def SignupPageNavigation():
    # closes login/signup and takes you to signup page
    app.hide()
    SignupPage.show()

def LoginBackButtonNavigation():
    # goes back to login/signup
    LoginPage.hide()
    app.show()

def SignupBackButtonNavigation():
    # goes back to login/signup
    SignupPage.hide()
    app.show()

#####################################
#          Navigation Bar           #
#####################################

def HomePageNavigation():
    # Home Navigation
    FitnessAppEatingPage.hide()
    FitnessAppWorkoutPage.hide()
    WorkoutCreationPage.hide()
    SubscriptionsPage1.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.hide()
    FitnessAppHomePage.show()

def EatingPageNavigation():
    # Healthy Eating Navigation
    FitnessAppHomePage.hide()
    FitnessAppWorkoutPage.hide()
    WorkoutCreationPage.hide()
    SubscriptionsPage1.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.hide()
    FitnessAppEatingPage.show()

def WorkoutPageNavigation():
    # Workout Plan Navigation
    FitnessAppHomePage.hide()
    FitnessAppEatingPage.hide()
    WorkoutCreationPage.hide()
    SubscriptionsPage1.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.hide()
    FitnessAppWorkoutPage.show()

def WorkoutCreationNavigation():
    # Workout Creation Navigation
    FitnessAppHomePage.hide()
    FitnessAppEatingPage.hide()
    FitnessAppWorkoutPage.hide()
    SubscriptionsPage1.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.hide()
    FitnessAppWorkoutPage.hide()
    WorkoutCreationPage.show()

def SubscriptionPageNavigation():
    # Subscriptions Navigation
    global TempUserID
    global temp3
    global NewUserID
    if temp3 == 0:
        # comes here if user has just signed in rather than logged in, diffrent textbox names diffrent query to grab userid.
        query = ("SELECT * from Subscriptions WHERE UserID = '"+ str(NewUserID) + "'")
    else:
        query = ("SELECT * from Subscriptions WHERE UserID = '"+ str(temp3) + "'")
    # grab userid
    # row of details for the person logged in.
    row1 = query_database(database_file, query)
    SubActive = row1[0][1]
    SubBought = str(row1[0][2])
    SubExpires = str(row1[0][3])
    # if they do have a subscription
    if SubActive == "True":
        textbox = PushButton(DetailsBox, grid=[1,0], text = "£14.99/Year ", align="left", enabled=False, width=15)
        textbox.text_size=20
        Sometext1 = PushButton(DetailsBox, grid=[1,1], text = "Active Subscription", align="left", enabled=False, width=15)
        Sometext1.text_size=20
        Sometext2 = PushButton(DetailsBox, grid=[1,2], text = SubBought, align="left", enabled=False, width=15)
        Sometext2.text_size=20
        Sometext3 = PushButton(DetailsBox, grid=[1,3], text = SubExpires, align="left", enabled=False, width=15)
        Sometext3.text_size=20
        Sometext4 = PushButton(DetailsBox, grid=[1,4], text="VISA ******", align="left", enabled=False, width=15)
        Sometext4.text_size=20
        FitnessAppHomePage.hide()
        FitnessAppEatingPage.hide()
        FitnessAppWorkoutPage.hide()
        SubscriptionsPage2.hide()
        TrackingPage.hide()
        GroupPage.hide()
        FitnessAppWorkoutPage.hide()
        WorkoutCreationPage.hide()
        SubscriptionsPage1.show()
    else:
        # if they do not have a subscription
        textbox = PushButton(DetailsBox1, grid=[1,0], text = "£14.99/Year ", align="left", enabled=False, width=15)
        textbox.text_size=20
        Sometext1 = PushButton(DetailsBox1, grid=[1,1], text = "Free", align="left", enabled=False, width=15)
        Sometext1.text_size=20
        Sometext2 = PushButton(DetailsBox1, grid=[1,2], text = "N/A", align="left", enabled=False, width=15)
        Sometext2.text_size=20
        Sometext3 = PushButton(DetailsBox1, grid=[1,3], text = "N/A", align="left", enabled=False, width=15)
        Sometext3.text_size=20
        Buy_Button = PushButton(DetailsBox1, grid=[1,4], text="VISA ******54", align="left", enabled=False, width=15)
        Buy_Button.text_size=20
        FitnessAppHomePage.hide()
        FitnessAppEatingPage.hide()
        FitnessAppWorkoutPage.hide()
        SubscriptionsPage1.hide()
        TrackingPage.hide()
        GroupPage.hide()
        FitnessAppWorkoutPage.hide()
        WorkoutCreationPage.hide()
        SubscriptionsPage2.show()

def TrackingPageNavigation():
    # Tracking Navigation
    FitnessAppHomePage.hide()
    FitnessAppEatingPage.hide()
    FitnessAppWorkoutPage.hide()
    SubscriptionsPage1.hide()
    GroupPage.hide()
    FitnessAppWorkoutPage.hide()
    WorkoutCreationPage.hide()
    SubscriptionsPage2.hide()
    TrackingPage.show()
    ShowGraphs()
    ReplaceImages()

def GroupPageNavigation():
    # Group Navigation
    FitnessAppHomePage.hide()
    FitnessAppEatingPage.hide()
    FitnessAppWorkoutPage.hide()
    SubscriptionsPage1.hide()
    FitnessAppWorkoutPage.hide()
    WorkoutCreationPage.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.show()
    GroupGraph()


################################
#     Create Workout Button    #
################################

def Create_Workout_Button():
    # alot of decitions here depends on the workout creation images you get.
    # gathers the answers.
    string1 = Answer1.value
    string2 = Answer2.value
    string3 = Answer3.value
    string4 = Answer4.value
    print(string1, string2, string3, string4)
    if Answer1.value == "":
        info("Error!","You must enter all boxes")
    elif Answer2.value == "":
        info("Error!","You must enter all boxes")
    elif Answer3.value == "":
        info("Error!","You must enter all boxes")
    elif Answer4.value == "":
        info("Error!","You must enter all boxes")
        #closes all the pages after validating the boxes are all filled.
    FitnessAppEatingPage.hide()
    FitnessAppWorkoutPage.hide()
    SubscriptionsPage1.hide()
    SubscriptionsPage2.hide()
    TrackingPage.hide()
    GroupPage.hide()
    FitnessAppHomePage.hide()
    #calcualtes bmi
    BMI = float(Answer4.value) ** 2
    BMI = float(Answer3.value) / BMI
    # users choice of workout gets created and called depending on what they choose.
    if Answer1.value == "Male":
        if Answer2.value == "Strong":
            # calls that window to get populated with data.
            MStrongWorkout()
        elif Answer2.value == "Lean":
            # calls that window to get populated with data.
            MLeanWorkout()
        else:
            # calls that window to get populated with data.
            MSkinnyWorkout()
    else:
        if Answer2.value == "Strong":
            # calls that window to get populated with data.
            FStrongWorkout()
        elif Answer2.value == "Lean":
            # calls that window to get populated with data.
            FLeanWorkout()
        else:
            # calls that window to get populated with data.
            FSkinnyWorkout()
    # BMI to 2 decimal places.
    temp1 = str("%.2f" % BMI)
    print(temp1)
    text1 = Text(Title_Box, text = temp1, grid=[2,0], align= "right", size=20)
    # puts it in the top left corner
    #shows the workout page after populating it with data
    WorkoutCreationPage.show()


#############################
#     Check Subscription    #
#############################

def CheckSubscription(userid):
    # checks to see if the user has a subscription, takes the logged in users id and does an SQL query to grab if they have a subscription or not.
    query = ("SELECT * from Subscriptions WHERE UserID = '"+ str(userid) + "'")
    print(query)
    row1 = query_database(database_file, query)
    # if they dont have one then disable the workout button on navigation
    if row1[0][1] == "False":
        WorkoutButton1.disable()
        WorkoutButton2.disable()
        WorkoutButton3.disable()
        WorkoutButton4.disable()
        WorkoutButton5.disable()
        WorkoutButton6.disable()
        WorkoutButton7.disable()
        WorkoutButton8.disable()
    
###########################
#      Login Button       #
###########################

def LoginButton():
    # done button procedure for checking whether or not the person is in the database or not.
    global row
    global temp3
    # validation for if null
    if textbox1.value =="":
        info("Error!", "You must enter a Username!")
    elif textbox2.value == "":
        info("Error!", "You must enter a Password!")
    else:
        # sql for selecting the username and password the user entered and search for it in the database
      #  query = ("SELECT * from User_Table WHERE Username = "+ "'"+ str(textbox1.value) + "'"+ " AND Password = "+ "'" + str(textbox2.value) + "'")
        query = ("SELECT * from User_Table WHERE Username = "+ "'"+ str(textbox1.value) + "'")
        print(query)
        # gets that row 
        # preventing sql injection by seperating the username and password from each other and read the password directly and check if it is the same as the password
        Inputed_Password = textbox2.value
        EncryptedPassword1 = EncryptPassword(Inputed_Password)
        try:
            row = query_database(database_file, query)
        except sqlite3.Error:
            info("Error", "Dont do that again")
        if len(row) == 0:
            info("Error!", "Your details are not in our database! Try again.")
        elif EncryptedPassword1 == row[0][2]:
                temp3 = str(row[0][0])
                CheckSubscription(temp3)
                FitnessAppHomePage.show()
                LoginPage.hide()
                # prevents anything that isnt the password they have.
        else: 
                info("Error","Dont do that again :(")


############################
#      Signup Button       #
############################

def SignupButton():
    #gloabals the Userid that they just get given 
    global NewUserID
    global String_Encrypt_Password
    # validation on signing up
    if textbox3.value == "":
        info("Error!", "You must enter a Username!")
    elif len(textbox3.value) <= 3:
        info("Error!", "Username must be larger than 3 characters!")
    elif len(textbox3.value) >= 15:
        info("Error!", "Username too large must be below 15 characters!")
    elif textbox4.value == "":
        info("Error!", "You must enter a Firstname!")
    elif textbox5.value == "":
        info("Error!", "You must enter a Surname!")
    elif textbox6.value == "":
        info("Error!", "You must enter a Email!")
    elif "@" and "." not in textbox6.value:
        info("Error!", "'Email' must have @ and a '.'!")
    elif textbox7.value == "":
        info("Error!", "You must enter a Date of Birth!")
    elif "/" not in textbox7.value:
        info("Error!", "'Date of birth must be in this format DD/MM/YYYY!")
    elif textbox8.value == "":
        info("Error!", "You must enter a Password!")
    elif len(textbox8.value) <= 3:
        info("Error!", "Password must be larger than 3 characters!")
    elif len(textbox8.value) >= 12:
        info("Error!", "Password too large must be below 12 characters!")
    elif checkbox1.value == 0:
        info("Error!", "In order to contine you have to accept the terms and conditions.")
    elif textbox8.value == textbox9.value:
        #insert the data into the database
        # encrypt the password.
        String_Password = textbox9.value
        String_Encrypt_Password = EncryptPassword(String_Password)
        DecryptPassword(String_Encrypt_Password)
        InsertSQL = ("INSERT INTO User_Table(Username, Password, Forename, Surname, Email, DateOfBirth, GroupID) VALUES ('"+ str(textbox3.value) + "','" + String_Encrypt_Password + "','" + str(textbox4.value) + "','" + str(textbox5.value) + "','" + str(textbox6.value) + "','" + str(textbox7.value)+ "', 1)")
        print(InsertSQL)
        Insert_Data(database_file, InsertSQL)
        # because the account was just created, there will be a brand new userid assigned to the database so this function will grab the new made userid 
        NewUserID = signup_verification()
        # if they chose not to buy a subscription then it will add this data to the persons subscriptions table

        if buttongroup1.value == "No":
            SubInsertSQL = ("INSERT INTO Subscriptions(SubscriptionActive, SubscriptionStart, SubscriptionEnd, UserID) VALUES ('False', 'N/A','N/A','"+ str(NewUserID)+ "')")
            Insert_Data(database_file, SubInsertSQL)
            # inserts the data and disables workout page as a paid for product.
            FitnessAppHomePage.show()
            WorkoutButton1.disable()
            WorkoutButton2.disable()
            WorkoutButton3.disable()
            WorkoutButton4.disable()
            WorkoutButton5.disable()
            WorkoutButton6.disable()
            WorkoutButton7.disable()
            WorkoutButton8.disable()
            SignupPage.hide()
        else:
            # if they chose to get a subscription :
            # grabs todays date and formats it DD/MM/YYYY
            now = datetime.now()
            formatted_now = now.strftime("%d/%m/%Y")
            # grabs 365 days or a year abd adds it to the date today and this makes a year from now.
            # now this is used to grab the expire date of the subscription
            year1 = timedelta(days = 365)
            AYearFromNow = now + year1
            AYearFromNow = AYearFromNow.strftime("%d/%m/%Y")
            print(AYearFromNow)
            # inserts to database the new data
            SubInsertSQL = ("INSERT INTO Subscriptions(SubscriptionActive, SubscriptionStart, SubscriptionEnd, UserID) VALUES ('True', '"+ str(formatted_now) + "','"+ str(AYearFromNow) + "','"+ str(NewUserID)+ "')")
            Insert_Data(database_file, SubInsertSQL)
            # navigates to the home page
            FitnessAppHomePage.show()
            SignupPage.hide()
    else:
        # if password != to confirm password then it will output an error.
        info("Sorry!","You need to enter your in password the same time twice!")

###########################
#   Grabs New UserID      #
###########################
# grabs the new user id.
def signup_verification():
    global row
    global String_Encrypt_Password
    print("dog")
    # sql for selecting where username and password are to get the row
    query = ("SELECT * from User_Table WHERE Username = "+ "'"+ str(textbox3.value) + "'"+ " AND Password = "+ "'" + String_Encrypt_Password + "'")
    print(query)
    row = query_database(database_file, query)
    # does the exact same as in the function done_dutton() by checking it found a row
    if len(row) == 0:
        info("Error!", "Your details are not in our database! Try again.")
    else:
        # opens the notes page and closes down windows no longer in use.
        temp3 = str(row[0][0])
        return temp3

###############################################
#                Database Setup               #
#                                             #
#           Delete Existing Database          #
###############################################
# This function deletes a database.
# It's just a file so all it does it 
#  delete the file
def delete_database(database_file):
    if os.path.exists(database_file):
        os.remove(database_file)
#######################################################
#              Executing SQL in a File                #
#######################################################
def init_db(database_file, database_sql):   
    # open the sqlite database file
    conn = sqlite3.connect(database_file)
    # connect to it and get a cursor
    # this is like a placeholder in the database
    cursor = conn.cursor()                  
    # open the script file containing SQL
    script = open(database_sql, 'r')
    # read the contents of the script 
    # into a string called sql
    sql = script.read()                     
    # execute the SQL 
    cursor.executescript(sql)               
    # commit the changes to make them permanent
    conn.commit()                           
    # close the connection to the database
    conn.close() 

#############################################
#              Executing SQL                #
#############################################
def Insert_Data(database_file, sql):   
    # open the sqlite database file
    conn = sqlite3.connect(database_file)
    # connect to it and get a cursor
    # this is like a placeholder in the database
    cursor = conn.cursor()                  
    cursor.executescript(sql)               
    # commit the changes to make them permanent
    conn.commit()                           
    # close the connection to the database
    conn.close() 
########################################
#          Query the Database          #
########################################
# this peice of code connected to the database file i have in my files
# it then creates a variable to hold all the data and uses cursor function
# it then excecutes the sql code its give and returns all the rows that it found
def query_database(database, query):
    # this is used to pass a query and then it will fetchall rows found and then return this value
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    cur.close()
    return rows

#############################################
#                                           #
#              MAIN PROGRAMME               # 
#                                           #
#############################################

#####################################
#         Login/Signup Page         #
#####################################
# creates the app / window
app = App(title = "Login / Signup Page", layout="auto")
#
app.after(1800000, SignOut)
# on all of these i am making it full screen for the user expeirence.
app.set_full_screen()
textblank = Text(app, text=" ")
text = Text(app, text="Please Login or", size=15)
text2 = Text(app, text="Create an Account", size=15)
textblank = Text(app, text=" ")
box = Box(app, align="top", width="fill")
# contains commands in the buttons so that when it is clicked a command function will happen this is event driven coding.
Login_button = PushButton(box, text="Login", command=LoginPageNavigation, width=20)
Signup_button = PushButton(box, text="Sign Up", command=SignupPageNavigation, width=20)

##############################
#         Login Page         #
##############################
# Create Login Page
LoginPage = Window(app, title="Login Page")
LoginPage.set_full_screen()
textblank = Text(app, text=" ")
box2 = Box(LoginPage, width="fill")
LoginPage.hide()
# Widgets in box2
textblank = Text(box2, text=" ")
text = Text(box2, text="Enter your login:", width="fill", height= "fill", size=15)
textblank = Text(box2,  width="fill", height= "fill", text=" ")
text2 = Text(box2, text="Username: ",  width="fill", height= "fill")
textbox1 = TextBox(box2, hide_text=False,width=30, height= "fill")
text3 = Text(box2, text="Password: ",   width="fill", height= "fill")
textbox2 = TextBox(box2, hide_text=True, width=30, height= "fill")
textblank = Text(box2,  width="fill", height= "fill", text=" ")
# Buttons on Login Page
textblank = Text(LoginPage, text=" ")
Login_button = PushButton(LoginPage, text="Login", command=LoginButton, width=10)
Back_button = PushButton(LoginPage, text="Back", command=LoginBackButtonNavigation, width=10)

###############################
#         Signup Page         #
###############################
SignupPage = Window(app, title="Signup Page")
SignupPage.set_full_screen()
SignupPage.hide()
textblank = Text(SignupPage, text=" ")
text = Text(SignupPage, text="    Please enter details:  ", size=15)
textblank = Text(SignupPage, text=" ")
box3 = Box(SignupPage, layout="grid")
# Widgets for Signup Page 
# Username text and textbox
textblank = Text(box3, text="               ", grid=[1,0])
text1 = Text(box3, text="Username:", align = "left", grid=[0,0])
textbox3 = TextBox(box3, hide_text=False, align="left", grid=[2,0], width=20)
# Forename text and textbox
textblank = Text(box3, text="                       ", grid=[1,1])
text2 = Text(box3, text="Forename:", align = "left", grid=[0,1])
textbox4 = TextBox(box3, hide_text=False, width=20, height= "fill", grid=[2,1])
# Surname text and textbox
textblank = Text(box3, text="                       ", grid=[1,2])
text3 = Text(box3, text="Surname: ",   align = "left", grid=[0,2])
textbox5 = TextBox(box3, hide_text=False, width=20, height= "fill", grid=[2,2])
# Email text and textbox
textblank = Text(box3, text="                       ", grid=[1,3])
text4 = Text(box3, text="Email: ",    align = "left", grid=[0,3])
textbox6 = TextBox(box3, hide_text=False, width=20, height= "fill",grid=[2,3])
# Date of Birth text and textbox
textblank = Text(box3, text="                       ", grid=[1,4])
text5 = Text(box3, text="Date of Birth: ",   align = "left", grid=[0,4])
textbox7 = TextBox(box3, hide_text=False, width=20, height= "fill",grid=[2,4])
# Password text and textbox
textblank = Text(box3, text="                       ", grid=[1,5])
text6 = Text(box3, text="Password: ",    align = "left", grid=[0,5])
textbox8 = TextBox(box3, hide_text=True, width=20, height= "fill",grid=[2,5])
# Confirm Password text and textbox
textblank = Text(box3, text="                       ", grid=[1,6])
text7 = Text(box3, text="Confirm Password: ",    align = "left", grid=[0,6])
textbox9 = TextBox(box3, hide_text=True, width=20, height= "fill",grid=[2,6])
# Buy a subscription? option
textblank = Text(SignupPage, text="                       ")
text8 = Text(SignupPage, text="Would you like to buy a subscription for £14.99? ")
buttongroup1 = ButtonGroup(SignupPage, options=["Yes","No"])
# Accept Terms and Conditions
textblank = Text(SignupPage, text="                       ")
checkbox1 = CheckBox(SignupPage, text=" Please Accept the Terms and Conditions if you wish to continue")
# Buttons for Signup Page
textblank = Text(SignupPage, text="                       ")
Signup_button = PushButton(SignupPage, text="Signup", command=SignupButton, width=15)
close_button = PushButton(SignupPage, text="Back", command=SignupBackButtonNavigation, width=15)

#########################################
#         Fitness App Home Page         #
#########################################
# home page for fintess app
FitnessAppHomePage = Window(app, title="Fitness App Home Page")
FitnessAppHomePage.set_full_screen()
FitnessAppHomePage.hide()
textblank = Text(FitnessAppHomePage, text= " ")
text = Text(FitnessAppHomePage, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(FitnessAppHomePage, text= " ")
# creates a box to put all the navigation buttons in.
box1 = Box(FitnessAppHomePage, layout = "grid", border=True)
# buttons
HomeButton = PushButton(box1, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(box1, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton1 = PushButton(box1, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(box1, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(box1, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(box1, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(box1, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(box1, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(box1, text="Sign out", grid=[8,0], width=27, command=SignOut)

textblank = Text(FitnessAppHomePage, text= " ")
# creates info for user to see and read.
# uses boxes to split up the page.
box4 = Box(FitnessAppHomePage, layout = "grid", border=False, width="fill")
ParagraphBox1 = Box(box4, grid=[0,1], border=False, align="left", width=1100, height=90)
ParagraphBox2 = Box(box4, grid=[0,3], border=False, align="left", width=1100, height=200)
ParagraphBox3 = Box(box4, grid=[0,5], border=False, align="left", width=1100, height=200)
PictureBox1 = Box(box4, grid=[1,1], border=False, align="left", layout="grid")
PictureBox2 = Box(box4, grid=[1,3], border=False, align="left", layout="grid")
PictureBox3 = Box(box4, grid=[1,5], border=False, align="left", layout="grid")
text = Text(box4, text="  Fitness Training", size=20, grid=[0,0], align="left")
text = Text(ParagraphBox1, text="Fitness training balances five elements of good health. Make sure your routine includes aerobic\nfitness, strength training, core exercises, balance training, and flexibility and stretching.", size=16, align="left")
text = Text(PictureBox1, text="                                            ", grid=[0,0])
text = Text(box4, text="  Aerobic fitness", size=20, grid=[0,2], align="left")
text = Text(ParagraphBox2, text="Aerobic activity, also known as cardio or endurance activity, is the cornerstone of most fitness training programs.\nAerobic activity or exercise causes you to breathe faster and more deeply, which maximizes the amount of oxygen\nin your blood. Your heart will beat faster, which increases blood flow to your muscles and back to your lungs.\n\nThe better your aerobic fitness, the more efficiently your heart, lungs and blood vessels transport oxygen throughout\nyour body — and the easier it is to complete routine physical tasks and rise to unexpected challenges, such as\nrunning to your car in the pouring rain.", size=16, align="left")
text = Text(box4, text="  Strength training", size=20, grid=[0,4], align="left")
text = Text(PictureBox2, text="                                            ", grid=[0,0])
Image2 = Picture(PictureBox2, image="StrengthTraining.png", grid=[1,0], width = 300, height = 300)
text = Text(ParagraphBox3, text="Muscular fitness is another key component of a fitness training program. Strength training can help you increase\nbone strength and muscular fitness, and it can help you manage or lose weight. It can also improve your ability to\ndo everyday activities. Aim to include strength training of all the major muscle groups into your fitness routine at\nleast twice a week.\n\nMost fitness centres offer various resistance machines, free weights and other tools for strength training. But you\ndon't need to invest in a gym membership or expensive equipment to reap the benefits of strength training.", size=16, align="left")
text = Text(PictureBox3, text="                                            ", grid=[0,0])
Image3 = Picture(PictureBox3, image="Cardio.png", grid=[1,0], width = 400, height = 300)
###################################################
#         Fitness App Healthy Eating Page         #
###################################################
FitnessAppEatingPage = Window(app, title="Fitness App Healthy Eating Page")
FitnessAppEatingPage.set_full_screen()
FitnessAppEatingPage.hide()
textblank = Text(FitnessAppEatingPage, text= " ")
text = Text(FitnessAppEatingPage, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(FitnessAppEatingPage, text= " ")
NavigationBox = Box(FitnessAppEatingPage, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton2 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(FitnessAppEatingPage, text= " ")
# title and paragraph boxes 
box4 = Box(FitnessAppEatingPage, layout = "grid", border=False, width="fill")
TitleBox = Box(box4, border=False, width="fill", grid=[0,0])
ParagraphBox1 = Box(box4, border=False, width="fill", grid=[0,1])
PictureBox1 = Box(box4, border=False, width="fill", grid=[1,1])
text = Text(TitleBox, text="  Healthy Eating", size=20, align="left")
text = text = Text(ParagraphBox1, text="\nEating a healthy diet is not about strict limitations, staying unrealistically thin, or depriving yourself\nof the foods you love. Rather, it’s about feeling great, having more energy, improving your health,\nand boosting your mood.\n\nHealthy eating doesn’t have to be overly complicated. If you feel overwhelmed by all the conflicting\nnutrition and diet advice out there, you’re not alone. It seems that for every expert who tells you a\ncertain food is good for you, you’ll find another saying exactly the opposite. The truth is that while\nsome specific foods or nutrients have been shown to have a beneficial effect on mood, it’s your\noverall dietary pattern that is most important. The cornerstone of a healthy diet should be to replace\nprocessed food with real food whenever possible. Eating food that is as close as possible to the\nway nature made it can make a huge difference to the way you think, look, and feel.\n\n\nThe Fundamentals of Healthy Eating\n\nWhile some extreme diets may suggest otherwise, we all need a balance of protein, fat,\ncarbohydrates, fiber, vitamins, and minerals in our diets to sustain a healthy body. You don’t need to\neliminate certain categories of food from your diet, but rather select the healthiest options from\neach category.\n\nProtein gives you the energy to get up and go—and keep going—while also supporting mood and\ncognitive function. Too much protein can be harmful to people with kidney disease, but the latest\nresearch suggests that many of us need more high-quality protein, especially as we age. That\ndoesn’t mean you have to eat more animal products—a variety of plant-based sources of protein\neach day can ensure your body gets all the essential protein it needs.\n\nFat. Not all fat is the same. While bad fats can wreck your diet and increase your risk of certain\ndiseases, good fats protect your brain and heart. In fact, healthy fats—such as omega-3s—are vital\nto your physical and emotional health. Including more healthy fat in your diet can help improve your\nmood, boost your well-being, and even trim your waistline.", size=16, align="left")
textblank = Text(ParagraphBox1, text= " ")
textblank = Text(PictureBox1, text= "                                      ", align="left")
Image = Picture(PictureBox1, image="HeathyEating.png")
box6 = Box(box4, border=False, width="fill", grid=[1,0])
#################################################
#         Fitness App Workout Plan Page         #
#################################################
FitnessAppWorkoutPage = Window(app, title="Fitness App Workout Page")
FitnessAppWorkoutPage.set_full_screen()
FitnessAppWorkoutPage.hide()
textblank = Text(FitnessAppWorkoutPage, text= " ")
text = Text(FitnessAppWorkoutPage, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(FitnessAppWorkoutPage, text= " ")
NavigationBox = Box(FitnessAppWorkoutPage, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton3 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(FitnessAppWorkoutPage, text= "  ")
# title and paragraph boxes 
Title_and_Paragraph_Box = Box(FitnessAppWorkoutPage, layout="grid", border=False)
Title = Text(Title_and_Paragraph_Box, text="  Workout Plan", grid=[0,0], size=20)
BlankText = Text(Title_and_Paragraph_Box, text=" ", grid=[0,1])
Paragraph = Text(Title_and_Paragraph_Box, text="In order to create a customized workout plan specifically for you,please answer a few questions so we can get to know you and create a custom workout for you.", size=16, grid=[0,2])
blanktext = Text(FitnessAppWorkoutPage, text="    ")
blanktext = Text(FitnessAppWorkoutPage, text="    ")
QuestionsBox = Box(FitnessAppWorkoutPage, layout="grid", border=False)
Question1 = Box(QuestionsBox, grid=[1,0], border=False, width="fill")
Question2 = Box(QuestionsBox, grid=[0,0], border=False, width="fill")
Question3 = Box(QuestionsBox, grid=[0,1], border=False, width="fill")
Question4 = Box(QuestionsBox, grid=[1,1], border=False, width="fill")
text1 = Text(Question1, text="What gender are you?", size=20)
blanktext = Text(Question1, text="    ")
Answer1 = ButtonGroup(Question1, options=["Male", "Female"])
blanktext = Text(Question1, text="    ")
text2 = Text(Question2, text="What kind of body type?", size=20)
blanktext = Text(Question2, text="    ")
Answer2 = ButtonGroup(Question2, options=["Strong", "Lean", "Skinny"])
text3 = Text(Question3, text="Weight in kg:", size=20)
blanktext = Text(Question3, text="    ")
blanktext = Text(Question3, text="    ")
Answer3 = TextBox(Question3, text=" ")
text4 = Text(Question4, text="Height in meters:", size=20)
blanktext = Text(Question4, text="    ")
blanktext = Text(Question4, text="    ")
Answer4 = TextBox(Question4, text=" ")
blanktext = Text(FitnessAppWorkoutPage, text="    ")
Create_Workout_Button = PushButton(FitnessAppWorkoutPage, text="Create Workout", command=Create_Workout_Button)



#####################################################
#         Fitness App Workout Creation Page         #
#####################################################
WorkoutCreationPage = Window(app, title="Fitness App Workout Creation Page")
WorkoutCreationPage.set_full_screen()
WorkoutCreationPage.hide()
textblank = Text(WorkoutCreationPage, text= " ")
text = Text(WorkoutCreationPage, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(WorkoutCreationPage, text= " ")
NavigationBox = Box(WorkoutCreationPage, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton4 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(WorkoutCreationPage, text= " ")
# title and paragraph boxes 
Title_Box = Box(WorkoutCreationPage, layout="grid", width="fill", border=False)
text1 = Text(Title_Box, text = "BMI:", grid=[1,0], align= "right", size=20)
textblank = Text(Title_Box, text = " ", grid = [0,1], size=20)

Workouts_Box =  Box(WorkoutCreationPage, layout="grid", width="fill", border=False)

#####################################################
#         Fitness App Subscriptions Page 1          #
#####################################################
SubscriptionsPage1 = Window(app, title="Fitness App Subscription Details Page")
SubscriptionsPage1.set_full_screen()
SubscriptionsPage1.hide()
textblank = Text(SubscriptionsPage1, text= " ")
text = Text(SubscriptionsPage1, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(SubscriptionsPage1, text= " ")
NavigationBox = Box(SubscriptionsPage1, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton5 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(SubscriptionsPage1, text= " ")
# title and paragraph boxes 
Title_and_Paragraph_Box = Box(SubscriptionsPage1, layout="grid", width="fill", border=False)
text = Text(Title_and_Paragraph_Box, text = " Subscription Details", grid=[0,0], align="left", size=20)
textblank = Text(Title_and_Paragraph_Box, text="  ", grid=[0,1])
text = Text(Title_and_Paragraph_Box, text = "  Here are all the sybscription details, because you have a subscription all your details should appear here:", grid=[0,2], align="left", size=16)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,3])
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,4])
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,5])
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,6])
DetailsBox_and_PictureBox = Box(SubscriptionsPage1, layout="grid", border=False)
DetailsBox = Box(DetailsBox_and_PictureBox, grid=[0,0], layout="grid", border=False)
text = Text(DetailsBox, grid=[0,0], text = "Subscription Price: ", size=30)
text1 = Text(DetailsBox, grid=[0,1], text = "Subscription Status: ", size=30)
text = Text(DetailsBox, grid=[0,2], text = "Subscription Bought: ", size=30)
text = Text(DetailsBox, grid=[0,3], text = "Subscription Expires: ", size=30)
text = Text(DetailsBox, grid=[0,4], text = "Payment Method: ", size=30)
textbox = PushButton(DetailsBox, grid=[1,0], text = "£14.99/Month ", enabled=False, width=15)
textbox.text_size=20
Buy_Button = PushButton(DetailsBox, grid=[1,4], text="VISA ******412", enabled=False, width=15)
Buy_Button.text_size=20
PictureBox = Box(DetailsBox_and_PictureBox, grid=[1,0], border=False)
image1 = Picture(PictureBox, image="SubPicture.png", height=400, width=500)
#####################################################
#         Fitness App Subscriptions Page 2          #
#####################################################
SubscriptionsPage2 = Window(app, title="Fitness App Subscription Details Page")
SubscriptionsPage2.set_full_screen()
SubscriptionsPage2.hide()
textblank = Text(SubscriptionsPage2, text= " ")
text = Text(SubscriptionsPage2, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(SubscriptionsPage2, text= " ")
NavigationBox = Box(SubscriptionsPage2, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton6 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(SubscriptionsPage2, text= " ")
# title and paragraph boxes 
Title_and_Paragraph_Box = Box(SubscriptionsPage2, layout="grid", width="fill", border=False)
text = Text(Title_and_Paragraph_Box, text = " Subscription Details", grid=[0,0], align = "left", size=20)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,1])
text = Text(Title_and_Paragraph_Box, text = "  Here are all the sybscription details, because you dont have a subscription you will not have payment method and exire date", grid=[0,2], align="left", size=16)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,3])
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,4])
DetailsBox_and_PictureBox1 = Box(SubscriptionsPage2, layout="grid", border=False)
DetailsBox1 = Box(DetailsBox_and_PictureBox1, grid=[0,0], layout="grid", border=False)
text = Text(DetailsBox1, grid=[0,0], text = "Subscription Price: ", size=30)
text1 = Text(DetailsBox1, grid=[0,1], text = "Subscription Status: ", size=30)
text = Text(DetailsBox1, grid=[0,2], text = "Subscription Bought: ", size=30)
text = Text(DetailsBox1, grid=[0,3], text = "Subscription Expires: ", size=30)
text = Text(DetailsBox1, grid=[0,4], text = "Purchase Subscription: ", size=30)
textbox = PushButton(DetailsBox1, grid=[1,0], text = "£14.99/Month ", enabled=False, width=15)
textbox.text_size=20
Sometext1 = PushButton(DetailsBox1, grid=[1,1], text = "Free Plan", enabled=False, width=15)
Sometext1.text_size=20
Sometext2 = PushButton(DetailsBox1, grid=[1,2], text = "N/A",  enabled=False, width=15)
Sometext2.text_size=20
Sometext3 = PushButton(DetailsBox1, grid=[1,3], text = "N/A", enabled=False, width=15)
Sometext3.text_size=20
Buy_Button = PushButton(DetailsBox1, grid=[1,4], text="Buy", enabled=False, width=15)
Buy_Button.text_size=20
PictureBox = Box(DetailsBox_and_PictureBox1, grid=[1,0], border=False)
image1 = Picture(PictureBox, image="SubPicture.png", height=400, width=500)
#####################################################
#             Fitness App Tracking Page             #
#####################################################
TrackingPage = Window(app, title="Fitness App Tracking Page")
TrackingPage.set_full_screen()
TrackingPage.hide()
textblank = Text(TrackingPage, text= " ")
text = Text(TrackingPage, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(TrackingPage, text= " ")
NavigationBox = Box(TrackingPage, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton7 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(TrackingPage, text= " ")
# title and paragraph boxes 
Title_and_Paragraph_Box = Box(TrackingPage, layout="grid", width="fill", border=False)
text = Text(Title_and_Paragraph_Box, text = "  Tracking Information", grid=[0,0], align="left", size=20)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,1])
text = Text(Title_and_Paragraph_Box, text = "Here is all the tracking information you have collected so far, if you wish to add some data please use the buttons\n under the graphs this page will show youyour weight progress over time and your overall step count overtime.", grid=[0,2], align="left", size=16)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,3])
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,4])

Graph_and_Buttons_Box = Box(TrackingPage, layout="grid", border=False)
GraphBox1 = Box(Graph_and_Buttons_Box, grid=[0,0], border=False)
GraphBox2 = Box(Graph_and_Buttons_Box, grid=[1,0], border=False)
ButtonBox1 = Box(Graph_and_Buttons_Box, grid=[0,1], border=False)
image1 = Picture(GraphBox1, image="therock.gif", height=400, width=500)
image2 = Picture(GraphBox2, image="therock.gif", height=400, width=500)
textblank = Text(TrackingPage, text=" ")
Weigh_In = PushButton(TrackingPage, text="Enter Info", width=20, command=InputsBoxShow)
Weigh_In.text_size = 15
InputsBox = Box(TrackingPage, layout="grid", border=True, visible=False)
Weight_Text = Text(InputsBox, grid=[0,0], text="Weight: ")
Weight_TextBox = TextBox(InputsBox, grid=[1,0])
Steps_Text = Text(InputsBox, grid=[0,1], text="Steps: ")
Steps_TextBox = TextBox(InputsBox, grid=[1,1])

InputButton = PushButton(TrackingPage, text="Done", command=InputWeightAndSteps, visible=False)
#####################################################
#               Fitness App Group Page              #
#####################################################
GroupPage = Window(app, title="Fitness App Group Page")
GroupPage.set_full_screen()
GroupPage.hide()
textblank = Text(GroupPage, text= " ")
text = Text(GroupPage, text="ToKa Fitness App", size=30, font="Times New Roman")
textblank = Text(GroupPage, text= " ")
NavigationBox = Box(GroupPage, layout = "grid", border=True)
# creates a box to put all the navigation buttons in.
HomeButton = PushButton(NavigationBox, text="Home",  grid=[0,0], width=26, command=HomePageNavigation)
HealthyEatingPage = PushButton(NavigationBox, text="Healthy Eating", grid=[1,0], width=26, command=EatingPageNavigation)
WorkoutButton8 = PushButton(NavigationBox, text="Workout", grid=[2,0], width=26, command=WorkoutPageNavigation)
SubscriptionsButton = PushButton(NavigationBox, text="Subscriptions", grid=[3,0], width=26, command=SubscriptionPageNavigation)
TrackingButton = PushButton(NavigationBox, text="Tracking Progress", grid=[4,0], width=26, command=TrackingPageNavigation)
GroupButton = PushButton(NavigationBox, text="Group Progress", grid=[5,0], width=27, command=GroupPageNavigation)
DarkModeButton = PushButton(NavigationBox, text="Dark Mode", grid=[6,0], width=27, command=DarkMode)
LightModeButton = PushButton(NavigationBox, text="Light Mode", grid=[7,0], width=27, command=LightMode)
SignOut_Button = PushButton(NavigationBox, text="Sign out", grid=[8,0], width=27, command=SignOut)
textblank = Text(GroupPage, text= " ")
# title and paragraph boxes 
Title_and_Paragraph_Box = Box(GroupPage, layout="grid", width="fill", border=False)
text = Text(Title_and_Paragraph_Box, text = "  Group T Level Students", grid=[0,0], align="left", size=20)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,1])
text = Text(Title_and_Paragraph_Box, text = "   The Groups Daily Goal: 10,000 steps a day", grid=[0,2], align="left", size=16)
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,3])
textblank = Text(Title_and_Paragraph_Box, text="", grid=[0,4])
# creates box for graph and participents list
Graph_and_ListBox_Box = Box(GroupPage, layout="grid", border=False)
PeopleInGroup = ListBox(Graph_and_ListBox_Box, grid=[0,0], items=["- Jack Mitchell", "- Marlon Evans", "- Tom Wells", "- Will Williams", "- Ash Gilbert", "- Chloe Knowles", "- Joe Harper"], enabled=False)
PeopleInGroup.text_size = 15
PictureBox = Box(Graph_and_ListBox_Box, grid=[1,0], border=False)
Graph1 = Picture(PictureBox, image="therock.gif", width=500, height=400) 
textblank = Text(Graph_and_ListBox_Box, text="                                                             ", size=20, grid=[0,1])
########################################
#         Calling the Database         #
########################################
# this bit of code called the functions that delete the existing database named FitnessApp, and then create a brand new one using DDL and DML sql in files and by calling these functions
delete_database(database_file)
init_db(database_file, "CreateDatabase.sql") # this is the SQL Data Definition Language to create the database
init_db(database_file, "DummyData.sql")      # this is the SQL Data Manipulation Language to insert dummy data

app.display()
