import pandas as pd
import tkinter as tk

# Goals:

    # Create a graphical user interface (GUI) using Tkinter

    # Allow the user to:

        # Select a movie genre from a dropdown menu

        # Select a maximum movie duration from a dropdown menu

        # Load movie data from an IMDb dataset

        # Filter movies based on the user's selections

        # Randomly pick one matching movie
        
        # Display the movie's title, genre, duration, and description in the app

class MyGUI():
    # Creating the app
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg='#f9f1f0')
        self.root.geometry('600x500')
        
        self.label = tk.Label(self.root, text='MOVIE PICKER', font=('Cooper Black',18))
        self.label.configure(bg='#f9f1f0')
        self.label.pack(padx=10,pady=10)

        self.lista_generos = ['Action', 'Comedy', 'Horror', 'Drama', 'Adventure',
                        'Sci-Fi', 'Biography', 'History', 'War', 'Crime',
                        'Romance', 'Fantasy', 'Mystery', 'Thriller', 'Sport',
                        'Music', 'Documentary']
        
        self.lista_duracao = [x for x in range (60,220,20)]

        self.generos = tk.StringVar()
        self.generos.set('Choose a genre')

        self.duracao = tk.StringVar()
        self.duracao.set('Choose max duration of the movie')

        self.escolha_gen = tk.OptionMenu(self.root, self.generos, *self.lista_generos)
        self.escolha_gen.configure(height=2, width=30, font=('Futura Bk BT',12), bg='#c8b4d0')
        self.escolha_gen.pack(padx=5, pady=5)
        
        self.escolha_dur = tk.OptionMenu(self.root, self.duracao, *self.lista_duracao)
        self.escolha_dur.configure(height=2, width=30, font=('Futura Bk BT',12), bg='#c8b4d0')
        self.escolha_dur.pack(padx=5, pady=5)
        
        self.button = tk.Button(self.root, text='Find a movie', font=('Futura Bk BT',12), command=self.escolher_filme)
        self.button.configure(height=2, width=20, bg='#c8b4d0')
        self.button.pack(padx=5,pady=5)

        self.moviepick = None

        self.root.mainloop()

    def escolher_filme(self):
        # Uploading dataset
        data_set = pd.read_csv('imdb-movies-dataset.csv')

        # Deleting columns that won't be used
        df = data_set[['Title','Year','Duration (min)','Genre','Rating','Description']] 

        # Cleaning and preprossecing the data
        df = df.dropna()

        df['Year'] = df['Year'].astype(int)
        df['Duration (min)'] = df['Duration (min)'].astype(int)
        df['Genre'] = df['Genre'].astype('string')
        df['Genre'].str.split(',', expand=True)

        # Getting the users paramaters
        genre = self.generos.get()

        time = int(self.duracao.get())

        # Creating new dataframe based on the users parameters
        df_choices = df[df['Duration (min)']<time]
        df_choices = df_choices[df_choices['Genre'].str.contains(genre)]

        # Choosing movie randomly
        pd.set_option("display.max_colwidth", None)
        if df_choices.empty:
            resultado_final = "No movies were found with these parameters."
        else:
            resultado1 = df_choices.sample(1)
            resultado_final = (
                'You should watch: ' + resultado1['Title'].to_string(index=False) +
                '\n\n Genre: ' + resultado1['Genre'].to_string(index=False) +
                '\n\n Duration: ' + resultado1['Duration (min)'].to_string(index=False) + ' min' +
                '\n\n Description: ' + resultado1['Description'].to_string(index=False)
            )

        # Refreshing the app
        if self.moviepick:
            self.moviepick.destroy()

        # Printing movie
        self.moviepick = tk.Label(self.root, text=resultado_final, font=('Futura Bk BT',12),
                               bg='#f9f1f0', wraplength=500, justify='left')
        self.moviepick.pack(pady=10, fill="both", expand=True)

MyGUI()