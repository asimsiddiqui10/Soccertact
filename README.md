# SoccerTact MLS Analysis Dashboard

A comprehensive data analysis dashboard for Major League Soccer (MLS) built with Streamlit. This application provides detailed insights into team performance, player statistics, and match analysis using advanced soccer analytics metrics.

## 🚀 Features

### Team Analysis
- **Team Performance Metrics**: Goals Added, Expected Goals (xG), Expected Pass (xPass)
- **Seasonal Comparisons**: Analyze team performance across multiple seasons (2013-2024)
- **Interactive Visualizations**: Dynamic charts and graphs for better data interpretation
- **Team Rankings**: Compare teams based on various performance indicators

### Player Analysis
- **Individual Player Stats**: Detailed performance metrics for each player
- **Position-Specific Analysis**: Separate analysis for field players and goalkeepers
- **Salary vs Performance**: Compare player salaries with their on-field contributions
- **Player Comparisons**: Side-by-side analysis of multiple players

### Match Analysis
- **Game-by-Game Breakdown**: Detailed analysis of individual matches
- **Team vs Team Comparisons**: Head-to-head performance analysis
- **Tactical Insights**: Advanced metrics to understand team strategies

### Advanced Analytics
- **Goals Added (g+)**: Comprehensive metric measuring player contributions
- **Expected Goals (xG)**: Probability-based goal scoring analysis
- **Expected Pass (xPass)**: Pass completion probability analysis
- **Auto Insights**: AI-powered analysis and recommendations

## 📊 Data Sources

The application uses data from:
- **American Soccer Analysis API**: Real-time MLS data
- **Historical Data**: Comprehensive dataset from 2013-2024
- **Player Mapping**: Cross-referenced player information
- **Team Statistics**: Detailed team performance metrics

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/asimsiddiqui10/Soccertact.git
   cd Soccertact
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas plotly requests
   ```

3. **Run the application**
   ```bash
   streamlit run App/app.py
   ```

4. **Access the dashboard**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will load with the latest MLS data

## 📁 Project Structure

```
MLSAnalysis/
├── App/
│   ├── app.py                 # Main Streamlit application
│   ├── data/                  # JSON data files
│   │   ├── teams.json         # Team information
│   │   ├── players.json       # Player data
│   │   ├── player_mapping.json # Player-team mappings
│   │   └── [season_data]/     # Yearly performance data
│   ├── modules/               # Core analysis modules
│   │   ├── methods.py         # API and data fetching methods
│   │   ├── teamAnalysis.py    # Team analysis algorithms
│   │   ├── promptGenerator.py # AI prompt generation
│   │   └── autoInsights.py    # Automated insights
│   └── pages/                 # Streamlit page modules
│       ├── 1Team Analysis.py
│       ├── 2Player Analysis.py
│       ├── 3Match Analysis.py
│       ├── 4Compare Teams.py
│       └── 5Compare Players.py
└── README.md
```

## 🎯 Usage

### Getting Started
1. **Select Season**: Choose from available seasons (2013-2024)
2. **Choose Analysis Type**: Navigate between different analysis modules
3. **Select Teams/Players**: Use the sidebar to select specific teams or players
4. **Explore Data**: Interact with visualizations and metrics

### Key Metrics Explained

- **Goals Added (g+)**: Measures a player's total contribution to their team's goal difference
- **Expected Goals (xG)**: Probability that a shot will result in a goal
- **Expected Pass (xPass)**: Probability that a pass will be completed successfully
- **Team Performance**: Aggregated metrics showing overall team effectiveness

## 🔧 Configuration

### API Configuration
The application uses the American Soccer Analysis API. No API key is required for basic functionality.

### Data Updates
- Data is automatically fetched from the API
- Historical data is stored locally for faster access
- New seasons are added as they become available

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📈 Future Enhancements

- [ ] Real-time match tracking
- [ ] Advanced machine learning predictions
- [ ] Mobile-responsive design improvements
- [ ] Additional league support
- [ ] Export functionality for reports
- [ ] Custom dashboard creation

## 🐛 Troubleshooting

### Common Issues

1. **Data Loading Errors**
   - Ensure all JSON files are present in the `data/` directory
   - Check internet connection for API calls

2. **Visualization Issues**
   - Update plotly: `pip install --upgrade plotly`
   - Clear browser cache and refresh

3. **Performance Issues**
   - Close other applications to free up memory
   - Consider using a more powerful machine for large datasets

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **American Soccer Analysis** for providing comprehensive MLS data
- **Streamlit** for the excellent web application framework
- **Plotly** for interactive visualizations
- **MLS** for the exciting soccer data to analyze

## 📞 Support

For support, email asimsiddiqui10@gmail.com or create an issue in the repository.

---

**Made with ⚽ for soccer analytics enthusiasts**
