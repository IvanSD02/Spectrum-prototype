from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import math
import random
#from functions import *
from book_manager.book import Book
from book_manager.movie import Movie
from book_manager.game import Game

general_books = []
general_movies = []
general_games = []


def print_listed():
    print_list_info()

def read_from_file(filename):
    movies = []
    inputs = []
    file = open(filename, 'r')
    for line in file:
        data = line.strip().split("|")
        inputs.append(data)
    file.close()
    return inputs

def add_to_file(filename, type):
    add = Tk()
    add.geometry("300x400")
    add.title("Add New Entry")
    add.config(bg="grey")
    top_label = Label(add, bg="white", text="Add "+type, font=("Helvetica", 15, "bold"), pady=10,
                      borderwidth=3, relief="ridge", bd=7, width=10)
    top_label.place(x=80, y=4)

    title_var = StringVar()
    genre_var = StringVar()
    year_var = StringVar()
    maker_var = StringVar()
    rating_var = StringVar()

    title_label = Label(add, text="Title: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black")
    title_label.place(x=40, y=80)
    title_entry = Entry(add, textvariable=title_var, borderwidth=5, relief="raised", highlightcolor="black")
    title_entry.place(x=130, y=80)

    genre_label = Label(add, text="Genre: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black")
    genre_label.place(x=40, y=120)
    genre_entry = Entry(add, textvariable=genre_var, borderwidth=5, relief="raised", highlightcolor="black")
    genre_entry.place(x=130, y=120)

    year_label = Label(add, text="Year: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black")
    year_label.place(x=40, y=160)
    year_entry = Entry(add, textvariable=year_var, borderwidth=5, relief="raised", highlightcolor="black")
    year_entry.place(x=130, y=160)

    if type=="Book":
        author_label = Label(add, text="Author: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black")
        author_label.place(x=40, y=200)
        author_entry = Entry(add, textvariable=maker_var, borderwidth=5, relief="raised", highlightcolor="black")
        author_entry.place(x=130, y=200)

        rating_label = Label(add, text="Rating: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black")
        rating_label.place(x=40, y=240)
        rating_entry = Entry(add, textvariable=rating_var, borderwidth=5, relief="raised", highlightcolor="black")
        rating_entry.place(x=130, y=240)

    if type=="Movie":
        director_label = Label(add, text="Director: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black")
        director_label.place(x=40, y=200)
        director_entry = Entry(add, textvariable=maker_var, borderwidth=5, relief="raised", highlightcolor="black")
        director_entry.place(x=130, y=200)

        rating_label = Label(add, text="Rating: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black")
        rating_label.place(x=40, y=240)
        rating_entry = Entry(add, textvariable=rating_var, borderwidth=5, relief="raised", highlightcolor="black")
        rating_entry.place(x=130, y=240)

    if type=="Game":
        creator_label = Label(add, text="Creator: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black")
        creator_label.place(x=40, y=200)
        creator_entry = Entry(add, textvariable=maker_var, borderwidth=5, relief="raised", highlightcolor="black")
        creator_entry.place(x=130, y=200)

        rating_label = Label(add, text="Rating: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black")
        rating_label.place(x=40, y=240)
        rating_entry = Entry(add, textvariable=rating_var, borderwidth=5, relief="raised", highlightcolor="black")
        rating_entry.place(x=130, y=240)

    add_button_add = Button(add, bg="wheat", bd=7, text="Add Entry", padx=13, pady=7, font=("Helvetica", 17, "bold"))
    add_button_add.place(x = 70, y = 300)

    newest_index = 0
    file = open(filename, 'r')
    for i in file:
        newest_index+=1

    file.close()

    def add_book(filename, newest_index):
        new_addition = open(filename, 'a')
        title = str(title_entry.get())
        year = str(year_entry.get())
        maker = str(author_entry.get())
        genre = str(genre_entry.get())
        rating = str(rating_entry.get())

        book = Book(title, maker, genre, year, rating)

        books = read_from_file("book_manager/books.txt")
        for ind in books:
            if len(ind)>0 and len(books)>0:
                if title == ind[1]:
                    messagebox.showinfo("Existing Entry", "This entry already exists!")
                    add.destroy()
                    return

        new_addition.write(str(newest_index) + "|")
        new_addition.write(book.title + "|")
        new_addition.write(book.author + "|")
        new_addition.write(book.genre + "|")
        new_addition.write(book.year_released + "|")
        new_addition.write(book.rating)
        new_addition.write("\n")
        new_addition.close()

    def add_movie(filename, newest_index):
        new_addition = open(filename, 'a')
        title = str(title_entry.get())
        year = str(year_entry.get())
        maker = str(director_entry.get())
        genre = str(genre_entry.get())
        rating = str(rating_entry.get())

        movie = Movie(title, maker, genre, year, rating)

        movies = read_from_file("book_manager/movies.txt")
        for ind in movies:
            if len(ind)>0 and len(movies)>0:
                if title == ind[1]:
                    messagebox.showinfo("Existing Entry", "This entry already exists!")
                    add.destroy()
                    return

        new_addition.write(str(newest_index) + "|")
        new_addition.write(movie.title + "|")
        new_addition.write(movie.director + "|")
        new_addition.write(movie.genre + "|")
        new_addition.write(movie.year_released + "|")
        new_addition.write(movie.rating)
        new_addition.write("\n")

        new_addition.close()

    def add_game(filename, newest_index):
        new_addition = open(filename, 'a')
        title = str(title_entry.get())
        year = str(year_entry.get())
        maker = str(creator_entry.get())
        genre = str(genre_entry.get())
        rating = str(rating_entry.get())

        game = Game(title, maker, genre, year, rating)

        games = read_from_file("book_manager/games.txt")
        for ind in games:
            if len(ind)>0 and len(games)>0:
                if title == ind[1]:
                    messagebox.showinfo("Existing Entry", "This entry already exists!")
                    add.destroy()
                    return

        new_addition.write(str(newest_index) + "|")
        new_addition.write(game.title + "|")
        new_addition.write(game.creator + "|")
        new_addition.write(game.genre + "|")
        new_addition.write(game.year_released + "|")
        new_addition.write(game.rating)
        new_addition.write("\n")
        new_addition.close()

    if type=="Book":
        add_button_add.config(command=lambda:[add_book("book_manager/books.txt", newest_index), showBoxBooks()])
        #messagebox.showinfo("Update","Successfully updated!")
    if type=="Movie":
        add_button_add.config(command=lambda: [add_movie("book_manager/movies.txt", newest_index), showBoxMovies()])

    if type=="Game":
        add_button_add.config(command=lambda: [add_game("book_manager/games.txt", newest_index), showBoxGames()])

    add.mainloop()

