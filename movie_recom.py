import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import messagebox
# comment 2
# Load datasets
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# Merge datasets and clean the data
merged_data = pd.merge(ratings, movies, on="movieId", how='left').drop(['userId', 'timestamp'], axis=1).set_index('title').dropna(subset=['genres'])

# Extract unique genres
genre_col = pd.DataFrame(merged_data['genres'].unique())

# Function to get the first genre
def get_first_genre(genre):
    genres_list = genre.split('|')
    return genres_list[0] if genres_list else None

genre_col['new'] = genre_col[0].apply(get_first_genre)

# Function to check if the genre matches the user input
def is_genre_matching(genre, g_movie):
    return g_movie if (g_movie in genre.split('|')) else None

# Function to get movie recommendations
def get_recommendations():
    g_movie = genre_listbox.get(tk.ACTIVE)  # Get selected genre from Listbox
    no_movies = number_entry.get()

    # Validate number of movies input
    try:
        no_movies = int(no_movies)
        if no_movies <= 0:
            raise ValueError("Please enter a positive integer.")
    except ValueError as e:
        messagebox.showerror("Input Error", f"Invalid number of movies: {e}")
        return

    # Check if a genre is selected
    if g_movie == "":
        messagebox.showerror("Input Error", "Please select a genre from the list.")
        return

    merged_data['genres2'] = merged_data['genres'].apply(lambda x: is_genre_matching(x, g_movie))
    filtered_movies = merged_data[merged_data['genres2'] == g_movie]

    # Display the recommended movies
    if not filtered_movies.empty:
        recommended_movies = filtered_movies.drop(['movieId', 'genres2'], axis=1).drop_duplicates().sort_values('rating', ascending=False).head(no_movies)
        result_text = recommended_movies.to_string()  # Convert DataFrame to string for display
    else:
        result_text = "No movies found for the selected genre."

    # Show results in a message box
    messagebox.showinfo("Recommended Movies", result_text)

# Create the main window
root = tk.Tk()
root.title("Movie Recommendation System")

# Create labels and Listbox for genres
tk.Label(root, text="Select Genre:").pack(pady=5)
genre_listbox = tk.Listbox(root, height=10, width=30)
for genre in genre_col['new'].unique():
    genre_listbox.insert(tk.END, genre)  # Add genres to the Listbox
genre_listbox.pack(pady=5)

# Create label and entry field for number of movies
tk.Label(root, text="Number of Movies:").pack(pady=5)
number_entry = tk.Entry(root)
number_entry.pack(pady=5)

# Create a button to get recommendations
recommend_button = tk.Button(root, text="Get Recommendations", command=get_recommendations)
recommend_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
# commiting to git