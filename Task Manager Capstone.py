import datetime
from datetime import *
# reg_user — that is called when the user selects ‘r’ to register a user.
def reg_user(menu):
    if menu == "r":  # Setting if statement for menu.
        new_username = input("Please enter a new username: \n")
        # Checking if the username already exists in the usernames.
        # Whilst listed, the user is prompted to re-enter a new username and an error message is displayed.
        while new_username in usernames:
            print("The username you entered is already listed.")
            new_username = input("Please enter a new username: \n")
        # If the new username is not already listed, it is added to usernames.
        if new_username not in usernames:
            usernames.append(new_username)
            user_details["Usernames"] = usernames  # The updated list is then updated in the dictionary user_details.       
        new_password = input("Please enter a new password: \n")
        confirm_password = input("Please confirm your new password: \n")        
        # prompt user to enter their new password and confirm it until they match.
        while new_password != confirm_password:
            print("Incorrect Password.")
            new_password = input("Enter your new password: \n")
            confirm_password = input("Confirm your password: \n") 
            
        if new_password == confirm_password:
            print("Correct Password!")
            passwords.append(new_password)
            user_details["Passwords"] = passwords  # The updated list is updated in the dictionary user_details

            with open('user.txt', 'r+') as file:
                # The number of lines is equal to the number of items in usernames list.
                for i in range(len(usernames)):
                        file.write(user_details["Usernames"][i] + ", " + user_details["Passwords"][i] + '\n')
        return("New username and password successfully added.")


# add_task function that is called when a user selects ‘a’ to add a new task.
def add_task(menu):
    if menu == "a":
        task_username = input("Enter the username of the person you to assign the task to: \n") 
        task_title = input("Enter the title of the task: \n")
        task_description = input("Enter a description of the task: \n")
        # Using the previously imported datetime module today() function to calculate the current date.
        current_date = datetime.date.today()
        # Changing the date object to a string.
        assigned_date = current_date.strftime('%d %b %Y')
        date_format = input("Please enter the due date of the task (e.g. dd-mm-yyyy): \n")
        date_list = date_format.split("-")
        numbers_date = [int(x) for x in date_list]
        due_date = date(numbers_date[2], numbers_date[1], numbers_date[0]).strftime('%d %b %Y') 
        # set task completed to "No" when adding a new task. 
        completed = "No"
        task_list = [task_username, task_title, task_description, assigned_date, due_date, completed]
        tasks_dict[f"Task {count} details:"] = task_list    
        with open('task.txt', 'r+') as file2:
            # Printing the list values for each key in tasks_dict to a new line.
            for key in tasks_dict:
                line_string = str(tasks_dict[key])  # Casting to a string enabling the info to be written to the file.
                bad_chars = ["[", "]", "\'",]  
                for i in bad_chars: 
                    line_string = line_string.replace(i, "")
                file2.write(line_string + '\n')  # Writing the correct format of each string line to the file. 
        # Message returned at the end of the function. 
        return("New task added successfully.")

# view_all function that is called when users type ‘va’ to view all the tasks listed in ‘task.txt’.
def view_all(menu):
    if menu == "va":
        task_count = 0
        for key in tasks_dict:
            task_count += 1
            print(f"""
                Task {str(task_count)}:     {str(tasks_dict[key][1])}
                Assigned to:            {str(tasks_dict[key][0])}
                Date assigned:          {str(tasks_dict[key][3])}
                Due Date:               {str(tasks_dict[key][4])}
                Task Complete?          {str(tasks_dict[key][-1])}
                Task Description:       {str(tasks_dict[key][2])}""")
    return("Those are all the tasks!")

