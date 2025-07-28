import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get your Spotify credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

print("🎵 Testing Spotify API setup...")
print("=" * 50)

# Check if credentials are loaded
if client_id:
    print(f"✅ Client ID found: {client_id[:10]}...")
else:
    print("❌ Client ID not found! Check your .env file")

if client_secret:
    print(f"✅ Client Secret found: {client_secret[:10]}...")
else:
    print("❌ Client Secret not found! Check your .env file")

print("=" * 50)

# Test API connection
def test_spotify_connection():
    if not client_id or not client_secret:
        print("❌ Cannot test connection - missing credentials")
        return
    
    print("🔄 Attempting to connect to Spotify API...")
    
    # Get access token from Spotify
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    try:
        # Request access token
        response = requests.post(auth_url, headers=auth_headers, data=auth_data)
        
        if response.status_code == 200:
            print("✅ SUCCESS: Connected to Spotify API!")
            
            # Get the access token
            token_data = response.json()
            access_token = token_data['access_token']
            print(f"🔑 Access token received: {access_token[:20]}...")
            
            # Test getting a popular playlist
            print("🔄 Testing playlist data retrieval...")
            headers = {'Authorization': f'Bearer {access_token}'}
            
            # Let's try a different approach - search for a popular artist instead
            test_url = 'https://api.spotify.com/v1/search?q=Taylor%20Swift&type=artist&limit=1'
            
            playlist_response = requests.get(test_url, headers=headers)
            
            if playlist_response.status_code == 200:
                playlist_data = playlist_response.json()
                print("✅ Successfully retrieved playlist data!")
                print(f"📋 Playlist Name: {playlist_data['name']}")
                print(f"🎵 Number of tracks: {playlist_data['tracks']['total']}")
                print(f"👥 Followers: {playlist_data['followers']['total']:,}")
                print("🎉 Everything is working perfectly!")
            else:
                print(f"❌ Failed to get playlist data. Status code: {playlist_response.status_code}")
                print(f"Error: {playlist_response.text}")
                
        else:
            print(f"❌ Failed to connect to Spotify API")
            print(f"Status code: {response.status_code}")
            print(f"Error: {response.text}")
            print("\n🔧 Troubleshooting tips:")
            print("- Double-check your Client ID and Client Secret in the .env file")
            print("- Make sure there are no extra spaces in your .env file")
            print("- Verify your Spotify app is created properly")
            
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        print("\n🔧 This might be a network issue or package installation problem")

if __name__ == "__main__":
    test_spotify_connection()
    print("=" * 50)
    print("Test complete! If you see ✅ messages above, you're ready to proceed!")