import numpy as np
from sentence_transformers import SentenceTransformer
import json  # Add this import

# Load the model
model = SentenceTransformer("E:/Models/arabert")

# Load video data from JSON file
with open("temp db.json", "r", encoding="utf-8") as file:
    video_data = json.load(file)

# Extract titles and descriptions
video_titles = [video["title"] for video in video_data]
video_descriptions = [video["description"] for video in video_data]

# Combine titles and descriptions for better embeddings
video_texts = [f"{title} {description}" for title, description in zip(video_titles, video_descriptions)]

# Generate embeddings for combined texts
video_embeddings = model.encode(video_texts)
# Save the data for later use
np.save("E:/Models/video_titles.npy", video_titles)
np.save("E:/Models/video_embeddings.npy", video_embeddings)

print("\n تم حفظ تمثيلات الفيديوهات بنجاح!")