#  view_mine function that is called when users type ‘vm’ to view all the tasks that have been assigned to them.
def view_mine(menu, username):
    if menu == "vm":
        task_count = 0  # initializing number of tasks.
        for key in tasks_dict:
            task_count += 1  # calculating the total number of tasks by increasing the count through tasks dictionary. 
            if username == (tasks_dict[key][0]):  # If a task is already assigned to the user, it will be displayed.
                print(f"""
                Task {str(task_count)}:      \t{str(tasks_dict[key][1])}
                Assigned to:        {str(tasks_dict[key][0])}
                Date assigned:      {str(tasks_dict[key][3])}
                Due Date:           {str(tasks_dict[key][4])}
                Task Complete?      {str(tasks_dict[key][-1])}
                Task Description:   {str(tasks_dict[key][2])}""")

    # option for the user to either edit a task by or return to the main menu.
    task_selection = input("\nPlease select a a task by number to edit (e.g. 1, 2,3) or type -1 to return to the main menu. \n")
    if task_selection == "-1": 
        return(menu)        
    else:
       option = input("Do you want to mark the task as complete or edit the task? (type mark OR edit) \n")
       if option == "mark":
           # If they choose to mark, the item linked to that task for completion is changed to 'Yes' in tasks_dict.
           tasks_dict[f"Task {task_selection} details:"][5] = "Yes"
           return("Your task has been marked as complete.")
       # If they choose to edit, the task must be incomplete, item in dictionary list equal to 'No'.
       elif option == "edit" and (tasks_dict[f"Task {task_selection} details:"][5] == "No"):
           #They are given the option to edit username or due date.
           edit_choice = input("Would you like to edit the task username or due date? (Type 'U' or 'D') \n").lower()
           if edit_choice == "u":  # If they choose to edit the username, they are prompted to enter a new username for the task.
               name_edit = input("Please enter a new username for the task: \n")
               tasks_dict[f"Task {task_selection} details:"][0] = name_edit  # The new name is assigned in the dictionary.
               return("The task username has been updated successfully.")  # Successful return message.
           elif edit_choice == "d":  # If they choose to edit the due date, they are prompted to enter a new date. 
               due_date_change = input("Please enter a new due date (e.g. 25 June 2022) \n")
               tasks_dict[f"Task {task_selection} details:"][4] = due_date_change  # New date is updated in the tasks_dict.
               return("The due date has been updated successfully.")
       elif option == "edit" and (tasks_dict[f"Task {task_selection} details:"][5] == "Yes"):
           return("You can only edit tasks that are not already complete. \nChoose 'vm' from menu below to select another task to edit.")
           
            
# is_task_overdue function to compare dates and check whether or not the task is over due
# if current date is greater than the due date, then the task is over due. 
import datetime
def is_task_overdue(due_date):
    # convert the due date string to a datetime object
    due_date = datetime.datetime.strptime(due_date, '%d %b %Y').date()
    
    # get the current date
    current_date = datetime.date.today()
    
    # compare the two dates and return True if the task is overdue
    return current_date > due_date

#  generate reports function to generate reports to the main menu of the application.
def generate_reports():
    task_overview = ""  # Setting blank strings to store info in to be written to the generated text files.
    user_overview = ""
    tasks_total = len(tasks_dict)  # Total number of tasks is equal to the key count of tasks_dict.
    # Adding a string with the total tasks number to the tas_overview string. 
    task_overview = task_overview + f"Number of tasks generated and tracked by task_manager.py is {str(len(tasks_dict))}."
    x = 0  # Setting variables for integers concerning complete tasks, incomplete tasks and overdue tasks respectively.
    y = 0
    z = 0
        
    for key in tasks_dict:
        if tasks_dict[key][5] == "Yes":  # checking for which tasks are complete by finding the 'Yes' string in each key of tasks_dict.
            x += 1  # If the task is complete, x is increased by 1.     
        elif tasks_dict[key][5] == "No":  # checking for which tasks are complete by finding the 'No' string in each key of tasks_dict.
           y += 1  # If the task is complete, variable y is increased by 1. 
           if is_task_overdue(tasks_dict[key][4]):  # If the is_task_overdue function returns 'True', a task is overdue and incomplete.
               z += 1  # 'z' is increased by 1 to count the incomplete, overdue tasks.
            

    # All of the numbers calculated above are now built into sentences in the task_overview string.
    # Percentages are also calculated within the f-strings added, with the results being rounded to 2 decimal places and cast into strings into sentences.
    task_overview = task_overview + f"\nThe total number of completed tasks: {str(x)}." + f"\nThe total number of incomplete tasks is {str(y)}."
    task_overview = task_overview + f"\nThe total number of incomplete and overdue tasks: {str(z)}."
    task_overview = task_overview + f"\nThe percentage of incomplete tasks: {str(round((y / len(tasks_dict)) * 100, 2))}%."
    task_overview = task_overview + f"\nThe percentage of tasks that are overdue: {str(round((z / len(tasks_dict)) * 100, 2))}%."

    # The task_overview string is then written to the file in an easy to read format.
    with open('task_overview.txt', 'w') as file3:
        file3.write(task_overview)

    # initializing variables to store information regarding total users, complete tasks for a user, incomplete tasks for the user,
    a = 0
    b = 0
    c = 0
    d = 0
    for key in tasks_dict:

        if tasks_dict[key][0] == username:  # Counting the number of tasks assigned to the user by identifying the first list item.
            a += 1  # Integer 'a' is increased by 1 if the task is for the user.

        elif tasks_dict[key][0] == username and tasks_dict[key][5] == "Yes":  # Checking if the task for the user is complete.
           b += 1  # Integer 'b' is increased by 1 if the task is complete.     

        elif tasks_dict[key][0] == username and tasks_dict[key][5] == "No":  # Checking if the task for the user is incomplete.
            c += 1  # Integer 'c' is increased by 1 if the task is incomplete.  

            if is_task_overdue(tasks_dict[key][4]):  # Checking if the task is incomplete and overdue.
                d += 1  # If overdue, integer 'd' is increased by 1.
         
    # Writing all the info calculated above into sentence strings which are built into the user_overview string variable.
    user_overview = user_overview + f" Number of users registered with task_manager.py is {str(len(user_details))}."
    user_overview = user_overview + f"Number of tasks generated and tracked by task_manager.py is {str(len(tasks_dict))}."
    user_overview = user_overview + f"Number of tasks assigned to {username} is {str(a)}."
    user_overview = user_overview + f"Percentage of the total number of tasks assigned to {username} is {str(round((a / len(tasks_dict)) * 100, 2))}%."
    user_overview = user_overview + f"Percentage of tasks assigned to {username} that have been completed is {str(round((b / a) * 100, 2))}%."
    user_overview = user_overview + f"Percentage of tasks still to be completed by {username} is {str(round((c / a) * 100, 2))}%."
    user_overview = user_overview + f"Percentage of incomplete and overdue tasks assigned to {username} is {str(round((d / a) * 100, 2))}%."

    # 'user_overview' file.
    with open('user_overview.txt', 'w') as file4:
        file4.write(user_overview)        
    return("Your reports have been generated!")

