import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SpotifyRateLimitAnalyzer:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = None
        self.base_url = 'https://api.spotify.com/v1'
        self.request_log = []  # Track all requests for analysis
        
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
            print("✅ Access token obtained!")
            return True
        else:
            print(f"❌ Failed to get access token: {response.status_code}")
            return False
    
    def make_tracked_request(self, endpoint, description=""):
        """Make a request while tracking rate limit info"""
        if not self.access_token:
            return None
            
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f"{self.base_url}{endpoint}"
        
        # Record request start time
        start_time = datetime.now()
        
        try:
            response = requests.get(url, headers=headers)
            end_time = datetime.now()
            
            # Log the request details
            request_info = {
                'endpoint': endpoint,
                'description': description,
                'status_code': response.status_code,
                'response_time_ms': (end_time - start_time).total_seconds() * 1000,
                'timestamp': start_time.isoformat(),
                'rate_limit_headers': {}
            }
            
            # Capture rate limit headers if they exist
            rate_limit_headers = [
                'X-RateLimit-Limit',
                'X-RateLimit-Remaining', 
                'X-RateLimit-Reset',
                'Retry-After'
            ]
            
            for header in rate_limit_headers:
                if header in response.headers:
                    request_info['rate_limit_headers'][header] = response.headers[header]
            
            self.request_log.append(request_info)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                print(f"⚠️  Rate limited! Endpoint: {endpoint}")
                if 'Retry-After' in response.headers:
                    retry_after = int(response.headers['Retry-After'])
                    print(f"   Retry after: {retry_after} seconds")
                return None
            else:
                print(f"❌ Request failed: {response.status_code} - {response.text[:100]}")
                return None
                
        except Exception as e:
            print(f"❌ Error making request: {str(e)}")
            return None
    
    def understand_spotify_rate_limits(self):
        """Learn about Spotify's rate limiting through documentation and testing"""
        print("\n" + "="*70)
        print("⏱️  UNDERSTANDING SPOTIFY RATE LIMITS")
        print("="*70)
        
        print("\n📚 What Spotify's Documentation Says:")
        print("   • Rate limits are applied per application (your Client ID)")
        print("   • Different endpoints may have different limits")
        print("   • Limits are typically measured in requests per second/minute")
        print("   • When you hit a limit, you get a 429 status code")
        print("   • The 'Retry-After' header tells you how long to wait")
        
        print("\n🧪 Let's test this with real requests...")
        print("   (Don't worry - we'll be respectful and not spam the API)")
        
        # Test with multiple quick requests to see rate limiting behavior
        print("\n1️⃣ Making several search requests to observe patterns...")
        
        test_queries = [
            ("Taylor Swift", "Popular artist search"),
            ("The Beatles", "Classic artist search"), 
            ("Billie Eilish", "Modern artist search"),
            ("Drake", "Hip-hop artist search"),
            ("Adele", "Another popular artist")
        ]
        
        for query, description in test_queries:
            endpoint = f"/search?q={query.replace(' ', '%20')}&type=artist&limit=1"
            data = self.make_tracked_request(endpoint, description)
            
            if data:
                artist = data['artists']['items'][0] if data['artists']['items'] else None
                if artist:
                    print(f"   ✅ Found: {artist['name']} ({artist['followers']['total']:,} followers)")
            
            # Small delay to be respectful
            time.sleep(0.5)
        
        print(f"\n📊 Request Analysis:")
        if self.request_log:
            total_requests = len(self.request_log)
            successful_requests = len([r for r in self.request_log if r['status_code'] == 200])
            avg_response_time = sum([r['response_time_ms'] for r in self.request_log]) / total_requests
            
            print(f"   • Total requests made: {total_requests}")
            print(f"   • Successful requests: {successful_requests}")
            print(f"   • Success rate: {(successful_requests/total_requests)*100:.1f}%")
            print(f"   • Average response time: {avg_response_time:.1f}ms")
            
            # Check if we got any rate limit info
            rate_limited = [r for r in self.request_log if r['status_code'] == 429]
            if rate_limited:
                print(f"   ⚠️  Rate limited {len(rate_limited)} times")
            else:
                print("   ✅ No rate limiting encountered (good!)")
    
    def analyze_data_structure(self):
        """Understand the structure of data returned by different endpoints"""
        print("\n" + "="*70)
        print("📋 ANALYZING DATA STRUCTURE")
        print("="*70)
        
        print("\n🔍 Let's examine the structure of different data types...")
        
        # Get artist data
        print("\n1️⃣ ARTIST DATA STRUCTURE:")
        artist_data = self.make_tracked_request("/search?q=Taylor%20Swift&type=artist&limit=1", "Artist structure analysis")
        
        if artist_data and 'artists' in artist_data:
            artist = artist_data['artists']['items'][0]
            print("   📊 Key fields available in artist data:")
            
            important_fields = {
                'id': 'Unique Spotify identifier',
                'name': 'Artist name',
                'popularity': 'Score 0-100 of current popularity',
                'followers': 'Number of followers (nested object)',
                'genres': 'List of associated genres',
                'images': 'Artist photos/artwork'
            }
            
            for field, description in important_fields.items():
                if field in artist:
                    value = artist[field]
                    if field == 'followers':
                        print(f"   • {field}: {value['total']:,} followers - {description}")
                    elif field == 'genres':
                        print(f"   • {field}: {value} - {description}")
                    elif field == 'images':
                        print(f"   • {field}: {len(value)} images available - {description}")
                    else:
                        print(f"   • {field}: {value} - {description}")
        
        # Get playlist data using search
        print("\n2️⃣ PLAYLIST DATA STRUCTURE:")
        playlist_data = self.make_tracked_request("/search?q=Today's%20Top%20Hits&type=playlist&limit=1", "Playlist structure analysis")
        
        if playlist_data and 'playlists' in playlist_data:
            playlists = playlist_data['playlists']['items']
            if playlists:
                playlist = playlists[0]
                print("   📊 Key fields available in playlist data:")
                
                playlist_fields = {
                    'id': 'Unique playlist identifier',
                    'name': 'Playlist name',
                    'description': 'Playlist description',
                    'followers': 'Number of followers',
                    'tracks': 'Track count and link to tracks',
                    'owner': 'Playlist creator info',
                    'public': 'Whether playlist is public'
                }
                
                for field, description in playlist_fields.items():
                    if field in playlist and playlist[field] is not None:
                        value = playlist[field]
                        if field == 'followers':
                            print(f"   • {field}: {value['total']:,} followers - {description}")
                        elif field == 'tracks':
                            print(f"   • {field}: {value['total']} tracks - {description}")
                        elif field == 'owner':
                            print(f"   • {field}: {value['display_name']} - {description}")
                        elif field == 'description':
                            desc_preview = value[:50] + "..." if len(value) > 50 else value
                            print(f"   • {field}: '{desc_preview}' - {description}")
                        else:
                            print(f"   • {field}: {value} - {description}")
        
        # Get track data structure
        print("\n3️⃣ TRACK DATA STRUCTURE:")
        track_data = self.make_tracked_request("/search?q=Anti-Hero%20Taylor%20Swift&type=track&limit=1", "Track structure analysis")
        
        if track_data and 'tracks' in track_data:
            tracks = track_data['tracks']['items']
            if tracks:
                track = tracks[0]
                print("   📊 Key fields available in track data:")
                
                track_fields = {
                    'id': 'Unique track identifier',
                    'name': 'Song title',
                    'popularity': 'Score 0-100 of current popularity',
                    'artists': 'List of artists (with their own data)',
                    'album': 'Album information (nested object)',
                    'duration_ms': 'Song length in milliseconds',
                    'explicit': 'Whether song has explicit content',
                    'preview_url': 'Link to 30-second preview'
                }
                
                for field, description in track_fields.items():
                    if field in track and track[field] is not None:
                        value = track[field]
                        if field == 'artists':
                            artists_names = [artist['name'] for artist in value]
                            print(f"   • {field}: {artists_names} - {description}")
                        elif field == 'album':
                            print(f"   • {field}: '{value['name']}' ({value['release_date']}) - {description}")
                        elif field == 'duration_ms':
                            duration_sec = value / 1000
                            print(f"   • {field}: {duration_sec:.1f} seconds - {description}")
                        else:
                            print(f"   • {field}: {value} - {description}")
    
    def create_data_collection_strategy(self):
        """Based on our learning, create a strategy for systematic data collection"""
        print("\n" + "="*70)
        print("🎯 DATA COLLECTION STRATEGY")
        print("="*70)
        
        print("\n📋 Based on our analysis, here's your optimal data collection approach:")
        
        print("\n1️⃣ RATE LIMIT STRATEGY:")
        print("   • Make requests every 0.5-1 seconds to be respectful")
        print("   • Batch requests in groups (e.g., 50 requests, then pause)")
        print("   • Always check for 429 status codes and respect Retry-After headers")
        print("   • Log all requests to monitor your usage patterns")
        
        print("\n2️⃣ DATA COLLECTION PRIORITY ORDER:")
        collection_steps = [
            ("Categories", "Get all available playlist categories", "Low effort, high value"),
            ("Playlists by Category", "Find popular playlists in each category", "Core data source"),
            ("Playlist Details", "Get full details for each playlist", "Essential metadata"), 
            ("Track Lists", "Get all tracks from selected playlists", "Primary analysis data"),
            ("Artist Info", "Get details for artists in your dataset", "Enrichment data"),
            ("Audio Features", "Get musical characteristics", "Analysis gold mine")
        ]
        
        for i, (name, description, value) in enumerate(collection_steps, 1):
            print(f"   {i}. {name}: {description} ({value})")
        
        print("\n3️⃣ DATA STRUCTURE INSIGHTS:")
        insights = [
            "Artists have popularity scores and follower counts - great for trend analysis",
            "Playlists have follower counts and track counts - perfect for engagement metrics", 
            "Tracks have popularity scores and detailed album info - ideal for discovery analysis",
            "All objects have unique IDs - use these to avoid duplicates and link data",
            "Nested objects (like artist info in tracks) provide rich relationship data"
        ]
        
        for insight in insights:
            print(f"   • {insight}")
        
        print("\n4️⃣ RECOMMENDED SAMPLE SIZES:")
        sample_sizes = [
            ("Categories", "All available (~20)", "Complete coverage"),
            ("Playlists per category", "10-20 popular ones", "Good representation"),
            ("Tracks per playlist", "All tracks", "Complete playlist picture"),
            ("Total playlists", "200-400", "Manageable but comprehensive"),
            ("Total tracks", "5,000-10,000", "Statistically significant")
        ]
        
        for data_type, size, rationale in sample_sizes:
            print(f"   • {data_type}: {size} ({rationale})")
    
    def save_request_log(self):
        """Save the request log for analysis"""
        if self.request_log:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"request_log_{timestamp}.json"
            
            try:
                with open(filename, 'w') as f:
                    json.dump(self.request_log, f, indent=2)
                print(f"\n💾 Request log saved to '{filename}'")
                print("   You can analyze this to understand your API usage patterns!")
            except Exception as e:
                print(f"❌ Failed to save request log: {str(e)}")
    
    def run_complete_analysis(self):
        """Run the complete rate limit and data structure analysis"""
        print("⏱️  SPOTIFY API RATE LIMITS & DATA STRUCTURE ANALYSIS")
        print("="*70)
        print("This script will help you understand:")
        print("• How fast you can make requests without getting rate limited")
        print("• What data structure each endpoint returns")  
        print("• How to build an efficient data collection strategy")
        print("="*70)
        
        # Get access token
        if not self.get_access_token():
            print("❌ Cannot proceed without access token")
            return
        
        # Run all analyses
        self.understand_spotify_rate_limits()
        time.sleep(1)
        
        self.analyze_data_structure()
        time.sleep(1)
        
        self.create_data_collection_strategy()
        
        # Save our learning for future reference
        self.save_request_log()
        
        print("\n" + "="*70)
        print("🎉 ANALYSIS COMPLETE!")
        print("="*70)
        print("You now understand:")
        print("✅ How to respect API rate limits")
        print("✅ The structure of artist, playlist, and track data")
        print("✅ How to plan systematic data collection")
        print("✅ What sample sizes make sense for your project")
        print("\nNext: Document what data you can access!")

if __name__ == "__main__":
    analyzer = SpotifyRateLimitAnalyzer()
    analyzer.run_complete_analysis()