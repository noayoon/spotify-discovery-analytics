# Spotify Discovery Engine Analytics

*A data-driven analysis of music discovery patterns to inform product strategy recommendations for music streaming platforms.*

## 📖 Project Overview

This project analyzes music discovery patterns using Spotify's Web API to identify opportunities for improving recommendation algorithms and discovery features. Built as a technical demonstration for product management applications, specifically targeting Spotify's 2026 Summer Product Management Internship.

## 🎯 Objectives

- **Data Collection**: Gather comprehensive playlist and track data across multiple genres and categories
- **Pattern Analysis**: Identify what makes playlists successful and tracks discoverable  
- **Product Insights**: Generate data-backed recommendations for discovery feature improvements
- **Technical Demonstration**: Showcase ability to work with APIs, analyze data, and translate insights into product strategy

## 🛠️ Technical Stack

- **Python 3.11** - Primary programming language
- **Spotify Web API** - Data source for playlists, tracks, and audio features
- **Pandas** - Data manipulation and analysis
- **Matplotlib/Seaborn** - Data visualization
- **Flask** - Web dashboard development
- **Jupyter Notebooks** - Interactive analysis and documentation

## 📊 Data Collection Strategy

The project collects three types of data to understand music discovery patterns:

1. **Playlist Metadata**: Names, descriptions, follower counts, categories
2. **Track Information**: Song details, artist info, popularity scores, release dates
3. **Audio Features**: Danceability, energy, valence, tempo, acousticness, and other musical characteristics

## 🔍 Key Research Questions

- What audio features correlate with track popularity and discoverability?
- How does playlist structure (size, diversity, curation style) impact user engagement?
- Which categories and genres show the strongest discovery patterns?
- What gaps exist in current recommendation systems that could be addressed?
- How do emerging artists gain traction in the current discovery ecosystem?

## 📈 Expected Deliverables

- **Interactive Dashboard**: Web-based visualization of discovery patterns and insights
- **Data Analysis Report**: Comprehensive findings with statistical analysis
- **Product Recommendations**: Feature concepts with supporting data and mockups
- **Technical Documentation**: API usage, data processing methodology, and architecture

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Spotify Developer Account
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/noayoon/spotify-discovery-analytics.git
cd spotify-discovery-analytics
```

2. Create virtual environment:
```bash
python3 -m venv spotify_env
source spotify_env/bin/activate  # On Windows: spotify_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install requests pandas matplotlib seaborn jupyter flask python-dotenv
```

4. Set up Spotify API credentials:
   - Create a `.env` file in the project root
   - Add your Spotify API credentials:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

5. Test the setup:
```bash
python test_setup.py
```

## 📁 Project Structure

```
spotify-discovery-analytics/
├── data/                   # Collected data files (CSV)
├── notebooks/              # Jupyter analysis notebooks  
├── src/                    # Source code modules
├── dashboard/              # Web dashboard files
├── docs/                   # Documentation and reports
├── test_setup.py          # API connection test
├── data_collector.py      # Main data collection script
├── .env                   # Environment variables (not tracked)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🎵 Why Music Discovery Matters

Music discovery is central to streaming platform success:
- **User Retention**: Better discovery keeps users engaged longer
- **Artist Success**: Effective discovery helps artists build audiences
- **Platform Differentiation**: Superior recommendations create competitive advantage
- **Revenue Growth**: Engaged users are more likely to convert to premium subscriptions

## 🔒 Data Privacy & Ethics

- Uses only publicly available playlist and track data
- No personal user data is collected or stored
- Complies with Spotify's API Terms of Service and rate limits
- Rate limiting implemented to respect API guidelines and server resources

## 📝 Development Status

- [x] Project setup and API connection
- [x] Initial data collection framework
- [ ] Large-scale data collection across categories
- [ ] Exploratory data analysis and pattern identification
- [ ] Statistical analysis and correlation studies
- [ ] Interactive dashboard development
- [ ] Product strategy documentation and feature mockups
- [ ] Final presentation materials and case study

## 🎓 Academic Context

**Noah Yoon**  
B.S. Computer Science & Human and Organizational Development  
Vanderbilt University, Class of 2027  
GPA: 3.86/4.00 | Dean's List (All Semesters)

This project combines technical skills from computer science coursework with product thinking from HOD studies and real-world experience from product marketing and campus leadership roles.

## 🤝 Contributing

This is a personal project for academic and career demonstration purposes. However, feedback and suggestions are welcome through issues or discussions.

## 📫 Contact

**Noah Yoon**  
📧 noah.s.yoon@vanderbilt.edu  
🎓 Vanderbilt University  
🎯 Aspiring Product Manager specializing in music technology

---

*Built with ❤️ for music discovery and data-driven product strategy*