import tkinter as tk
from tkinter import messagebox
import pandas as pd
import random
#importing predefined functions, lists and variables from the helpers file that will be used later
from src.helpers import clear_widgets, add_image, add_image_place_method, add_sectioning_image
from src.helpers import quotes
from src.helpers import background_colour_1, background_colour_2, font_colour_1, font_colour_2, text, heading

#configurating the GUI
root = tk.Tk()
root.title('Art Friend 🎨')
screen_width = 800
screen_height = 600
root.geometry(f'{screen_width}x{screen_height}+525+150') #placing the GUI in a specific space on the screen
root.configure(background = background_colour_1) #setting a background colour for the GUI

#LOGIN PAGES
def check_user(root):
    """
    This function checks if the user that is trying to log in exists.
    If the username is correct the user will be directed to the main app.
    """
    global username, usernames

    #reading and storing the usernames in the user data csv file
    usernames = list(pd.read_csv("data/user_data.csv").username)

    if username.get() in usernames: #if the user exists go to the next page
        username = username.get() #saving the username for later use
        create_homepage()
    else: #giving a warning to the user
        tk.messagebox.showwarning("WARNING", "User does not exist")

def create_login_page():
    """
    This function creates the widgets for the login page.
    On this page the user can enter their username, which is verified in the check_user function above.
    """
    global username

    root.configure(background = background_colour_2)
    clear_widgets(root)

    #asking for the username
    username_label = tk.Label(root,
                            text = 'Enter your username:',
                            bg = background_colour_2, fg = font_colour_1, font = text)
    username_label.place(x = 75, y = 150)

    #creating an entry box where the user can enter their username
    username = tk.StringVar()
    username_box = tk.Entry(root,
                            textvar = username,
                            fg = font_colour_1, bg = background_colour_1, font = text)
    username_box.place(x=300, y=150)

    #adding a button to check the information and log in
    login_button = tk.Button(root,
                             text = 'LOGIN',
                             bg = background_colour_2, fg = font_colour_1, font = text,
                             command = lambda:check_user(root))
    login_button.place(x=300, y=200)

def create_startpage():
    """
    This function configures and creates the start page of the app.
    This is the first page the user sees, and they will be redirected here when they log out.
    """
    clear_widgets(root) #this will do nothing when the app is first being executed, however the page will be cleared after logging out

    add_image(root, 'images/art_friend.jpg', 500, 175) #adding the apps logo to greet the user

    welcome_label = tk.Label(root,
                             text = 'Hi there! Please sign in to use the app! :)',
                             bg = background_colour_2, fg = font_colour_1, font = heading)
    welcome_label.pack(pady = 20)

    #placing a button to continue to the login page
    login_button = tk.Button(root, text = 'LOGIN',
                                      bg = font_colour_1, fg = font_colour_2, font = heading,
                                      command = create_login_page)
    login_button.pack()

#MAIN APP
def create_page_buttons():
    """
    This function places buttons that lead to the main pages of the app.
    With them the user can navigate between the homepage, the friends page, and the chat page.
    They can also log out. These buttons will be played on the bottom of every page for simple navigation.
    """
    add_sectioning_image(root) #adding an image to section out this part of the page

    home = tk.Button(root,
                     text = '🏠︎', width = 10,
                     font = text, fg = font_colour_1, bg = background_colour_2,
                     command = create_homepage)
    home.place(x=50, y=540)

    friends = tk.Button(root,
                        text = '❤', width = 10,
                        font = text, fg = font_colour_1, bg = background_colour_2,
                        command = create_friends_page)
    friends.place(x=240, y=540)

    chat = tk.Button(root,
                     text = '✉', width = 10,
                     font = text, fg = font_colour_1, bg = background_colour_2,
                     command = create_chat_page)
    chat.place(x=430, y=540)

    #logout button that leads back to the very first page
    logout = tk.Button(root,
                       text = 'Logout', width = 10,
                       font = text, fg = font_colour_1, bg = background_colour_2,
                       command = create_startpage)
    logout.place(x=625, y=540)

def display_profile():
    """
    This function displays the profile of any user from the database.
    It shows their username, profile picture, social media handles and biography.
    """
    profile_username_label = tk.Label(root,
                                      text=profile,
                                      fg=font_colour_2, bg=background_colour_1, font=heading)
    profile_username_label.pack(pady=10)

    add_image_place_method(root, f'images/{profile}_profile_pic.jpg', 200, 200, 200, 200)

    #fetching and placing the instagram handle from the wanted profile
    profile_insta_handle = list(userdata[userdata.username == profile].insta_handle)[0]
    profile_insta_handle_label = tk.Label(root,
                                          text=f'Insta: {profile_insta_handle}',
                                          fg=font_colour_1, bg=background_colour_1, font=text)
    profile_insta_handle_label.place(x=425, y=225)

    #fetching and placing the twitter handle from the wanted profile
    profile_twitter_handle = list(userdata[userdata.username == profile].twitter_handle)[0]
    profile_twitter_handle_label = tk.Label(root,
                                            text=f'Twitter: {profile_twitter_handle}',
                                            fg=font_colour_1, bg=background_colour_1, font=text)
    profile_twitter_handle_label.place(x=425, y=275)

    #fetching and placing the biography from the wanted profile
    profile_biography = list(userdata[userdata.username == profile].biography)[0]
    profile_biography_label = tk.Label(root,
                                       text=profile_biography,
                                       fg=font_colour_1, bg=background_colour_1, font=text)
    profile_biography_label.place(x=425, y=325)

