
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load the dataset
movies = pd.read_csv('dataset.csv')

# Select relevant columns
movies = movies[['id', 'title', 'overview', 'genre']]

# Create tags
movies['tags'] = movies['overview'].fillna('') + movies['genre'].fillna('')

# Create new dataframe
new_data = movies.drop(columns=['overview', 'genre'])

# Vectorize the tags
cv = CountVectorizer(max_features=10000, stop_words='english')
vector = cv.fit_transform(new_data['tags'].values.astype('U')).toarray()

# Calculate similarity
similarity = cosine_similarity(vector)

# Save the pickle files
pickle.dump(new_data, open('movies_list_pkl', 'wb'))
pickle.dump(similarity, open('similarity_pkl', 'wb'))

print("Pickle files generated successfully.")
