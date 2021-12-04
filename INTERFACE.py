# !pip install lxml,bs4,requesets,tk,tkcalendar
# !pip install ttkwidgets

import io
import random
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import *
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df = pd.read_csv('cleaned_movies.csv', index_col = False)

movie_name = df['Movie']
movie_year = df['Production Year']
movie_list = movie_name + "  |  " + tuple(movie_year)

user_watch_history = pd.DataFrame(data=None,
                                  columns=["Movie", "Production Year", "Watchtime", "Rating", "Metascore", "Genres",
                                           "Description", "Votes", "Director"])


                        ###########################################
                        ######       CREATING INTERFACE       #####
                        ###########################################


root = Tk()
root.title("Movie Recommendation DataBase")
root.iconbitmap('images.ico')
canvas = Canvas(root, height=1100, width=2400, bg="#30475E")
canvas.pack()
root.state("zoomed")


                                        ##########################
                                        ##### PLOT FUNCTIONS #####
                                        ##########################

# Categorical Statistics #

def plot_categorical_stat():

    df = pd.read_csv('user_complete_watch_history.csv')

    df['Genres'].value_counts().plot(kind='pie', autopct='%1.1f%%',
                                     startangle=120, shadow=False, labels=df['Genres'], legend=False, fontsize=10)


# Production Year Statistics #

def plot_year_stat():

    df = pd.read_csv('user_complete_watch_history.csv')

    df['Production Year'].value_counts().plot(kind='bar', title='Production Year', legend=False, fontsize=9, rot=45)


# Director Statistics #

def plot_director_stat():
    df = pd.read_csv('user_complete_watch_history.csv')

    df['Director'] = df['Director'].apply(lambda x: str(x).replace('Director:',''))

    df['Director'] = df['Director'].apply(lambda x: str(x).replace('Directors:', ''))

    df['Director'] = df['Director'].apply(lambda x: str(x).replace('nan', 'Multiple Directors'))

    df['Director'].value_counts().plot(kind = 'barh', fontsize=13, color='navy',title='Director').invert_yaxis()


# Rating Statistics #

def plot_rate_stat():

    df = pd.read_csv('user_complete_watch_history.csv')

    df['Rating'] = pd.cut(df['Rating'], [1, 3, 5, 7, 9, 10], labels=['1-3', '3-5', '5-7', '7-9', '9-10'])

    df['Rating'].value_counts().plot(kind='bar', title='Rating', legend=False, fontsize=10, rot=45)



                        ##########################################################
                        ##### CREATING A NEW WINDOW TO GIVE POINTS TO MOVIE ######
                        ##########################################################

def point_screen(watched_movie):

    newWindow = Toplevel(root, bg="#5b9aa0")
    newWindow.title("Your point for the movie")
    newWindow.geometry("350x750")
    newWindow.resizable(0, 0)

    point_var = IntVar()
    point_var.set(0)

    def given_point(value):
        d = {'Movie': [watched_movie], 'Point': [value]}
        user_df = pd.DataFrame(data=d, columns=['Movie', 'Point'])

        if os.path.exists('user_watch_history.csv'):
            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_history.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        movie = watched_movie.split("|")[0]

        movie_list = list(df['Movie'].values)

        loop_movie = watched_movie.replace(" ", "").split('|')
        loop_movie = loop_movie[0]

        for i in range(len(movie_list)):
            if movie_list[i].replace(" ", "") == loop_movie:

                new_df_dict = {'Movie': df.iloc[i].values[0], 'Production Year': df.iloc[i].values[1],
                               'Watchtime': df.iloc[i].values[2],
                               'Rating': df.iloc[i].values[3], 'Metascore': df.iloc[i].values[4],
                               'Genres': df.iloc[i].values[5], 'Description': df.iloc[i].values[6],
                               'Votes': df.iloc[i].values[7], 'Director': df.iloc[i].values[8], 'User_Point': value
                               }

                new_df = pd.DataFrame([new_df_dict],
                                      columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                               'Description', 'Votes', 'Director', 'User_Point'])

                new_df['Director'] = new_df['Director'].apply(lambda x: str(x).replace('Director:', ''))

                new_df['Director'] = new_df['Director'].apply(lambda x: str(x).replace('Directors:', ''))

                new_df['Director'] = new_df['Director'].apply(lambda x: str(x).replace('nan', 'Multiple Directors'))

                new_df.drop_duplicates(keep = 'last',inplace = True)

                if os.path.exists('user_complete_watch_history.csv'):

                    boolean = False

                else:

                    boolean = True

                new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=boolean)


        messagebox.showinfo("POINT SCREEN", f"{movie} -> {value} ")
        newWindow.destroy()

    points = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for point in points:
        Radiobutton(newWindow, text=point, font="Times 12 bold", variable = point_var, value=point, relief=RAISED,
                    borderwidth=1, bd=4).pack(padx=5, pady=8, ipadx=15, ipady=7)

    save_button = Button(newWindow, text="Save My Point", font="Times 16 bold", borderwidth=1, bd=5,
                         relief=RAISED, command=lambda: given_point(point_var.get()))

    save_button.pack(padx=5, pady=20, ipadx=5, ipady=4)



###################################
##### WATCHED BUTTON FUNCTION #####
###################################

def watched():

    for i in my_list.curselection():
        watched_movie = my_list.get(i)

    point_screen(watched_movie)


##########################################
###### WATCH HISTORY BUTTON FUNCTION #####
##########################################