def like():
    """
    This function defines what to do when the user likes a profile.
    It will save the profiles name to the friend list of the user.
    """
    #creating a dictionary with the profile as a friend
    user_friends = {
        'friends': profile
    }
    user_friends_df = pd.DataFrame([user_friends]) #turning the dictionary into a pandas dataframe
    #saving the dataframe in the users friends csv file
    user_friends_df.to_csv(f'data/{username}_friends.csv', index=False, mode='a', header=False)

    clear_widgets(root)
    create_homepage() #creating the homepage again to randomize a new profile

def dislike():
    """
    This function defines what to do with a profile the user dislikes.
    It will be added to the list of disliked profiles list by the user.
    """
    #creating a dictionary with the profile as a disliked user
    user_disliked = {
        'disliked': profile
    }
    user_disliked_df = pd.DataFrame([user_disliked]) #turning the dictionary into a pandas dataframe
    #saving the dataframe in the users disliked profiles csv file
    user_disliked_df.to_csv(f'data/{username}_disliked.csv', index=False, mode='a', header=False)

    clear_widgets(root)
    create_homepage() #creating the homepage again to randomize a new profile

def randomize_profile():
    """
    This function randomly picks a profile from the userdata.
    It will then be displayed for the user as a potential friend.
    """
    global userdata, userfriends, user_disliked, profile, possible_profiles

    userdata = pd.read_csv('data/user_data.csv') #fetching the userdata from the csv file
    #fetching data that is specific to the user that is currently logged-in
    userfriends = list(pd.read_csv(f'data/{username}_friends.csv').friends)
    user_disliked = list(pd.read_csv(f'data/{username}_disliked.csv').disliked)

    possible_profiles = [] #creating an empty list of profiles that can shown to be filled in the next step

    #checking for every profile in the user database whether it was already liked or disliked by the user
    for profile in usernames:
        if profile not in userfriends:
            if profile not in user_disliked:
                possible_profiles.append(profile) #adding the appropriate profiles to the list of possible profiles

    possible_profiles.remove(username) #removing the user that is logged-in from the profiles that can be shown

    if len(possible_profiles) == 0: #checking if there are profiles available to show
        no_profiles_label = tk.Label(root,
                                     text = 'We do not have any profiles left to show you! :)',
                                     fg = font_colour_2, bg = background_colour_1, font = heading)
        no_profiles_label.pack(pady = 25)

        no_profiles_label2 = tk.Label(root,
                                     text = 'Be sure to check out the profiles you saved on the friends page.',
                                     fg = font_colour_1, bg = background_colour_2, font = heading)
        no_profiles_label2.pack()
    else:
        profile = random.choice(possible_profiles) #picking a random profile that will be displayed

        display_profile()

        #adding a button that allows the user to save the profile to their friends
        like_button = tk.Button(root, text = '❤', width = 5,
                                fg = font_colour_2, bg = background_colour_1, font = text,
                                command = like)
        like_button.place(x = 300, y = 425)

        #adding a button that allows the user to save the profile to their disliked like
        dislike_button = tk.Button(root, text = 'X', width = 5,
                                   fg = font_colour_2, bg = background_colour_1, font = text,
                                   command = dislike)
        dislike_button.place(x = 430, y = 425)

def display_friend(friend):
    """
    This function displays the profile that the user clicked on in the friends page.
    """
    global profile

    clear_widgets(root)
    create_page_buttons()

    profile = friend #defining the profile to be displayed as the friend the user clicked on

    friendpage_label = tk.Label(root,
                                 text = f'Your friend, {profile}',
                                 fg = font_colour_1, bg = background_colour_2, font = heading)
    friendpage_label.pack(pady=10)

    friend_label = tk.Label(root,
                        text = 'This is your friends data:',
                        bg = background_colour_1, fg = font_colour_1,
                        font = text)
    friend_label.pack(pady = 10)

    display_profile()

def define_friend(friend):
    """
    This function returns the username that the user clicked on.
    """
    return lambda: display_friend(friend)

def display_friends():
    """
    This function adds a button for every friend the user has saved.
    Clicking on one of them will display the corresponding profile in the same format as on the homepage.
    """
    for friend in userfriends:
        value = friend
        friend_button = tk.Button(root,
                                text = friend,
                                bg = background_colour_2, fg = font_colour_1,
                                font = text, command = define_friend(value))
        friend_button.pack()