user_details = {}

usernames = []
passwords = []

tasks_dict = {}

# Opening the task.txt file to read and write information from it.
# Adding the info in the user.txt file into the set list.
with open('user.txt', 'r+') as f:
    for line in f:
        newline = line.rstrip('\n')
        split_line = newline.split(", ")
        usernames.append(split_line[0 ])
        passwords.append(split_line[1])
        user_details["Usernames"] = usernames
        user_details["Passwords"] = passwords      
# count to keep track of the number of lines in the task.txt file.
count = 1
# Opening the task.txt file to read and write information to it.
with open('task.txt', 'r+') as file2:
    for line in file2:
        newline = line.rstrip('\n')  # Stripping newline characters.
        split_line = newline.split(", ")  # Splitting line into a list of items.
        tasks_dict[f"Task {count} details:"] = split_line # Assigning each list of items to a key in tasks_dict.
        count += 1  # Count used to change key value for each list of info.


username = input("Please enter your username: \n")
password = input("Please enter your password: \n")

while (username not in usernames) or (password not in passwords):
        
        if (username not in usernames) and (password in passwords):
            print("Your username is not listed.")
            username = input("Enter your usernam againe: \n")
            password = input("Enter your password again: \n")
        # If password is incorrect and username is correct, the following message is displayed.
        elif (password not in passwords) and (username in usernames):
            print("Your password is incorrect.")
            username = input("Enter your username again: \n")
            password = input("Enter your password again: \n")
        # If both the username and password are incorrect, the following message is displayed. 
        elif (username not in usernames) and (password not in passwords):
            print("Your username and password are incorrect.")
            username = input("Enter your username again: \n")
            password = input("Enter your password again: \n")
# If both username and password are correct           
if (username in usernames) and (password in passwords):
    print("You are successfully logged in.")

# loop created to display the menu once the user is logged in.
# allows the user to return to the menu after each option.
while 1:
    if username == "admin":  # only the admin is able to view the menu with both the gs and s options
        menu = input("""\n Select one of the following options:
                        r - register user
                        a - add task
                        va - view all tasks
                        vm - view my tasks
                        gr - generate reports
                        s - display statistics
                        e - exit \n""").lower()
        print("User's Option: ", menu)            

    else:
       menu = input("""\nPlease select one of the following options:
                        r - register user
                        a - add task
                        va - view all tasks
                        vm - view my tasks
                        gr - generate reports
                        e - exit
                        \n""").lower()
       print("User's Option: ", menu)
    if menu == "r":
        print(reg_user(menu))
    elif menu == "a":
        print(add_task(menu))
    elif menu == "va":
        print(view_all(menu))
    elif menu == "vm":
       print(view_mine(menu, username))
    elif menu == "gr":
        print(generate_reports())
    elif menu == 's':
        print(generate_reports())
        print("""\n The task overview report:\n""") 

        with open('task_overview.txt', 'r+') as file3:
            for line in file3:
                print(line)  # displaying each line in the file.
        print("""\n The user overview report:\n""")
        with open('user_overview.txt', 'r+') as file4:
            for line in file4:
                print(line) 
        print("""\n End of Statistics Reports\n""")
    elif menu == "e":
        print("You Have Been logged out.")
        break