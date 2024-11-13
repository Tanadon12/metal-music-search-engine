import requests
import base64
import json
import time

SPOTIFY_CLIENT_ID = '16996ca203e34af587ce8fabc27954af'
SPOTIFY_CLIENT_SECRET = 'f160f5dc10f543a8b21e93b59404b05a'

def get_spotify_access_token():
    """Get access token from Spotify API."""
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(
            (SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode()
        ).decode()
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to fetch Spotify access token')

def search_spotify_song(query, access_token):
    """Search for a song on Spotify."""
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'q': query,
        'type': 'track',
        'limit': 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        items = response.json()['tracks']['items']
        return items[0] if items else {}
    else:
        return {}

def get_lyrics_from_lyrics_ovh(song_title, artist):
    """Fetch song lyrics from Lyrics.ovh API."""
    base_url = "https://api.lyrics.ovh/v1"
    response = requests.get(f"{base_url}/{artist}/{song_title}")
    
    if response.status_code == 200:
        data = response.json()
        return data.get("lyrics", "Lyrics not found.")
    else:
        return "Lyrics not found."

def clean_song_data(combined_data):
    """Extract and clean relevant song information."""
    spotify_data = combined_data.get('spotify', {})
    lyrics_data = combined_data.get('lyrics', {})

    return {
        'Song Query': combined_data.get('song_name', 'Unknown Query'),
        'Track Name': spotify_data.get('name', 'Unknown Song'),
        'Artist/Band': spotify_data.get('artists', [{}])[0].get('name', 'Unknown Artist'),
        'Duration': f"{spotify_data.get('duration_ms', 0) // 60000}:{(spotify_data.get('duration_ms', 0) % 60000) // 1000:02d}",
        'Release Date': spotify_data.get('album', {}).get('release_date', 'Unknown Date'),
        'Image': spotify_data.get('album', {}).get('images', [{}])[0].get('url', 'No Image'),
        'Type': spotify_data.get('type', 'Unknown Type'),
        'Album Name': spotify_data.get('album', {}).get('name', 'Unknown Album'),
        'Lyrics': lyrics_data.get('lyrics', 'Lyrics not available')
    }

def fetch_song_data(query):
    """Fetch data from Spotify and Lyrics.ovh APIs."""
    spotify_token = get_spotify_access_token()
    spotify_data = search_spotify_song(query, spotify_token)
    
    if spotify_data:
        song_title = spotify_data['name']
        artist_name = spotify_data['artists'][0]['name']
        lyrics = get_lyrics_from_lyrics_ovh(song_title, artist_name)
    else:
        song_title = query
        artist_name = "Unknown"
        lyrics = "No data from Spotify."

    combined_data = {
        'song_name': query,
        'spotify': spotify_data,
        'lyrics': {
            'title': song_title,
            'artist': artist_name,
            'lyrics': lyrics
        }
    }

    # Remove songs without valid lyrics
    if "Lyrics not found." in lyrics or "No data from Spotify." in lyrics:
        return None

    return clean_song_data(combined_data)

# List of metal songs
# List of metal songs
metal_songs = [
    "Master of Puppets", "Hallowed Be Thy Name", "Iron Man", "Painkiller", "One",
    "Holy Wars... The Punishment Due", "The Trooper", "Angel of Death", "War Pigs",
    "Fade to Black", "Raining Blood", "Breaking the Law", "Black Sabbath",
    "Symphony of Destruction", "Aces High", "The Number of the Beast", "Walk",
    "Battery", "Caught in a Mosh", "Cowboys from Hell", "Sweating Bullets",
    "For Whom the Bell Tolls", "Children of the Grave", "Seek & Destroy",
    "Kashmir", "Paranoid", "Peace Sells", "Fear of the Dark", "Fight Fire with Fire",
    "Nightmare", "Ace of Spades", "Am I Evil?", "Man in the Box", "Rainbow in the Dark",
    "Dreams of Eschaton", "Metal Meltdown", "The Heretic Anthem", "Run to the Hills",
    "Ashes of the Wake", "Enter Sandman", "Orion", "Revolution Is My Name", "Stillborn",
    "Domination", "The Sentinel", "Hammer Smashed Face", "Painkiller",
    "March of the Fire Ants", "Pledge Your Allegiance", "Immigrant Song", "Blackened",
    "Symphony of Destruction", "God of Thunder", "Disciple", "Bloodline", "Refuse/Resist",
    "Headcrusher", "Schism", "Leper Messiah", "Spit Out the Bone", "Walk with Me in Hell",
    "Beyond the Black", "Electric Eye", "Bleed", "Roots Bloody Roots", "In Waves",
    "Pull Me Under", "Wait and Bleed", "Sad But True", "Ghost Walking", "Bitter Peace",
    "Spirit Crusher", "Prayer", "The End of Heartache", "Spheres of Madness",
    "My Last Serenade", "Enemy", "Before I Forget", "World So Cold", 
    "Welcome Home (Sanitarium)", "Unholy Confessions", "Tears Don’t Fall", "This Love",
    "St. Anger", "Cold Sweat", "I'm Broken", "Death Church", "Mouth for War", "Roots",
    "Demon Cleaner", "Dead Skin Mask", "Twilight of the Thunder God", "Indians",
    "Screaming for Vengeance", "Into the Void", "Through the Never", "Desperate Cry",
    "The Evil That Men Do", "Deliverance", "Heavy Metal", "Killing in the Name", "Duality",
    "Angel of Death", "People = Shit", "Hail and Kill", "Master of Disguise", "Nemesis",
    "End of All Hope", "Down with the Sickness", "Pray for Plagues", "More Than Meets the Eye",
    "Sulfur", "Dance of Death", "Forevermore", "Repentless", "Into the Grave", "God of Emptiness",
    "Seasons in the Abyss", "Blood Brothers", "In Your Face", "Burnt Offerings", "Pure Evil",
    "Trivium", "Black Label", "Cowboys from Hell", "All Nightmare Long", "Suicide Messiah",
    "The Great Southern Trendkill", "My Own Summer", "A Dying God Coming into Human Flesh",
    "Life Burns", "Dystopia", "Oblivion", "Only for the Weak", "Push It", "Rain",
    "Sleeping My Day Away", "Still Remains", "Tread the Floods", "Into the Fire",
    "Beneath, Between & Behind", "Back to the Primitive", "I Stand Alone", "Death Magnetic",
    "Devil in I", "Strength Beyond Strength", "Spirits of the Dead", "Hallowed Point",
    "Psychosocial"
]

# Song to find
song_name = "Before I Forget"

# Find the index of the song
try:
    index = metal_songs.index(song_name)
    print(f"The song '{song_name}' is at index {index}.")
except ValueError:
    print(f"The song '{song_name}' was not found in the list.")


# Process each song ensuring 15 requests per minute
def process_songs(song_list):
    try:
        all_songs = []
        for i, song in enumerate(song_list):
            print(f"Fetching data for: {song}")
            result = fetch_song_data(song)
            if result:
                all_songs.append(result)
            
            # Save results to JSON file after every fetch
            with open("songs.json", "w", encoding="utf-8") as json_file:
                json.dump(all_songs, json_file, indent=4)

            # Wait for a while to maintain rate limits
            if (i + 1) % 15 == 0:
                print("Waiting for 60 seconds to comply with rate limits...")
                time.sleep(60)  # Wait 1 minute after every 10 requests
            else:
                time.sleep(6)  # Adjust delay between requests (6s to balance)

        print(f"Final list size: {len(all_songs)} songs with lyrics.")

    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    process_songs(metal_songs)