def create_homepage():
    """
    This function creates the homepage for the app.
    The homepage welcomes the user and displays different profiles that can be added to the friend list.
    """
    clear_widgets(root)
    create_page_buttons()

    root.configure(background = background_colour_1)
    welcome_label = tk.Label(root,
                             text = f'Welcome back to Art Friend, {username}!',
                             bg = background_colour_2, fg = font_colour_1,
                             font = heading)
    welcome_label.pack(pady = 10)

    random_quote = random.choice(quotes)  # choosing a random quote from the list in the helpers file
    quote_label = tk.Label(root,
                           text = random_quote,
                           fg = font_colour_1,
                           bg = background_colour_1,
                           font = text)
    quote_label.pack()

    profiles_label = tk.Label(root,
                           text = 'Here is a profile that might be of interest for you:',
                           fg = font_colour_1, bg = background_colour_1, font = text, pady = 15)
    profiles_label.pack()

    randomize_profile()

def create_friends_page():
    """
    This function creates the friends page of the app.
    It displays the friends the user has added and shows their information.
    """
    clear_widgets(root)
    create_page_buttons()

    friendspage_label = tk.Label(root,
                             text = 'Your friends',
                             fg = font_colour_1, bg = background_colour_2, font = heading)
    friendspage_label.pack(pady = 10)

    friends_label = tk.Label(root,
                           text = 'Here is a list with your friends:',
                           fg = font_colour_1, bg = background_colour_1, font = text)
    friends_label.pack()

    display_friends()


def sendmessage():
    """
    This function fetches the message in the chatbox.
    If there is a message, it will be mirrored.
    """
    user_message = entry_box.get()

    # if the user enters a message repeat it
    if user_message:
        text_box.insert(tk.END, f'\n{username}: {user_message}')
        text_box.insert(tk.END, f'\n{chat_username}: {user_message}')

def open_chat_room(root):
    """
    This function creates the chatbox.
    If the requested user is in the users friend list, a chat with that person will be opened.
    """
    global chat_username, entry_box, text_box
    userfriends = list(pd.read_csv(f'data/{username}_friends.csv').friends)
    if chat_username.get() in userfriends:
        chat_username = chat_username.get()
        clear_widgets(root)

        chat_label = tk.Label(root,
                                  text = f'Your chat with {chat_username}',
                                  fg = font_colour_1, bg = background_colour_2, font = heading)
        chat_label.pack(pady = 10)

        # creating the text box for the chat
        text_box = tk.Text(root,
                           fg = font_colour_1, bg = background_colour_1, font = text,
                           width = 50, height = 300)
        text_box.place(x = 0, y = 50, relwidth = 1)

        #explaing the chat to the user
        text_box.insert(tk.END, f'{chat_username}: Hi there! :)')
        text_box.insert(tk.END, f'\n{chat_username}: This is not a real chat since this is only an MVP...')
        text_box.insert(tk.END, f'\n{chat_username}: But I will mirror everything that you say!')

        #creating a scrollbar for the textbox
        scroll_bar = tk.Scrollbar(text_box)
        scroll_bar.place(relheight = 0.75, relx = 0.974)

        #creating an entry box for the user to enter a message
        entry_box = tk.Entry(root,
                             bg = background_colour_2, fg = font_colour_1, font = text,
                             width = 50)
        entry_box.place(x = 10,
                        rely = 0.80)

        send_button = tk.Button(root,
                                text = "Send",
                                bg = background_colour_2, fg = font_colour_1, font = text,
                                command = sendmessage,
                                width = 10)
        send_button.place(relx = 0.785,
                          rely = 0.78)

        create_page_buttons()
    else:
        #giving a warning that the username isn't in the friend list
        tk.messagebox.showwarning("WARNING",
                                  "User is not in friend list. Please correct your spelling.")

def create_chat_page():
    """
    This function creates the chat page.
    It gives the user the option to choose a friend to chat with.
    """
    global chat_username
    clear_widgets(root)
    create_page_buttons()

    chatpage_label = tk.Label(root,
                              text='Your chats',
                              fg=font_colour_1, bg=background_colour_2, font=heading)
    chatpage_label.pack(pady=10)

    chat_label = tk.Label(root,
                          text='Who do you want to chat with?',
                          fg=font_colour_1, bg=background_colour_1, font=text)
    chat_label.pack()

    chat_username = tk.StringVar()
    chat_username_box = tk.Entry(root,
                                 textvar=chat_username,
                                 fg=font_colour_1, bg=background_colour_1, font=text)
    chat_username_box.place(x=300, y=150)

    #adding a button to confirm the username
    chat_username_button = tk.Button(root,
                                     text='Chat with them',
                                     bg=background_colour_2, fg=font_colour_1, font=text,
                                     command=lambda: open_chat_room(root))
    chat_username_button.place(x=300, y=200)

create_startpage() #starting the GUI

root.mainloop()