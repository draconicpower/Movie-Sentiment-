import requests
import json


def Getid(name):

    url = f"https://api.themoviedb.org/3/search/movie?query={name}&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzkxMTZhYzg0MTBjNjFiYmU4OTQ3ZDA4YWFlOGEyNyIsInN1YiI6IjY2MTdhZDhjZDhmNDRlMDEzMDJlMjRkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9T9-Io6pZJke6ont3Q-MvfZwRuFtRC-bX2d_dIOdpbE"
    }
    
    try:
        response = requests.get(url, headers=headers)
        results = response.json().get('results', [])
        if not results:
            return None
        return results[0]['id']
    except (requests.RequestException, KeyError, IndexError) as e:
        print(f"Error fetching movie ID: {e}")
        return None


import requests

def GetDetails(movie_id):
    # Define the base URL
    base_url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews"

    # Headers including your Bearer token
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzkxMTZhYzg0MTBjNjFiYmU4OTQ3ZDA4YWFlOGEyNyIsInN1YiI6IjY2MTdhZDhjZDhmNDRlMDEzMDJlMjRkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9T9-Io6pZJke6ont3Q-MvfZwRuFtRC-bX2d_dIOdpbE"
    }

    # List to store review contents
    Words = []
    page = 1  # Start with the first page

    while True:
        # Send the GET request with the current page
        response = requests.get(base_url, headers=headers, params={'page': page})

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Extract review data from response
            data = response.json()
            all_reviews = data.get('results', [])

            # If no reviews found, break the loop
            if not all_reviews:
                break

            # Extract review contents from collected reviews
            for review in all_reviews:
                Words.append(review['content'])

            # Check if there are more pages
            if page >= data['total_pages']:
                break

            # Increment the page number to get the next page
            page += 1
        else:
            # If request was not successful, return an empty list
            print(f"Failed to fetch reviews for movie ID: {movie_id}. Status code: {response.status_code}")
            return []

    return Words



def GetImage(Id):
    url = f"https://api.themoviedb.org/3/movie/{Id}/images?include_image_language=en&language=en"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzkxMTZhYzg0MTBjNjFiYmU4OTQ3ZDA4YWFlOGEyNyIsInN1YiI6IjY2MTdhZDhjZDhmNDRlMDEzMDJlMjRkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9T9-Io6pZJke6ont3Q-MvfZwRuFtRC-bX2d_dIOdpbE"
    }

    response = requests.get(url, headers=headers)
    return response.json()


def GetPoster(image):
    images = image['backdrops']
    middle_index = len(images) // 2
    photopath = images[middle_index]['file_path']
    url = f"https://image.tmdb.org/t/p/w500/{photopath}"
    return url


def GetKeywords(id):
    url = f"https://api.themoviedb.org/3/movie/{id}/keywords"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzkxMTZhYzg0MTBjNjFiYmU4OTQ3ZDA4YWFlOGEyNyIsInN1YiI6IjY2MTdhZDhjZDhmNDRlMDEzMDJlMjRkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9T9-Io6pZJke6ont3Q-MvfZwRuFtRC-bX2d_dIOdpbE"
    }

    response = requests.get(url, headers=headers)
    Keywords = response.json()
    comments = []

    if 'keywords' in Keywords:
        for keyword in Keywords['keywords']:
            comments.append(keyword['name'])

    return comments


def GetTrailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2YzkxMTZhYzg0MTBjNjFiYmU4OTQ3ZDA4YWFlOGEyNyIsInN1YiI6IjY2MTdhZDhjZDhmNDRlMDEzMDJlMjRkMSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.9T9-Io6pZJke6ont3Q-MvfZwRuFtRC-bX2d_dIOdpbE"
    }

    response = requests.get(url, headers=headers)
    data = response.json() # Parse the JSON response
    base_url = "https://www.youtube.com/watch?v=" # Base URL for YouTube videos

    
    if "results" in data: # Check if results are present in the data
        results = data["results"]
        
        
        for video in results: # Iterate through results to find the first official trailer
            
            if video.get("site") == "YouTube" and video.get("type") == "Trailer": # Check if the video is from YouTube and is a trailer
                
                video_key = video.get("key") # Retrieve the key of the trailer
                
                
                video_link = f"{base_url}{video_key}" # Construct the YouTube link
                

                return video_link  # Return the YouTube link
        
    
    return None # If no trailer is found, return None