def watch_history():

    if os.path.exists('user_watch_history.csv'):

        watch_history_df = pd.read_csv('user_watch_history.csv')

        watched_movie_name = watch_history_df['Movie']
        point = watch_history_df['Point']

        watch_historyWindows = Toplevel(bg="#30475E")
        watch_historyWindows.state("zoomed")
        watch_historyWindows.title("Watched Movies")

        watch_history_label = Label(watch_historyWindows, text=str("Search the Movie"), bg="#FFC074", fg="black",
                                    font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        watch_history_label.place(relx=0.055, rely=0.03, relwidth=0.4, relheight=0.95)

        watch_history_graph = Label(watch_historyWindows, text=str("Watch History Graphics"), bg="#FFA36C", fg="black",
                                    font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        watch_history_graph.place(relx=0.530, rely=0.25, relwidth=0.4, relheight=0.45)

        def clear_watch_history():

            resp = messagebox.askokcancel("Delete Watch History", "Are you sure want to delete the Watch History?")
            Label(watch_historyWindows, text=resp).pack()

            if resp == 1:
                os.remove("user_watch_history.csv")
                os.remove('user_complete_watch_history.csv')
                messagebox.showinfo("Delete Watch History", "You Deleted the Watch History!")

            elif resp == 0:
                messagebox.showinfo("Delete Watch History ", "That was close")

        clear_watch_history_Button = Button(watch_historyWindows, text="Clear Watch History", font="Times 14 bold",
                                            borderwidth=1, bd=6,
                                            relief=RAISED, command=clear_watch_history)

        clear_watch_history_Button.place(relx=0.108, rely=0.85, relwidth=0.123, relheight=0.08)

        plot_categorical_stat_Button = Button(master=watch_historyWindows, text="Categorical Graph",
                                              font="Times 14 bold", borderwidth=1, bd=6,
                                              relief=RAISED, command=plot_categorical_stat)

        plot_categorical_stat_Button.place(relx=0.57, rely=0.365, relwidth=0.123, relheight=0.09)

        plot_year_stat_Button = Button(master=watch_historyWindows, text="Production Year Graph",
                                       font="Times 14 bold", borderwidth=1, bd=6,
                                       relief=RAISED, command=plot_year_stat)

        plot_year_stat_Button.place(relx=0.75, rely=0.365, relwidth=0.136, relheight=0.09)

        plot_director_stat_Button = Button(master=watch_historyWindows, text="Director Graph",
                                           font="Times 14 bold", borderwidth=1, bd=6,
                                           relief=RAISED, command=plot_director_stat)

        plot_director_stat_Button.place(relx=0.57, rely=0.5, relwidth=0.123, relheight=0.09)

        plot_rate_stat_Button = Button(master=watch_historyWindows, text="Rate Graph",
                                       font="Times 14 bold", borderwidth=1, bd=6,
                                       relief=RAISED, command=plot_rate_stat)

        plot_rate_stat_Button.place(relx=0.75, rely=0.5, relwidth=0.136, relheight=0.09)


############################################
##### CREATING LISTBOX TO CHOOSE MOVIE #####
############################################

        def update(data):
            # Clear the listbox #

            my_list.delete(0, END)

            # Add data to listbox #

            for item in data:
                my_list.insert(END, item)

        # Update entry box with listbox clicked #

        def fillout(e):
            # Delete whatever is in the entry box #
            my_entry.delete(0, END)

            # Add clicked list item to entry box #
            my_entry.insert(0, my_list.get(ANCHOR))

        # Create function to check entry vs listbox #

        def check(e):
            # grab what was typed
            typed = my_entry.get()

            if typed == '':
                data = watched_movie_name
            else:
                data = []
                for item in watched_movie_name:
                    if typed.lower() in item.lower():
                        data.append(item)

            # update our listbox with selected items
            update(data)

        ################################
        ###### Create an entry box #####
        ################################

        my_entry = Entry(watch_history_label, font=("Helvetica", 14))
        my_entry.place(relx=0.02, rely=0.05, relwidth=0.87, relheight=0.06)

        ############################
        ##### Create a listbox #####
        ############################

        my_list = Listbox(watch_history_label, width=51, height=22, font=("Helvetica", 13), selectmode=SINGLE)

        my_list.place(relx=0.02, rely=0.12, relwidth=0.87, relheight=0.74)

        #############################################
        ##### Add the Watched Movie to the list #####
        #############################################

        update(watched_movie_name)

        ############## Create a binding on the listbox onclick ##############
        my_list.bind("<<ListboxSelect>>", fillout)

        ############## Create a binding on the entry box ##############
        my_entry.bind("<KeyRelease>", check)

        ############## Create Scrollbar ##############
        scrollbar = Scrollbar(
            watch_history_label,
            orient='vertical',
            command=my_list.yview
        )

        my_list['yscrollcommand'] = scrollbar.set

        scrollbar.place(relx=0.93, rely=0.12, relwidth=0.042, relheight=0.74)

    else:
        messagebox.showinfo("Watch History", "There is no Watch History!")

    def clear_movie():

        for i in my_list.curselection():
            watched_movie = my_list.get(i)

            data = pd.read_csv('user_watch_history.csv')

            movie_index = data[data['Movie'] == watched_movie].index

            movie_to_be_cleared = data.iloc[movie_index]

            new_Df = data.drop(data.index[movie_index])

            new_Df.to_csv("user_watch_history.csv", index=False)

            all_movie_data = pd.read_csv('user_complete_watch_history.csv')

            new_all_movie_data = all_movie_data.drop(all_movie_data.index[movie_index])

            new_all_movie_data.to_csv("user_complete_watch_history.csv", index=False)

            messagebox.showinfo("Delete The Movie", f"You Deleted {watched_movie}")

            watch_history()

    clear_watched_movie_button = Button(watch_historyWindows, text="Clear The Movie", font="Times 14 bold",
                                        borderwidth=1, bd=6,
                                        relief=RAISED, command=clear_movie)

    clear_watched_movie_button.place(relx=0.254, rely=0.85, relwidth=0.12, relheight=0.08)


                            ####################################
                            ######         FRAMES         ######
                            ####################################

watchedMovie = Frame(root, bg="#FFC074", bd=10, relief=RAISED)
watchedMovie.place(relx=0.03, rely=0.025, relwidth=0.355, relheight=0.94)

watchedMovie_label = Label(watchedMovie, text=str("Search the Movie"), bg="#FFC074", fg="black",
                           font="Times 17 bold underline", anchor='n')
watchedMovie_label.grid(row=0, column=2, padx=5, pady=5, ipadx=23)



############## Creating search and autofill ##############

############## Update the listbox ##############

def update(data):
    ############## Clear the listbox ##############

    my_list.delete(0, END)

    ############## Add movies to listbox ##############

    for item in data:
        my_list.insert(END, item)


############## Update entry box with listbox clicked ##############

def fillout(e):
    #### Delete whatever is in the entry box ####
    my_entry.delete(0, END)

    #### Add clicked list item to entry box ####
    my_entry.insert(0, my_list.get(ANCHOR))


##### Create function to check entry vs listbox ####

def check(e):
    # grab what was typed
    typed = my_entry.get()

    if typed == '':
        data = movie_list
    else:
        data = []
        for item in movie_list:
            if typed.lower() in item.lower():
                data.append(item)

    # update our listbox with selected items
    update(data)


############## Create an entry box ##############

my_entry = Entry(watchedMovie, font=("Helvetica", 15))
my_entry.grid(row=2, column=2, padx=14, pady=13, ipadx=115, ipady=5)

############## Create a listbox ##############
my_list = Listbox(watchedMovie, width=51, height=22, font=("Helvetica", 11), selectmode=SINGLE)

my_list.grid(row=4, column=2, padx=17, pady=13, ipadx=23)

############## Add the toppings to our list ##############
update(movie_list)

############## Create a binding on the listbox onclick ##############
my_list.bind("<<ListboxSelect>>", fillout)

############## Create a binding on the entry box ##############
my_entry.bind("<KeyRelease>", check)

############## Create Scrollbar ##############
scrollbar = Scrollbar(
    watchedMovie,
    orient='vertical',
    command=my_list.yview
)

my_list['yscrollcommand'] = scrollbar.set

scrollbar.grid(row=4, column=3, padx=4, pady=15, ipadx=2, ipady=174)


def will_be_watched():
    for i in my_list.curselection():

        will_be_watched_movie = my_list.get(i)

        movie = will_be_watched_movie.split("|")[0].strip()

        production_year = will_be_watched_movie.split("|")[1].strip()

        d = {'Movie': movie, 'Production Year': production_year}

        user_df = pd.DataFrame(d, columns=['Movie', 'Production Year'], index=[0])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:

            boolean = True

        user_df.drop_duplicates(keep='last', inplace=True, ignore_index=True)

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("POINT SCREEN", f"{movie} -> Added to WatchList ")



                    ##################################################################
                    ################# CREATING WATCH HISTORY BUTTONS #################
                    ##################################################################

add_watch_history = Button(watchedMovie, text="Watched", font="Times 16 bold", borderwidth=1, bd=6, relief=RAISED,
                           command=watched)
add_watch_history.place(relx=0.033, rely=0.74, relwidth=0.3, relheight=0.09)

add_watch_list = Button(watchedMovie, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6, relief=RAISED,
                        command=will_be_watched)
add_watch_list.place(relx=0.033, rely=0.88, relwidth=0.3, relheight=0.09)

show_watch_history = Button(watchedMovie, text="Watch History", font="Times 16 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=watch_history)
show_watch_history.place(relx=0.61, rely=0.74, relwidth=0.3, relheight=0.09)


######################################
##### WATCH LIST DISPLAY FUNCTION ####
######################################

def show_watch_list():

    if os.path.exists('user_watch_list.csv'):


        df = pd.read_csv('user_watch_list.csv', dtype='string')

        if df.empty == True:
            messagebox.showinfo("WATCH LIST", "Watch List is Empty ! ")


        #df.drop_duplicates(keep='last', inplace=True, ignore_index=True)

        #df.to_csv('user_watch_list.csv', header=False)

        will_be_watched_movie_name = df['Movie']

        will_be_watched_movie_year = df['Production Year']

        will_be_watched_movie_name = will_be_watched_movie_name + '  |  ' + will_be_watched_movie_year

        watch_list_Windows = Toplevel(bg="#30475E")
        watch_list_Windows.state("zoomed")
        watch_list_Windows.title("WatchList")

        watch_list_label = Label(watch_list_Windows, text="Your Watch List", bg="#FFC074", fg="black",
                                 font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        watch_list_label.place(relx=0.075, rely=0.035, relwidth=0.55, relheight=0.95)

        ############## Creating search and autofill ##############

        ############## Update the listbox ##############

        def update(data):
            ############## Clear the listbox ##############

            my_list.delete(0, END)

            ############## Add toppings to listbox ##############

            for item in data:
                my_list.insert(END, item)

        ############## Update entry box with listbox clicked ##############

        def fillout(e):
            #### Delete whatever is in the entry box ####
            my_entry.delete(0, END)

            #### Add clicked list item to entry box ####
            my_entry.insert(0, my_list.get(ANCHOR))

        ##### Create function to check entry vs listbox ####

        def check(e):
            # grab what was typed
            typed = my_entry.get()

            if typed == '':
                data = will_be_watched_movie_name
            else:
                data = []
                for item in will_be_watched_movie_name:
                    if typed.lower() in item.lower():
                        data.append(item)

            # update our listbox with selected items
            update(data)

        ############## Create an entry box ##############
        my_entry = Entry(watch_list_Windows, font=("Helvetica", 15))
        my_entry.place(relx=0.13, rely=0.11, relwidth=0.37, relheight=0.04)

        ############## Create a listbox ##############
        my_list = Listbox(watch_list_Windows, width=51, height=22, font=("Helvetica", 13), selectmode=SINGLE)

        my_list.place(relx=0.13, rely=0.17, relwidth=0.37, relheight=0.71)

        ############## Add the movies to list ##############
        update(will_be_watched_movie_name)

        ############## Create a binding on the listbox onclick ##############
        my_list.bind("<<ListboxSelect>>", fillout)

        ############## Create a binding on the entry box ##############
        my_entry.bind("<KeyRelease>", check)

        ############## Create Scrollbar ##############
        scrollbar = Scrollbar(
            watch_list_Windows,
            orient='vertical',
            command=my_list.yview
        )

        my_list['yscrollcommand'] = scrollbar.set

        scrollbar.place(relx=0.555, rely=0.17, relwidth=0.02, relheight=0.71)

    else:

        messagebox.showinfo("WATCH LIST", "There is no Watch List ! ")



    ### Function that will delete the chosen movie from the Watch List ###

    def delete_watch_list():

        for i in my_list.curselection():

            deleted_movie = my_list.get(i)

            print(deleted_movie)

            movie = deleted_movie.split("|")[0].strip()

            production_year = deleted_movie.split("|")[1].strip()


            d = {'Movie': movie, 'Production Year': production_year}

            delete_df = pd.DataFrame(d, columns=['Movie', 'Production Year'],index = [0])

            user_watch_list_df = pd.read_csv('user_watch_list.csv')

            user_watch_list_df = user_watch_list_df[~user_watch_list_df['Movie'].str.contains(movie)]

            user_watch_list_df.to_csv("user_watch_list.csv", index=False)

            messagebox.showinfo("Delete The Movie", f"You Deleted {deleted_movie}")

            watch_list_Windows.destroy()

            show_watch_list()


    ### Function that will clear all the Watch List ###

    def clear_watch_list():

        os.remove("user_watch_list.csv")

        messagebox.showinfo("WATCHLIST", "You Cleared The Watch List")

        watch_list_Windows.destroy()


                #########################################################
                ###### DELETE THE MOVIE FROM THE WATCH LIST BUTTON ######
                #########################################################

    delete_watch_list_movie_Button = Button(watch_list_Windows, text="Delete The Movie", font="Times 16 bold",
                                            borderwidth=1, bd=6, relief=RAISED,
                                            command=delete_watch_list)

    delete_watch_list_movie_Button.place(relx=0.73, rely=0.18, relwidth=0.17, relheight=0.08)


                        #########################################
                        ###### CLEAR THE WATCH LIST BUTTON ######
                        #########################################

    clear_watch_list_movie_Button = Button(watch_list_Windows, text="Clear The Watch List", font="Times 16 bold",
                                           borderwidth=1,
                                           bd=6, relief=RAISED,
                                           command=clear_watch_list)

    clear_watch_list_movie_Button.place(relx=0.73, rely=0.43, relwidth=0.17, relheight=0.08)


###################################
##### SHOW WATCH LIST BUTTON ######
###################################

show_watch_list_Button = Button(watchedMovie, text="Watch List", font="Times 16 bold", borderwidth=1, bd=6,
                                relief=RAISED, command=show_watch_list)

show_watch_list_Button.place(relx=0.61, rely=0.88, relwidth=0.3, relheight=0.09)


                                #############################################
                                ###### CATEGORICAL RECOMMENDATION PART ######
                                #############################################

#######################
##### MOVIE FRAME #####
#######################

movieFrame = Frame(root, bg="#FFA36C", bd=8, relief=RAISED)

movieFrame.place(relx=0.42, rely=0.025, relwidth=0.55, relheight=0.485)

movieVariable = IntVar()

movieLabel = Label(movieFrame, bg="#FFA36C", fg="black", text="CATEGORICAL RECOMMENDATION",
                   font="Times 18 bold italic underline")

movieLabel.place(relx=0.25, rely=0.001, relwidth=0.5, relheight=0.1)


###################################################
###### GETTING THE CSV FILE BASED ON CATEGORY #####
###################################################

def recommend_movie_csv(movie_genre):

    global df

    df = pd.read_csv(f'{movie_genre}_movie.csv')

    df = df.drop_duplicates(subset="Movie", keep='first').reset_index(drop=True)

    df = df.sort_values(by='Movie')

    df = df.sample(1, ignore_index=False)

    movie_name = df['Movie']

    movie_year = df['Production Year']

    recommended_movie = movie_name + ' | ' + movie_year

    return list(recommended_movie)


                    ################## Action Movie Recommendation ##################

def ActionButtonFunc():

    newActionWindows = Toplevel()
    newActionWindows.state("zoomed")
    newActionWindows.title("Action Movie Recommendation")

    action_movie_canvas = Canvas(newActionWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    action_movie_canvas.pack()

    actionMovieArea = Text(newActionWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)

    theActionMovie = "{}".format(recommend_movie_csv('action'))

    actionMovieArea.tag_configure('style', font=('Verdana', 14))

    actionMovieArea.insert(END, theActionMovie, 'style')
    actionMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)


    def watched_rec():

        point_screen(theActionMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df],ignore_index= True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a',header = False)

            newActionWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df],ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a',header = True)

            newActionWindows.destroy()


    def rec_another():
        ActionButtonFunc()

        newActionWindows.destroy()

    def action_watch_list():

        will_be_watched_movie = theActionMovie.split('|')[0]
        movie_production_year = theActionMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    ###############
    ### BUTTONS ###
    ###############

    add_watch_history = Button(newActionWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command= watched_rec)

    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newActionWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=action_watch_list)

    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newActionWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


actionButton = Button(movieFrame, text="Action", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                      command=ActionButtonFunc)
actionButton.place(relx=0.02, rely=0.22, relwidth=0.15, relheight=0.15)


                    ################## Adventure Recommendation ##################

def AdventureButtonFunc():

    newAdventureWindows = Toplevel()
    newAdventureWindows.state("zoomed")
    newAdventureWindows.title("Adventure Movie Recommendation")

    adventure_movie_canvas = Canvas(newAdventureWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    adventure_movie_canvas.pack()

    adventureMovieArea = Text(newAdventureWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theAdventureMovie = "{}".format(recommend_movie_csv('adventure'))

    adventureMovieArea.tag_configure('style', font=('Verdana', 14))

    adventureMovieArea.insert(END, theAdventureMovie, 'style')
    adventureMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():

        point_screen(theAdventureMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newAdventureWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newAdventureWindows.destroy()

    def rec_another():

        AdventureButtonFunc()
        newAdventureWindows.destroy()

    def adventure_watch_list():

        will_be_watched_movie = theAdventureMovie.split('|')[0]
        movie_production_year = theAdventureMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")



    add_watch_history = Button(newAdventureWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)

    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newAdventureWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=adventure_watch_list)

    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newAdventureWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)

    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


adventureButton = Button(movieFrame, text="Adventure", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                         command=AdventureButtonFunc)
adventureButton.place(relx=0.21, rely=0.22, relwidth=0.15, relheight=0.15)


                 ################## Comedy Movie Recommendation ##################

def ComedyButtonFunc():
    newComedyWindows = Toplevel()
    newComedyWindows.state("zoomed")
    newComedyWindows.title("Comedy Movie Recommendation")

    comedy_movie_canvas = Canvas(newComedyWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    comedy_movie_canvas.pack()

    comedyMovieArea = Text(newComedyWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theComedyMovie = "{}".format(recommend_movie_csv('comedy'))

    comedyMovieArea.tag_configure('style', font=('Verdana', 14))

    comedyMovieArea.insert(END, theComedyMovie, 'style')
    comedyMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():

        point_screen(theComedyMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newComedyWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newComedyWindows.destroy()


    def rec_another():

        ComedyButtonFunc()
        newComedyWindows.destroy()

    def comedy_watch_list():

        will_be_watched_movie = theComedyMovie.split('|')[0]
        movie_production_year = theComedyMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")


    add_watch_history = Button(newComedyWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newComedyWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=comedy_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newComedyWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


comedyButton = Button(movieFrame, text="Comedy", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                      command=ComedyButtonFunc)
comedyButton.place(relx=0.4, rely=0.22, relwidth=0.15, relheight=0.15)


                    ################## Crime Movie Recommendation ##################

def CrimeButtonFunc():
    newCrimeWindows = Toplevel()
    newCrimeWindows.state("zoomed")
    newCrimeWindows.title("Crime Movie Recommendation")

    crime_movie_canvas = Canvas(newCrimeWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    crime_movie_canvas.pack()

    crimeMovieArea = Text(newCrimeWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theCrimeMovie = "{}".format(recommend_movie_csv('crime'))

    crimeMovieArea.tag_configure('style', font=('Verdana', 14))

    crimeMovieArea.insert(END, theCrimeMovie, 'style')
    crimeMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():

        point_screen(theCrimeMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newCrimeWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)
    def rec_another():
        CrimeButtonFunc()
        newCrimeWindows.destroy()

    def crime_watch_list():

        will_be_watched_movie = theCrimeMovie.split('|')[0]
        movie_production_year = theCrimeMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")



    add_watch_history = Button(newCrimeWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newCrimeWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=crime_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newCrimeWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


crimeButton = Button(movieFrame, text="Crime", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                     command=CrimeButtonFunc)
crimeButton.place(relx=0.59, rely=0.22, relwidth=0.15, relheight=0.15)


                    ################## Drama Movie Recommendation ##################

def DramaButtonFunc():
    newDramaWindows = Toplevel()
    newDramaWindows.state("zoomed")
    newDramaWindows.title("Drama Movie Recommendation")

    drama_movie_canvas = Canvas(newDramaWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    drama_movie_canvas.pack()

    dramaMovieArea = Text(newDramaWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theDramaMovie = "{}".format(recommend_movie_csv('drama'))

    dramaMovieArea.tag_configure('style', font=('Verdana', 14))

    dramaMovieArea.insert(END, theDramaMovie, 'style')
    dramaMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():
        point_screen(theDramaMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newDramaWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newDramaWindows.destroy()

    def rec_another():
        DramaButtonFunc()
        newDramaWindows.destroy()

    def drama_watch_list():

        will_be_watched_movie = theDramaMovie.split('|')[0]
        movie_production_year = theDramaMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newDramaWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newDramaWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=drama_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newDramaWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


dramaButton = Button(movieFrame, text="Drama", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                     command=DramaButtonFunc)
dramaButton.place(relx=0.02, rely=0.47, relwidth=0.15, relheight=0.15)


                    ################## Fantasy Movie Recommendation ##################

def FantasyButtonFunc():
    newFantasyWindows = Toplevel()
    newFantasyWindows.state("zoomed")
    newFantasyWindows.title("Fantasy Movie Recommendation")

    fantasy_movie_canvas = Canvas(newFantasyWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    fantasy_movie_canvas.pack()

    fantasyMovieArea = Text(newFantasyWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theFantasyMovie = "{}".format(recommend_movie_csv('fantasy'))

    fantasyMovieArea.tag_configure('style', font=('Verdana', 14))

    fantasyMovieArea.insert(END, theFantasyMovie, 'style')
    fantasyMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():

        point_screen(theFantasyMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newFantasyWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newFantasyWindows.destroy()

    def rec_another():
        FantasyButtonFunc()
        newFantasyWindows.destroy()

    def fantasy_watch_list():

        will_be_watched_movie = theFantasyMovie.split('|')[0]
        movie_production_year = theFantasyMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newFantasyWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newFantasyWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=fantasy_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newFantasyWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


fantasyButton = Button(movieFrame, text="Fantasy", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                       command=FantasyButtonFunc)
fantasyButton.place(relx=0.21, rely=0.47, relwidth=0.15, relheight=0.15)


                    ################## Horror Movie Recommendation ##################

def HorrorButtonFunc():
    newHorrorWindows = Toplevel()
    newHorrorWindows.state("zoomed")
    newHorrorWindows.title("Horror Movie Recommendation")

    horror_movie_canvas = Canvas(newHorrorWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    horror_movie_canvas.pack()

    horrorMovieArea = Text(newHorrorWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theHorrorMovie = "{}".format(recommend_movie_csv('horror'))

    horrorMovieArea.tag_configure('style', font=('Verdana', 14))

    horrorMovieArea.insert(END, theHorrorMovie, 'style')
    horrorMovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():
        point_screen(theHorrorMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newHorrorWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newHorrorWindows.destroy()

    def rec_another():
        HorrorButtonFunc()
        newHorrorWindows.destroy()

    def horror_watch_list():

        will_be_watched_movie = theHorrorMovie.split('|')[0]
        movie_production_year = theHorrorMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newHorrorWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newHorrorWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=horror_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newHorrorWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


horrorButton = Button(movieFrame, text="Horror", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                      command=HorrorButtonFunc)
horrorButton.place(relx=0.4, rely=0.47, relwidth=0.15, relheight=0.15)


                    ################## Mystery Movie Recommendation ##################

def MysteryButtonFunc():
    newMysteryWindows = Toplevel()
    newMysteryWindows.state("zoomed")
    newMysteryWindows.title("Mystery Movie Recommendation")

    mystery_movie_canvas = Canvas(newMysteryWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    mystery_movie_canvas.pack()

    mystery_MovieArea = Text(newMysteryWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theMysteryMovie = "{}".format(recommend_movie_csv('mystery'))

    mystery_MovieArea.tag_configure('style', font=('Verdana', 14))

    mystery_MovieArea.insert(END, theMysteryMovie, 'style')
    mystery_MovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():
        point_screen(theMysteryMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newMysteryWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newMysteryWindows.destroy()

    def rec_another():
        MysteryButtonFunc()
        newMysteryWindows.destroy()

    def mystery_watch_list():

        will_be_watched_movie = theMysteryMovie.split('|')[0]
        movie_production_year = theMysteryMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newMysteryWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newMysteryWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=mystery_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newMysteryWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


mysteryButton = Button(movieFrame, text="Mystery", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                       command=MysteryButtonFunc)
mysteryButton.place(relx=0.59, rely=0.47, relwidth=0.15, relheight=0.15)


                    ################## Romance Movie Recommendation ##################

def RomanceButtonFunc():
    newRomanceWindows = Toplevel()
    newRomanceWindows.state("zoomed")
    newRomanceWindows.title("Romance Movie Recommendation")

    romance_movie_canvas = Canvas(newRomanceWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    romance_movie_canvas.pack()

    romance_MovieArea = Text(newRomanceWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theRomanceMovie = "{}".format(recommend_movie_csv('romance'))

    romance_MovieArea.tag_configure('style', font=('Verdana', 14))

    romance_MovieArea.insert(END, theRomanceMovie, 'style')
    romance_MovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():
        point_screen(theRomanceMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newRomanceWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newRomanceWindows.destroy()

    def rec_another():
        RomanceButtonFunc()
        newRomanceWindows.destroy()

    def romance_watch_list():

        will_be_watched_movie = theRomanceMovie.split('|')[0]
        movie_production_year = theRomanceMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newRomanceWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newRomanceWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=romance_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newRomanceWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


romanceButton = Button(movieFrame, text="Romance", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                       command=RomanceButtonFunc)
romanceButton.place(relx=0.02, rely=0.72, relwidth=0.15, relheight=0.15)


                    ################## Sci-fi Movie Recommendation ##################

def ScifiButtonFunc():
    newScifiWindows = Toplevel()
    newScifiWindows.state("zoomed")
    newScifiWindows.title("Sci-fi Movie Recommendation")

    scifi_movie_canvas = Canvas(newScifiWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    scifi_movie_canvas.pack()

    scifi_MovieArea = Text(newScifiWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theScifiMovie = "{}".format(recommend_movie_csv('scifi'))

    scifi_MovieArea.tag_configure('style', font=('Verdana', 14))

    scifi_MovieArea.insert(END, theScifiMovie, 'style')
    scifi_MovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():
        point_screen(theScifiMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newScifiWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newScifiWindows.destroy()

    def rec_another():
        ScifiButtonFunc()
        newScifiWindows.destroy()

    def scifi_watch_list():

        will_be_watched_movie = theScifiMovie.split('|')[0]
        movie_production_year = theScifiMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newScifiWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newScifiWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=scifi_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newScifiWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


scienceFictionButton = Button(movieFrame, text="Sci-Fi", font="Times 16 italic bold", borderwidth=1, bd=6,
                              relief=RAISED, command=ScifiButtonFunc)
scienceFictionButton.place(relx=0.21, rely=0.72, relwidth=0.15, relheight=0.15)


                    ################## Super-Hero Movie Recommendation ##################

def SuperHeroButtonFunc():
    newSuperHeroWindows = Toplevel()
    newSuperHeroWindows.state("zoomed")
    newSuperHeroWindows.title("SuperHero Movie Recommendation")

    superhero_movie_canvas = Canvas(newSuperHeroWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    superhero_movie_canvas.pack()

    superhero_MovieArea = Text(newSuperHeroWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theSuperHeroMovie = "{}".format(recommend_movie_csv('superhero'))

    superhero_MovieArea.tag_configure('style', font=('Verdana', 14))

    superhero_MovieArea.insert(END, theSuperHeroMovie, 'style')
    superhero_MovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():
        point_screen(theSuperHeroMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newSuperHeroWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newSuperHeroWindows.destroy()

    def rec_another():
        SuperHeroButtonFunc()
        newSuperHeroWindows.destroy()

    def superhero_watch_list():

        will_be_watched_movie = theSuperHeroMovie.split('|')[0]
        movie_production_year = theSuperHeroMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newSuperHeroWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newSuperHeroWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=superhero_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newSuperHeroWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


superHeroButton = Button(movieFrame, text="Super-Hero", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                         command=SuperHeroButtonFunc)
superHeroButton.place(relx=0.4, rely=0.72, relwidth=0.15, relheight=0.15)


                    ################## Thriller Movie Recommendation ##################

def ThrillerButtonFunc():
    newThrillerWindows = Toplevel()
    newThrillerWindows.state("zoomed")
    newThrillerWindows.title("Thriller Movie Recommendation")

    thriller_movie_canvas = Canvas(newThrillerWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    thriller_movie_canvas.pack()

    thriller_MovieArea = Text(newThrillerWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theThrillerMovie = "{}".format(recommend_movie_csv('thriller'))

    thriller_MovieArea.tag_configure('style', font=('Verdana', 14))

    thriller_MovieArea.insert(END, theThrillerMovie, 'style')
    thriller_MovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():

        point_screen(theThrillerMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newThrillerWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newThrillerWindows.destroy()

    def rec_another():

        ThrillerButtonFunc()
        newThrillerWindows.destroy()

    def thriller_watch_list():

        will_be_watched_movie = theThrillerMovie.split('|')[0]
        movie_production_year = theThrillerMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")


    add_watch_history = Button(newThrillerWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newThrillerWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=thriller_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newThrillerWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


thrillerButton = Button(movieFrame, text="Thriller", font="Times 16 italic bold", borderwidth=1, bd=6, relief=RAISED,
                        command=ThrillerButtonFunc)
thrillerButton.place(relx=0.59, rely=0.72, relwidth=0.15, relheight=0.15)


                    ################## Random Movie Recommendation ##################


def RandomButtonFunc():
    movie_categories_list = list(
        ['action', 'adventure', 'comedy', 'crime', 'drama', 'fantasy', 'horror', 'mystery', 'romance', 'scifi',
         'superhero', 'thriller'])
    random_choiced_movie = random.choice(movie_categories_list)

    newRandomWindows = Toplevel()
    newRandomWindows.state("zoomed")
    newRandomWindows.title("Random Movie Recommendation")

    random_movie_canvas = Canvas(newRandomWindows, bg="#528AAE", height=1100, width=2400, bd=5, relief=RAISED)
    random_movie_canvas.pack()

    random_MovieArea = Text(newRandomWindows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
    theRandomMovie = "{}".format(recommend_movie_csv(f'{random_choiced_movie}'))

    random_MovieArea.tag_configure('style', font=('Verdana', 14))

    random_MovieArea.insert(END, theRandomMovie, 'style')
    random_MovieArea.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

    def watched_rec():

        point_screen(theRandomMovie)

        if os.path.exists('user_complete_watch_history.csv'):

            user_watch_history_df = pd.read_csv('user_complete_watch_history.csv')

            user_watch_history_df = pd.concat([df], ignore_index=True)

            user_watch_history_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=False)

            newRandomWindows.destroy()

        else:

            new_df = pd.DataFrame(columns=['Movie', 'Production Year', 'Watchtime', 'Rating', 'Metascore', 'Genres',
                                           'Description', 'Votes', 'Director', 'User_Point'])

            new_df = pd.concat([df], ignore_index=True)

            new_df.to_csv('user_complete_watch_history.csv', index=False, mode='a', header=True)

            newRandomWindows.destroy()

    def rec_another():
        RomanceButtonFunc()
        newRandomWindows.destroy()

    def random_watch_list():

        will_be_watched_movie = theRandomMovie.split('|')[0]
        movie_production_year = theRandomMovie.split('|')[1]

        d = {'Movie': [will_be_watched_movie], 'Production Year': [movie_production_year]}

        user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

        if os.path.exists('user_watch_list.csv'):

            boolean = False

        else:
            boolean = True

        user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

        messagebox.showinfo("WATCHLIST", f"{will_be_watched_movie} -> Added to WatchList ")

    add_watch_history = Button(newRandomWindows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                               relief=RAISED, command=watched_rec)
    add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

    add_watch_list = Button(newRandomWindows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                            relief=RAISED, command=random_watch_list)
    add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

    another_rec = Button(newRandomWindows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                         relief=RAISED, command=rec_another)
    another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


randomButton = Button(movieFrame, bg="black", fg="white", text='Random', font="Times 13 bold", borderwidth=2, bd=6,
                      relief=RAISED, command=RandomButtonFunc)
randomButton.place(relx=0.78, rely=0.46, relwidth=0.16, relheight=0.15)


                    ###########################################################
                    #######          CONTENT-BASED RECOMMENDATION      #######
                    ###########################################################


content_based = Frame(root, bg="#75CFB8", bd=8, relief=RAISED)
content_based.place(relx=0.42, rely=0.53, relwidth=0.55, relheight=0.432)

item_based_Label = Label(content_based, bg="#75CFB8", fg="black", text="CONTENT-BASED RECOMMENDATION",
                         font="Times 18 bold italic underline")
item_based_Label.place(relx=0.25, rely=0.001, relwidth=0.54, relheight=0.1)


    #####################
    ###   FUNCTIONS   ###
    #####################

## Director Function ##

def director_rec_function():

    if os.path.exists('user_complete_watch_history.csv'):

        df = pd.read_csv('user_complete_watch_history.csv').reset_index()

        df.drop('index',axis = 1,inplace = True)

        df.head()

        all_movies = pd.read_csv('cleaned_movies.csv').reset_index()

        all_movies.drop('index',axis = 1,inplace = True)

        all_movies.head()

        def clean_director_names(dataframe):

            dataframe['Director'] = dataframe['Director'].apply(lambda x: str(x).replace('Director:',''))

            dataframe['Director'] = dataframe['Director'].apply(lambda x: str(x).replace('Directors:',''))

            dataframe['Director'] = dataframe['Director'].apply(lambda x: str(x).replace('nan','Multiple Directors'))

            dataframe = dataframe[dataframe['Director'] != 'Multiple Directors']
            return dataframe


        clean_director_names(df)

        clean_director_names(all_movies)

        director_df = pd.pivot_table(values = 'User_Point', index = 'Director',data = df).sort_values(by = 'User_Point',ascending =False).reset_index()

        global favourite_director

        favourite_director = director_df.iloc[0]['Director']

        frames = [all_movies, df]

        movies = pd.concat(frames, ignore_index=True)

        movies.drop_duplicates(subset='Movie', keep=False, inplace=True)

        movies['Production Year']

        rec_movies_df = movies[movies['Director'] == favourite_director]

        for i in range(len(director_df)):

            if len(rec_movies_df) == 0:
                favourite_director = director_df.iloc[i]['Director']

        rec_movies_df = movies[movies['Director'] == favourite_director]

        rec_movies = rec_movies_df[['Movie', 'Production Year']].reset_index().drop('index', axis=1)

        recommend_director_movie = rec_movies.sample(1, ignore_index=True)

        recommend_director_movie = recommend_director_movie['Movie'] + ' | ' + recommend_director_movie[
            'Production Year']

        recommend_director_movie = str(recommend_director_movie.values).replace('[', '').replace(']', '').replace("'",
                                                                                                                  "")

        recommend_director_movie_name = recommend_director_movie.split("|")[0].rstrip()

        recommend_director_movie_year = recommend_director_movie.split("|")[1].lstrip()

        recommend_director_movie = recommend_director_movie_name + " | " + recommend_director_movie_year

        ### INTERFACE ###

        rec_by_director_windows= Toplevel(bg="#30475E")
        rec_by_director_windows.state("zoomed")
        rec_by_director_windows.title("Recommendation Based on Favourite Director")

        rec_by_director_label = Label(rec_by_director_windows, text=str("Recommended Movies"), bg="#FFC074", fg="black",
                                      font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        rec_by_director_label.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

        director_MovieArea = Text(rec_by_director_windows, height=10, width=50, borderwidth=5, bd=8, relief=RAISED)
        theRecMovie = "Favourite Director -> {}\n\nYou might like this movie  ->  {}".format(favourite_director,recommend_director_movie)

        director_MovieArea.tag_configure('style', font=('Verdana', 14))

        director_MovieArea.insert(END, theRecMovie, 'style')
        director_MovieArea.place(relx=0.3, rely=0.37, relwidth=0.45, relheight=0.19)



        def watched_director_rec():

            point_screen(recommend_director_movie)

            rec_by_director_windows.destroy()


        def rec_another_director_movie():

            director_rec_function()

            rec_by_director_windows.destroy()

        def director_watch_list():

            d = {'Movie': [recommend_director_movie_name], 'Production Year': [recommend_director_movie_year]}

            user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

            if os.path.exists('user_watch_list.csv'):

                boolean = False

            else:
                boolean = True

            user_df.drop_duplicates(subset = 'Movie', keep = 'last', inplace = True)

            user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)


            messagebox.showinfo("WATCHLIST",  f"{recommend_director_movie}  ->  Added to WatchList ")


        ### Watch History Button ###
        add_watch_history = Button(rec_by_director_windows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                                   relief=RAISED, command=watched_director_rec)
        add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Watch List Button ###

        add_watch_list = Button(rec_by_director_windows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                                relief=RAISED, command=director_watch_list)
        add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Recommend Another Movie Button ###

        another_rec = Button(rec_by_director_windows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                             relief=RAISED, command=rec_another_director_movie)
        another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)


    else:

        messagebox.showinfo("Watch History", "There is no Watch History!")




## Favourite Genres ##

def favourite_cat_rec_function():

    if os.path.exists('user_complete_watch_history.csv'):

        df = pd.read_csv('user_complete_watch_history.csv').reset_index()

        df.drop('index', axis=1, inplace=True)

        all_movies = pd.read_csv('cleaned_movies.csv').reset_index()

        all_movies.drop('index', axis=1, inplace=True)

        genres_df = pd.pivot_table(values='User_Point', index='Genres', data=df).sort_values(by='User_Point',ascending=False).reset_index()

        favourite_genres = genres_df.iloc[0]['Genres']

        frames = [all_movies, df]

        movies = pd.concat(frames,ignore_index=True)

        movies.drop_duplicates(subset = 'Movie',keep= False,inplace = True)

        rec_movies_df = movies[movies['Genres'] == favourite_genres]

        if len(rec_movies_df) == 0:
            favourite_genres = genres_df.iloc[1]['Genres']

        rec_movies_df = movies[movies['Genres'] == favourite_genres]

        rec_movies = rec_movies_df[['Movie', 'Production Year']].reset_index().drop('index', axis=1)

        global recommend_genres_movie

        recommend_genres_movie = rec_movies.sample(1, ignore_index=True)

        recommend_genres_movie = recommend_genres_movie['Movie'] + ' | ' + recommend_genres_movie['Production Year']

        recommend_genres_movie = str(recommend_genres_movie.values).replace('[', '').replace(']', '').replace("'", "")

        recommend_genres_movie_name = recommend_genres_movie.split("|")[0].rstrip()

        recommend_genres_movie_year = recommend_genres_movie.split("|")[1].lstrip()

        recommend_genres_movie = recommend_genres_movie_name + " | " + recommend_genres_movie_year

        ### INTERFACE ###

        rec_by_genres_windows= Toplevel(bg="#30475E")
        rec_by_genres_windows.state("zoomed")
        rec_by_genres_windows.title("Recommendation Based on Favourite Genres")

        rec_by_genres_label = Label(rec_by_genres_windows, text=str("Recommended Movies"), bg="#FFC074", fg="black",
                                      font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        rec_by_genres_label.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

        genres_MovieArea = Text(rec_by_genres_windows, height=10, width=55, borderwidth=5, bd=8, relief=RAISED)
        theGenreRecMovie = "Favourite Genres  ->  {}\n\nYou might like this movie  ->  {}".format(favourite_genres,recommend_genres_movie)

        genres_MovieArea.tag_configure('style', font=('Verdana', 14))

        genres_MovieArea.insert(END, theGenreRecMovie, 'style')
        genres_MovieArea.place(relx=0.3, rely=0.37, relwidth=0.45, relheight=0.19)


        def watched_genres_rec():

            point_screen(recommend_genres_movie)

            rec_by_genres_windows.destroy()


        def rec_another_genres_movie():

            favourite_cat_rec_function()

            rec_by_genres_windows.destroy()

        def genres_watch_list():

            d = {'Movie': [recommend_genres_movie_name], 'Production Year': [recommend_genres_movie_year]}

            user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

            if os.path.exists('user_watch_list.csv'):

                boolean = False

            else:
                boolean = True

            user_df.drop_duplicates(subset = 'Movie', keep = 'last', inplace = True)

            user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)


            messagebox.showinfo("WATCHLIST",  f"{recommend_genres_movie}  ->  Added to WatchList ")


        ### Watch History Button ###
        add_watch_history = Button(rec_by_genres_windows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                                   relief=RAISED, command=watched_genres_rec)
        add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Watch List Button ###

        add_watch_list = Button(rec_by_genres_windows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                                relief=RAISED, command=genres_watch_list)
        add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Recommend Another Movie Button ###

        another_rec = Button(rec_by_genres_windows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                             relief=RAISED, command=rec_another_genres_movie)
        another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)

    else:

        messagebox.showinfo("Watch History", "There is no Watch History!")


#### TF-IDF VECTORIZER ####

def calculate_cosine_sim(dataframe):

        tfidf = TfidfVectorizer(stop_words='english')
        dataframe['Description'] = dataframe['Description'].fillna('')
        tfidf_matrix = tfidf.fit_transform(dataframe['Description'])
        cosine_sim = cosine_similarity(tfidf_matrix)
        return cosine_sim

def content_based_recommender(title, cosine_sim, dataframe):

    indices = pd.Series(dataframe.index, index=dataframe['Movie'])
    indices = indices[~indices.index.duplicated(keep='last')]

    movie_index = indices[title]

    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])

    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
    return dataframe['Movie'].iloc[movie_indices]


#### Recommend a Movie Based on Last Movie #####

def rec_based_on_last_movie():

    if os.path.exists('user_complete_watch_history.csv'):

        df = pd.read_csv('cleaned_movies.csv')

        cosine_sim = calculate_cosine_sim(df)

        watch_history_df = pd.read_csv('user_watch_history.csv')

        last_movie = watch_history_df.iloc[-1]['Movie']

        last_movie = last_movie.split("|")[0].rstrip()

        recommended_movies = content_based_recommender(last_movie, cosine_sim, df)

        rand = random.randint(0, 10)

        recommended_movie = recommended_movies.iloc[rand]

        recommended_movie_year = df.loc[df['Movie'] == recommended_movie]['Production Year']

        recommended_movie_year = recommended_movie_year.iloc[0]

        movie_name_year = recommended_movie + ' | ' + recommended_movie_year

        ### INTERFACE ###

        rec_by_last_movie_windows = Toplevel(bg="#30475E")
        rec_by_last_movie_windows.state("zoomed")
        rec_by_last_movie_windows.title("Recommendation Based on Last Movie")

        rec_by_last_movie_label = Label(rec_by_last_movie_windows, text=str("Recommended Movies"), bg="#FFC074", fg="black",
                                    font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        rec_by_last_movie_label.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

        rec_by_last_MovieArea = Text(rec_by_last_movie_windows, height=10, width=55, borderwidth=5, bd=8, relief=RAISED)
        theLastRecMovie = "Last Movie ->  {}\n\nYou might like this movie  ->  {}".format(last_movie,
                                                                                            recommended_movie)

        rec_by_last_MovieArea.tag_configure('style', font=('Verdana', 14))

        rec_by_last_MovieArea.insert(END, theLastRecMovie, 'style')
        rec_by_last_MovieArea.place(relx=0.3, rely=0.37, relwidth=0.45, relheight=0.19)


        def last_watched_rec():
            point_screen(movie_name_year)

            rec_by_last_movie_windows.destroy()


        def rec_another_last_watched_movie():
            rec_based_on_last_movie()

            rec_by_last_movie_windows.destroy()


        def last_movie_watch_list():
            d = {'Movie': [recommended_movie], 'Production Year': [recommended_movie_year]}

            user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

            if os.path.exists('user_watch_list.csv'):

                boolean = False

            else:
                boolean = True

            user_df.drop_duplicates(subset='Movie', keep='last', inplace=True)

            user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

            messagebox.showinfo("WATCHLIST", f"{movie_name_year}  ->  Added to WatchList ")

            rec_by_last_movie_windows.destroy()

        ### Watch History Button ###
        add_watch_history = Button(rec_by_last_movie_windows, text="Watched", font="Times 16 bold", borderwidth=1, bd=6,
                                   relief=RAISED, command=last_watched_rec)
        add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Watch List Button ###

        add_watch_list = Button(rec_by_last_movie_windows, text="Will be watched", font="Times 15 bold", borderwidth=1, bd=6,
                                relief=RAISED, command=last_movie_watch_list)
        add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Recommend Another Movie Button ###

        another_rec = Button(rec_by_last_movie_windows, text="Recommend Another", font="Times 15 bold", borderwidth=1, bd=6,
                             relief=RAISED, command=rec_another_last_watched_movie)
        another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)

    else:

        messagebox.showinfo("Watch History", "There is no Watch History!")


### RECOMMEND A MOVIE BASED ON ALL WATCH HISTORY ###

def recommend_movie_based_on_choices():

    if os.path.exists('user_watch_history.csv'):

        watch_history_df = pd.read_csv('user_watch_history.csv')

        all_movie_list = []

        length = watch_history_df.shape[0]

        for i in range(0,length):

            movie = watch_history_df.iloc[i]['Movie'].split(' | ')[0].rstrip()

            all_movie_list.append(movie)

        all_rec_movies_list = []

        cosine_sim = calculate_cosine_sim(df)

        for i in range(len(all_movie_list)):

            recommended_movies = content_based_recommender(all_movie_list[i], cosine_sim, df)

            for j in range(len(recommended_movies)):

                recommended_movie = recommended_movies.iloc[j]

                all_rec_movies_list.append(recommended_movie)


        set_movies = set()
        duplicated = [x for x in all_rec_movies_list if x in set_movies or (set_movies.add(x) or False)]

        if len(duplicated) != 0:
            recommend_the_movie = random.choice(duplicated)

            recommend_the_movie_year = df.loc[df['Movie'] == recommend_the_movie]['Production Year']

            recommend_the_movie_year = recommend_the_movie_year.iloc[0]

            choice_movie_name_year = recommend_the_movie + ' | ' + recommend_the_movie_year

        else:
            recommend_the_movie = random.choice(all_rec_movies_list)

            recommend_the_movie_year = df.loc[df['Movie'] == recommend_the_movie]['Production Year']

            recommend_the_movie_year = recommend_the_movie_year.iloc[0]

            choice_movie_name_year = recommend_the_movie + ' | ' + recommend_the_movie_year

        ### INTERFACE ###

        rec_by_choices_windows = Toplevel(bg="#30475E")
        rec_by_choices_windows.state("zoomed")
        rec_by_choices_windows.title("Recommendation Based on Choices")

        rec_by_choices_label = Label(rec_by_choices_windows, text=str("Recommended Movies"), bg="#FFC074",
                                        fg="black",
                                        font="Times 17 bold underline", anchor='n', bd=10, relief=RAISED)

        rec_by_choices_label.place(relx=0.3, rely=0.4, relwidth=0.42, relheight=0.15)

        choice_MovieArea = Text(rec_by_choices_windows, height=10, width=55, borderwidth=5, bd=8, relief=RAISED)
        theChoiceMovie = "\nYou might like this movie  ->  {}".format(choice_movie_name_year)


        choice_MovieArea.tag_configure('style', font=('Verdana', 14))

        choice_MovieArea.insert(END, theChoiceMovie, 'style')
        choice_MovieArea.place(relx=0.3, rely=0.37, relwidth=0.45, relheight=0.19)

        def rec_by_choice_history():
            point_screen(choice_movie_name_year)

            rec_by_choices_windows.destroy()

        def rec_another_by_choices_movie():
            recommend_movie_based_on_choices()

            rec_by_choices_windows.destroy()

        def movie_based_on_watch_list():
            d = {'Movie': [recommend_the_movie], 'Production Year': [recommend_the_movie_year]}

            user_df = pd.DataFrame(data=d, columns=['Movie', 'Production Year'])

            if os.path.exists('user_watch_list.csv'):

                boolean = False

            else:
                boolean = True

            user_df.drop_duplicates(subset='Movie', keep='last', inplace=True)

            user_df.to_csv('user_watch_list.csv', index=False, mode='a', header=boolean, columns=user_df.columns)

            messagebox.showinfo("WATCHLIST", f"{choice_movie_name_year}  ->  Added to WatchList ")

            rec_by_choices_windows.destroy()

        ### Watch History Button ###
        add_watch_history = Button(rec_by_choices_windows, text="Watched", font="Times 16 bold", borderwidth=1,
                                   bd=6,
                                   relief=RAISED, command=rec_by_choice_history)
        add_watch_history.place(relx=0.24, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Watch List Button ###

        add_watch_list = Button(rec_by_choices_windows, text="Will be watched", font="Times 15 bold",
                                borderwidth=1, bd=6,
                                relief=RAISED, command=movie_based_on_watch_list)
        add_watch_list.place(relx=0.45, rely=0.61, relwidth=0.14, relheight=0.09)

        ### Recommend Another Movie Button ###

        another_rec = Button(rec_by_choices_windows, text="Recommend Another", font="Times 15 bold",
                             borderwidth=1, bd=6,
                             relief=RAISED, command=rec_another_by_choices_movie)
        another_rec.place(relx=0.66, rely=0.61, relwidth=0.14, relheight=0.09)

    else:

        messagebox.showinfo("Watch History", "There is no Watch History!")

##### Recommendation Based on Watched Movies #####
rec_by_watched_Button = Button(content_based, text="Recommend a Movie\n Based on My Choices", font="Times 15 italic bold",
                               borderwidth=1, bd=6, relief=RAISED,command =recommend_movie_based_on_choices)

rec_by_watched_Button.place(relx=0.06, rely=0.22, relwidth=0.36, relheight=0.25)

##### Recommendation Based on Director #####

rec_by_director_Button = Button(content_based, text="Recommend a Movie\n Based on My Favourite Director",
                                font="Times 15 italic bold", borderwidth=1, bd=6, relief=RAISED, command = director_rec_function)

rec_by_director_Button.place(relx=0.06, rely=0.58, relwidth=0.36, relheight=0.25)

##### Recommendation Based on Last Movie #####

rec_by_last_movie_Button = Button(content_based, text="Recommend a Movie\n Based on My Last Movie",
                                  font="Times 15 italic bold", borderwidth=1, bd=6, relief=RAISED,command = rec_based_on_last_movie)
rec_by_last_movie_Button.place(relx=0.55, rely=0.22, relwidth=0.36, relheight=0.25)

##### Recommendation Based on Favourite Genres #####

rec_by_fav_cat_Button = Button(content_based, text="Recommend a Movie Based on\n My Favourite Genres",
                               font="Times 15 italic bold", borderwidth=1, bd=6, relief=RAISED,command = favourite_cat_rec_function)
rec_by_fav_cat_Button.place(relx=0.55, rely=0.58, relwidth=0.36, relheight=0.25)

root.mainloop()
