import os
import requests
import json
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

class SpotifyAPIExplorer:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = None
        self.base_url = 'https://api.spotify.com/v1'
        
    def get_access_token(self):
        """Get access token for Spotify API"""
        print("🔑 Getting access token...")
        
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(auth_url, headers=auth_headers, data=auth_data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            print("✅ Access token obtained successfully!")
            return True
        else:
            print(f"❌ Failed to get access token: {response.status_code}")
            return False
    
    def make_request(self, endpoint):
        """Make a request to Spotify API with proper headers"""
        if not self.access_token:
            print("❌ No access token available")
            return None
            
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Request failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error making request: {str(e)}")
            return None
    
    def explore_search_endpoint(self):
        """Test the search endpoint - great for finding artists, tracks, playlists"""
        print("\n" + "="*60)
        print("🔍 EXPLORING SEARCH ENDPOINT")
        print("="*60)
        
        # Search for a popular artist
        print("\n1️⃣ Searching for 'Taylor Swift' (artist)...")
        artist_data = self.make_request("/search?q=Taylor%20Swift&type=artist&limit=1")
        
        if artist_data and 'artists' in artist_data:
            artist = artist_data['artists']['items'][0]
            print(f"   ✅ Found: {artist['name']}")
            print(f"   👥 Followers: {artist['followers']['total']:,}")
            print(f"   🎵 Genres: {', '.join(artist['genres'][:3])}")
            print(f"   🔗 Spotify ID: {artist['id']}")
            
            # Save the artist ID for later use
            self.taylor_swift_id = artist['id']
        
        # Search for playlists
        print("\n2️⃣ Searching for 'Top Hits' playlists...")
        playlist_data = self.make_request("/search?q=top%20hits&type=playlist&limit=3")
        
        if playlist_data and 'playlists' in playlist_data:
            print(f"   ✅ Found {len(playlist_data['playlists']['items'])} playlists:")
            for i, playlist in enumerate(playlist_data['playlists']['items'], 1):
                if playlist:  # Check if playlist data exists
                    name = playlist.get('name', 'Unknown')
                    followers = playlist.get('followers', {}).get('total', 0)
                    tracks = playlist.get('tracks', {}).get('total', 0)
                    description = playlist.get('description', 'No description')
                    
                    print(f"   {i}. {name}")
                    print(f"      👥 Followers: {followers:,}")
                    print(f"      🎵 Tracks: {tracks}")
                    print(f"      📝 Description: {description[:50]}...")
    
    def explore_artist_endpoint(self):
        """Test getting detailed artist information"""
        print("\n" + "="*60)
        print("🎤 EXPLORING ARTIST ENDPOINT")
        print("="*60)
        
        if not hasattr(self, 'taylor_swift_id'):
            print("❌ Need to run search endpoint first to get artist ID")
            return
        
        # Get artist details
        print("\n1️⃣ Getting detailed artist information...")
        artist_data = self.make_request(f"/artists/{self.taylor_swift_id}")
        
        if artist_data:
            print(f"   ✅ Artist: {artist_data['name']}")
            print(f"   👥 Followers: {artist_data['followers']['total']:,}")
            print(f"   ⭐ Popularity Score: {artist_data['popularity']}/100")
            print(f"   🎵 Genres: {', '.join(artist_data['genres'])}")
        
        # Get artist's top tracks
        print("\n2️⃣ Getting artist's top tracks...")
        top_tracks_data = self.make_request(f"/artists/{self.taylor_swift_id}/top-tracks?market=US")
        
        if top_tracks_data and 'tracks' in top_tracks_data:
            print(f"   ✅ Found {len(top_tracks_data['tracks'])} top tracks:")
            for i, track in enumerate(top_tracks_data['tracks'][:5], 1):
                print(f"   {i}. {track['name']}")
                print(f"      💿 Album: {track['album']['name']}")
                print(f"      ⭐ Popularity: {track['popularity']}/100")
    
    def explore_playlist_endpoint(self):
        """Test getting playlist information"""
        print("\n" + "="*60)
        print("📋 EXPLORING PLAYLIST ENDPOINT")
        print("="*60)
        
        # Use a well-known Spotify playlist ID (Today's Top Hits)
        playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Today's Top Hits
        
        print("\n1️⃣ Getting playlist details...")
        playlist_data = self.make_request(f"/playlists/{playlist_id}")
        
        if playlist_data:
            print(f"   ✅ Playlist: {playlist_data['name']}")
            print(f"   👥 Followers: {playlist_data['followers']['total']:,}")
            print(f"   🎵 Total Tracks: {playlist_data['tracks']['total']}")
            print(f"   📝 Description: {playlist_data['description'][:100]}...")
            print(f"   👤 Owner: {playlist_data['owner']['display_name']}")
        
        # Get playlist tracks (first few)
        print("\n2️⃣ Getting playlist tracks (first 5)...")
        tracks_data = self.make_request(f"/playlists/{playlist_id}/tracks?limit=5")
        
        if tracks_data and 'items' in tracks_data:
            print(f"   ✅ Found tracks:")
            for i, item in enumerate(tracks_data['items'], 1):
                if item and item.get('track'):  # Check if track data exists
                    track = item['track']
                    if track:  # Additional check for track data
                        artists = ', '.join([artist['name'] for artist in track.get('artists', [])])
                        track_name = track.get('name', 'Unknown Track')
                        popularity = track.get('popularity', 0)
                        album_name = track.get('album', {}).get('name', 'Unknown Album')
                        
                        print(f"   {i}. {track_name} by {artists}")
                        print(f"      ⭐ Popularity: {popularity}/100")
                        print(f"      💿 Album: {album_name}")
    
    def explore_audio_features_endpoint(self):
        """Test getting audio features for tracks - this is GOLD for your analysis!"""
        print("\n" + "="*60)
        print("🎵 EXPLORING AUDIO FEATURES ENDPOINT")
        print("="*60)
        
        # Get a specific track ID first
        print("\n1️⃣ Getting a track to analyze...")
        search_data = self.make_request("/search?q=Anti-Hero%20Taylor%20Swift&type=track&limit=1")
        
        if search_data and 'tracks' in search_data and search_data['tracks']['items']:
            track = search_data['tracks']['items'][0]
            track_id = track['id']
            
            print(f"   ✅ Found track: {track['name']} by {track['artists'][0]['name']}")
            
            # Get audio features
            print("\n2️⃣ Getting audio features...")
            features_data = self.make_request(f"/audio-features/{track_id}")
            
            if features_data:
                print("   ✅ Audio Features Analysis:")
                print(f"      🕺 Danceability: {features_data['danceability']:.3f} (0-1 scale)")
                print(f"      ⚡ Energy: {features_data['energy']:.3f} (0-1 scale)")
                print(f"      🔊 Loudness: {features_data['loudness']:.1f} dB")
                print(f"      🎤 Speechiness: {features_data['speechiness']:.3f} (0-1 scale)")
                print(f"      🎼 Acousticness: {features_data['acousticness']:.3f} (0-1 scale)")
                print(f"      🎪 Valence (mood): {features_data['valence']:.3f} (0-1 scale)")
                print(f"      ⏱️ Tempo: {features_data['tempo']:.1f} BPM")
                print(f"      ⏰ Duration: {features_data['duration_ms']/1000:.1f} seconds")
                
                print("\n   📊 What this means for your analysis:")
                if features_data['danceability'] > 0.7:
                    print("      - High danceability - good for party playlists")
                if features_data['energy'] > 0.7:
                    print("      - High energy - good for workout playlists")
                if features_data['valence'] > 0.6:
                    print("      - Positive mood - good for happy/upbeat playlists")
                else:
                    print("      - Lower valence - might be more emotional/sad")
    
    def explore_categories_endpoint(self):
        """Test getting available playlist categories"""
        print("\n" + "="*60)
        print("📂 EXPLORING CATEGORIES ENDPOINT")
        print("="*60)
        
        print("\n1️⃣ Getting available playlist categories...")
        categories_data = self.make_request("/browse/categories?limit=20")
        
        if categories_data and 'categories' in categories_data:
            print(f"   ✅ Found {len(categories_data['categories']['items'])} categories:")
            for i, category in enumerate(categories_data['categories']['items'], 1):
                print(f"   {i:2d}. {category['name']} (ID: {category['id']})")
            
            # Get playlists from a specific category (e.g., 'pop')
            print(f"\n2️⃣ Getting playlists from 'Pop' category...")
            pop_playlists = self.make_request("/browse/categories/pop/playlists?limit=5")
            
            if pop_playlists and 'playlists' in pop_playlists:
                print("   ✅ Pop playlists:")
                for i, playlist in enumerate(pop_playlists['playlists']['items'], 1):
                    print(f"   {i}. {playlist['name']}")
                    print(f"      👥 {playlist['followers']['total']:,} followers")
    
    def save_sample_data(self, data, filename):
        """Save sample data to JSON file for inspection"""
        try:
            with open(f"sample_data_{filename}.json", 'w') as f:
                json.dump(data, f, indent=2)
            print(f"   💾 Sample data saved to 'sample_data_{filename}.json'")
        except Exception as e:
            print(f"   ❌ Failed to save data: {str(e)}")
    
    def run_full_exploration(self):
        """Run all endpoint explorations"""
        print("🎵 SPOTIFY API ENDPOINT EXPLORATION")
        print("="*60)
        print("This script will test different Spotify API endpoints")
        print("to understand what data is available for your project.")
        print("="*60)
        
        # Get access token first
        if not self.get_access_token():
            print("❌ Cannot proceed without access token")
            return
        
        # Run all explorations
        self.explore_search_endpoint()
        time.sleep(1)  # Be nice to the API
        
        self.explore_artist_endpoint()
        time.sleep(1)
        
        self.explore_playlist_endpoint()
        time.sleep(1)
        
        self.explore_audio_features_endpoint()
        time.sleep(1)
        
        self.explore_categories_endpoint()
        
        print("\n" + "="*60)
        print("🎉 EXPLORATION COMPLETE!")
        print("="*60)
        print("Now you know:")
        print("✅ How to search for artists, tracks, and playlists")
        print("✅ How to get detailed artist information and top tracks")
        print("✅ How to access playlist data and track listings")
        print("✅ How to get audio features (the secret sauce for your analysis!)")
        print("✅ How to browse different playlist categories")
        print("\nNext step: Understanding rate limits and data structure!")

if __name__ == "__main__":
    explorer = SpotifyAPIExplorer()
    explorer.run_full_exploration()