def update_file(filename, type):
    global listbox_list
    items = []
    current_item = listbox_list.get(ACTIVE)
    file = open(filename, 'r')
    for line in file:
        data = line.strip().split("|")
        if data[1]==current_item:
            items = data
    upd = Tk()
    upd.geometry("300x400")
    upd.title("Add New Entry")
    upd.config(bg="grey")
    top_label = Label(upd, bg="white", text="Update " + type, font=("Helvetica", 15, "bold"), pady=10,
                      borderwidth=3, relief="ridge", bd=7, width=12)
    top_label.place(x=70, y=4)

    title_var = StringVar()
    genre_var = StringVar()
    year_var = StringVar()
    maker_var = StringVar()
    rating_var = StringVar()

    title_label = Label(upd, text="Title: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black")
    title_label.place(x=40, y=80)
    title_entry = Entry(upd, textvariable=title_var, borderwidth=5, relief="raised", highlightcolor="black")
    title_entry.place(x=130, y=80)
    title_entry.insert(0, items[1])

    genre_label = Label(upd, text="Genre: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black")
    genre_label.place(x=40, y=120)
    genre_entry = Entry(upd, textvariable=genre_var, borderwidth=5, relief="raised", highlightcolor="black")
    genre_entry.place(x=130, y=120)
    genre_entry.insert(0, items[3])

    year_label = Label(upd, text="Year: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                       relief="raised", highlightcolor="black")
    year_label.place(x=40, y=160)
    year_entry = Entry(upd, textvariable=year_var, borderwidth=5, relief="raised", highlightcolor="black")
    year_entry.place(x=130, y=160)
    year_entry.insert(0, items[4])

    if type == "Book":
        author_label = Label(upd, text="Author: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                             relief="raised", highlightcolor="black")
        author_label.place(x=40, y=200)
        author_entry = Entry(upd, textvariable=maker_var, borderwidth=5, relief="raised", highlightcolor="black")
        author_entry.place(x=130, y=200)
        author_entry.insert(0, items[2])

        rating_label = Label(upd, text="Rating: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                             relief="raised", highlightcolor="black")
        rating_label.place(x=40, y=240)
        rating_entry = Entry(upd, textvariable=rating_var, borderwidth=5, relief="raised", highlightcolor="black")
        rating_entry.place(x=130, y=240)
        rating_entry.insert(0, items[5])

    if type == "Movie":
        director_label = Label(upd, text="Director: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                               relief="raised", highlightcolor="black")
        director_label.place(x=40, y=200)
        director_entry = Entry(upd, textvariable=maker_var, borderwidth=5, relief="raised", highlightcolor="black")
        director_entry.place(x=130, y=200)
        director_entry.insert(0, items[2])

        rating_label = Label(upd, text="Rating: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                             relief="raised", highlightcolor="black")
        rating_label.place(x=40, y=240)
        rating_entry = Entry(upd, textvariable=rating_var, borderwidth=5, relief="raised", highlightcolor="black")
        rating_entry.place(x=130, y=240)
        rating_entry.insert(0, items[5])

    if type == "Game":
        creator_label = Label(upd, text="Creator: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                              relief="raised", highlightcolor="black")
        creator_label.place(x=40, y=200)
        creator_entry = Entry(upd, textvariable=maker_var, borderwidth=5, relief="raised", highlightcolor="black")
        creator_entry.place(x=130, y=200)
        creator_entry.insert(0, items[2])

        rating_label = Label(upd, text="Rating: ", font=("Helvetica", 13, "bold"), borderwidth=5,
                             relief="raised", highlightcolor="black")
        rating_label.place(x=40, y=240)
        rating_entry = Entry(upd, textvariable=rating_var, borderwidth=5, relief="raised", highlightcolor="black")
        rating_entry.place(x=130, y=240)
        rating_entry.insert(0, items[5])

    update_button_add = Button(upd, bg="wheat", bd=7, text="Update Entry", padx=13, pady=7, font=("Helvetica", 15, "bold"))
    update_button_add.place(x=70, y=300)

    newest_index = 0
    file = open(filename, 'r')
    get_all = file.readlines()
    for i in file:
        newest_index += 1

    file.close()
    inputs_new = []
    for line in get_all:
        data = line.strip().split("|")
        inputs_new.append(data)
   # print(inputs_new)
    def add_book(filename, newest_index):
        new_addition = open(filename, 'w')
        title = str(title_entry.get())
        year = str(year_entry.get())
        maker = str(author_entry.get())
        genre = str(genre_entry.get())
        rating = str(rating_entry.get())

        book = Book(title, maker, genre, year, rating)
        #books = read_from_file("books.txt")
        for i in range (0, len(get_all)):
            data = inputs_new[i]
            if title==data[1]:
                new_addition.write(str(data[0]) + "|")
                new_addition.write(book.title + "|")
                new_addition.write(book.author + "|")
                new_addition.write(book.genre + "|")
                new_addition.write(book.year_released + "|")
                new_addition.write(book.rating)
                new_addition.write("\n")
            else:
                new_addition.write(get_all[i])
        new_addition.close()

    def add_movie(filename, newest_index):
        new_addition = open(filename, 'w')
        title = str(title_entry.get())
        year = str(year_entry.get())
        maker = str(director_entry.get())
        genre = str(genre_entry.get())
        rating = str(rating_entry.get())

        movie = Movie(title, maker, genre, year, rating)
        for i in range (0, len(get_all)):
            data = inputs_new[i]
            if title==data[1]:
                new_addition.write(str(data[0]) + "|")
                new_addition.write(movie.title + "|")
                new_addition.write(movie.director + "|")
                new_addition.write(movie.genre + "|")
                new_addition.write(movie.year_released + "|")
                new_addition.write(movie.rating)
                new_addition.write("\n")
            else:
                new_addition.write(get_all[i])
        new_addition.close()

    def add_game(filename, newest_index):
        new_addition = open(filename, 'w')
        title = str(title_entry.get())
        year = str(year_entry.get())
        maker = str(creator_entry.get())
        genre = str(genre_entry.get())
        rating = str(rating_entry.get())

        game = Game(title, maker, genre, year, rating)

        for i in range(0, len(get_all)):
            data = inputs_new[i]
            if title == data[1]:
                new_addition.write(str(data[0]) + "|")
                new_addition.write(game.title + "|")
                new_addition.write(game.creator + "|")
                new_addition.write(game.genre + "|")
                new_addition.write(game.year_released + "|")
                new_addition.write(game.rating)
                new_addition.write("\n")
            else:
                new_addition.write(get_all[i])
        new_addition.close()

    if type == "Book":
        update_button_add.config(command=lambda: [add_book("book_manager/books.txt", newest_index), print_list_info()])
    if type == "Movie":
        update_button_add.config(command=lambda: [add_movie("book_manager/movies.txt", newest_index), print_list_info()])
    if type == "Game":
        update_button_add.config(command=lambda: [add_game("book_manager/games.txt", newest_index), print_list_info()])

    upd.mainloop()

def delete_file(filename, type):
    global listbox_list
    current_item = listbox_list.get(ACTIVE)

    file = open(filename,'r')
    get_all = file.readlines()
    file.close()

    inputs_new = []
    for line in get_all:
        data = line.strip().split("|")
        inputs_new.append(data)

    new_addition = open(filename, 'w')
    for i in range(0, len(get_all)):
        data = inputs_new[i]
        if data[1] == current_item:
            continue
        else:
            new_addition.write(str(i) + "|")
            new_addition.write(data[1] + "|")
            new_addition.write(data[2]+ "|")
            new_addition.write(data[3] + "|")
            new_addition.write(data[4] + "|")
            new_addition.write(data[5])
            new_addition.write("\n")

    new_addition.close()
    listbox_list.delete(0, END)
    for widgets in data_frame_lower_right.winfo_children():
        widgets.destroy()
    if type=="Book":
        books = read_from_file("book_manager/books.txt")
        general_books.pop(current_item)
        for book in books:
            listbox_list.insert(END, book[1])
    if type=="Movie":
        movies = read_from_file("book_manager/movies.txt")
        general_movies.pop(current_item)
        for movie in movies:
            listbox_list.insert(END, movie[1])
    if type == "Game":
        games = read_from_file("book_manager/games.txt")
        general_games.pop(current_item)
        for game in games:
            listbox_list.insert(END, game[1])

mng = Tk()
mng.geometry("900x630")
mng.title("Collection Manager")
mng.config(bg = "powder blue")

menu_bar = Menu(mng)
mng.config(menu=menu_bar)
file_menu = Menu(mng, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_separator()
file_menu.add_command(
    label='Close',
    command = mng.destroy,
)

top_label = Label(mng, bg="white", text="Collection Manager", font=("Times New Roman",19, "bold"), pady=10,
             borderwidth=3, relief="ridge", bd=7, width=58)
top_label.place(x=7, y=4)

var_1 = IntVar()

data_frame = Frame(mng, bd=20, width=900, height=450, relief=RIDGE)
data_frame.place(x=0, y=150)

data_frame_left = LabelFrame(data_frame, bd=10, width=300,height=410, relief=RIDGE, font=('arial', 12, 'bold'), padx=2, pady=2)
data_frame_left.pack(side=LEFT)

data_frame_right = LabelFrame(data_frame, bd=10, width=510,height=410, relief=RIDGE, font=('arial', 12, 'bold'), padx=2, pady=2)
data_frame_right.pack(side=RIGHT)

data_frame_upper_right = LabelFrame(data_frame_right, bd=3, width=510,height=50, relief=RIDGE, font=('arial', 12, 'bold'), padx=2, pady=2)
data_frame_upper_right.pack(side=TOP)
data_frame_upper_right.pack_propagate(False)

data_frame_lower_right = LabelFrame(data_frame_right, bd=3, width=510,height=360, relief=RIDGE, font=('arial', 12, 'bold'), padx=2, pady=2)
data_frame_lower_right.pack(side=BOTTOM)
data_frame_lower_right.grid_propagate(False)

data_frame_upper_left = LabelFrame(data_frame_left, bd=3, width=300,height=360, relief=RIDGE, font=('arial', 12, 'bold'), padx=2, pady=2)
data_frame_upper_left.pack(side=TOP)
listbox_list = Listbox(data_frame_upper_left, width=30, height=19, font=('arial', 12, 'bold'), bd=2, borderwidth=2, activestyle=NONE)
listbox_list.pack(side=LEFT)

#data_frame_lower_left = LabelFrame(data_frame_left, bd=3, width=300,height=50, relief=RIDGE, font=('arial', 12, 'bold'), padx=2, pady=2)
search_str = StringVar()
search = Entry(data_frame_left, textvariable=search_str, width=10)
search.pack(side=BOTTOM)

scrollbar = Scrollbar(data_frame_upper_left)
scrollbar.pack(side=RIGHT)
listbox_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_list.yview)

add_button = Button(data_frame_upper_right, width=10, bg="#FFF772", bd=6, text="Add Entry",font=("Helvetica", 12, "bold"))
update_button = Button(data_frame_upper_right, width=10, bg="#FFF772", bd=6, text="Update Entry",font=("Helvetica", 12, "bold"))
delete_button = Button(data_frame_upper_right, width=10, bg="#FFF772", bd=6, text="Delete Entry",font=("Helvetica", 12, "bold"))

def showBoxBooks():
    listbox_list.delete(0, END)
    books = read_from_file("book_manager/books.txt")
    for book in books:
        listbox_list.insert(END, book[1])
        general_books.append(book)
    add_button.config(command=lambda:[add_to_file("book_manager/books.txt", "Book")])
    update_button.config(command=lambda:[update_file("book_manager/books.txt", "Book")])
    delete_button.config(command=lambda:[delete_file("book_manager/books.txt", "Book")])

def showBoxMovies():
    listbox_list.delete(0, END)
    movies = read_from_file("book_manager/movies.txt")
    for movie in movies:
        listbox_list.insert(END, movie[1])
        general_movies.append(movie)
    add_button.config(command=lambda: add_to_file("book_manager/movies.txt", "Movie"))
    update_button.config(command=lambda: [update_file("book_manager/movies.txt", "Movie")])
    delete_button.config(command=lambda: [delete_file("book_manager/movies.txt", "Movie")])

def showBoxGames():
    listbox_list.delete(0, END)
    games = read_from_file("book_manager/games.txt")
    for game in games:
        listbox_list.insert(END, game[1])
        general_games.append(game)
    add_button.config(command=lambda: add_to_file("book_manager/games.txt", "Game"))
    update_button.config(command=lambda: [update_file("book_manager/games.txt", "Game")])
    delete_button.config(command=lambda: [delete_file("book_manager/games.txt", "Game")])


books_rad = Radiobutton(mng, text="Books",padx = 20,variable=var_1,value=1, bg="wheat", font=("Helvetica", 15, "bold"), pady=10, borderwidth=3, relief="groove", command=lambda:showBoxBooks())
books_rad.place(x=100, y=80)

movies_rad = Radiobutton(mng, text="Movies",padx = 20,variable=var_1,value=2, bg="wheat", font=("Helvetica", 15, "bold"), pady=10, borderwidth=3, relief="groove", command=lambda:showBoxMovies())
movies_rad.place(x=380, y=80)

games_rad = Radiobutton(mng, text="Games",padx = 20,variable=var_1,value=3, bg="wheat", font=("Helvetica", 15, "bold"), pady=10, borderwidth=3, relief="groove", command=lambda:showBoxGames())
games_rad.place(x=670, y=80)

def print_list_info():
    global listbox_list
    for widgets in data_frame_lower_right.winfo_children():
        widgets.destroy()
    current_item = listbox_list.get(ACTIVE)
    current_list = var_1.get()
    item_attributes = []
    if current_list == 1:
        current_file = open("book_manager/books.txt", 'r')
        for line in current_file:
            data = line.strip().split("|")
            if(data[1]==current_item):
                item_attributes = data
    if current_list == 2:
        current_file = open("book_manager/movies.txt", 'r')
        for line in current_file:
            data = line.strip().split("|")
            if(data[1]==current_item):
                item_attributes = data
    if current_list == 3:
        current_file = open("book_manager/games.txt", 'r')
        for line in current_file:
            data = line.strip().split("|")
            if(data[1]==current_item):
                item_attributes = data
    print(item_attributes)
    grid_frame = Frame(data_frame_lower_right)
    grid_frame.place(x=170, y=50)
    title_label = Label(grid_frame, text="Title: " + item_attributes[1], font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black").grid(row=0, column=0)
    year_label = Label(grid_frame, text="Year Released: " + item_attributes[4], font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black").grid(row=3, column=0)
    genre_label = Label(grid_frame, text="Genre: " + item_attributes[3] , font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black").grid(row=2, column=0)
    rating_label = Label(grid_frame, text="Rating: " + item_attributes[5], font=("Helvetica", 13, "bold"), borderwidth=5,
                        relief="raised", highlightcolor="black").grid(row=4, column=0)
    if current_list == 1:
        author_label = Label(grid_frame, text="Author: " + item_attributes[2], font=("Helvetica", 13, "bold"), borderwidth=5,
                            relief="raised", highlightcolor="black").grid(row=1, column=0)
    if current_list == 2:
        director_label = Label(grid_frame, text="Director: " + item_attributes[2], font=("Helvetica", 13, "bold"), borderwidth=5,
                             relief="raised", highlightcolor="black").grid(row=1, column=0)
    if current_list == 3:
        creator_label = Label(grid_frame, text="Creator: " + item_attributes[2], font=("Helvetica", 13, "bold"), borderwidth=5,
                             relief="raised", highlightcolor="black").grid(row=1, column=0)

def buttons(event):
    data_frame_upper_right.config(bg="snow")
    add_button.place(x=0, y=0)

    update_button.place(x=191, y=0)
    delete_button.place(x=392, y=0)
    print_list_info()

def filtered_search(event):
    general_list = []
    current_list = var_1.get()
    if current_list == 1:
        current_file = open("book_manager/books.txt", 'r')
        for line in current_file:
            data = line.strip().split("|")
            general_list.append(data[1])
    if current_list == 2:
        current_file = open("book_manager/movies.txt", 'r')
        for line in current_file:
            data = line.strip().split("|")
            general_list.append(data[1])
    if current_list == 3:
        current_file = open("book_manager/games.txt", 'r')
        for line in current_file:
            data = line.strip().split("|")
            general_list.append(data[1])

    sstr = search_str.get()
    listbox_list.delete(0, END)

    filtered_data = []

    for item in general_list:
        if sstr in item:
            filtered_data.append(item)
    print(filtered_data)
    for item in filtered_data:
        listbox_list.insert(END, item)

listbox_list.bind('<Double-1>', buttons)
search.bind('<Return>', filtered_search)

mng.mainloop()



