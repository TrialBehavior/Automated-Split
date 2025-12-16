# Jury Optimization Tool

A Flask-based web application for optimizing jury selection and assignment using Mixed Integer Programming (MIP). The tool creates balanced juries across multiple demographic dimensions with two different optimization strategies.

## Overview

This application helps jury consultants split a pool of potential jurors into multiple balanced juries. It uses advanced optimization algorithms to ensure fair demographic representation across all juries while prioritizing the most critical factors.

## Features

### Core Functionality
- **Upload Juror Data**: Excel file input with demographic information
- **Dual Optimization Methods**:
  - **Sequential Optimization**: Fills juries one at a time, guaranteeing complete juries
  - **Simultaneous Optimization**: Optimizes all juries together for maximum similarity
- **Interactive Editing Interface**: Manually adjust jury assignments after optimization
- **Comprehensive Reporting**: HTML and Excel reports with demographic breakdowns
- **Real-time Scoreboard**: Live balance tracking during manual editing

### Optimization Hierarchy

The optimization uses a three-tier constraint system:

**Tier 1 - Inviolable Hard Constraints:**
- Exact jury size (e.g., 12 jurors per jury)
- Overall P/D (Plaintiff/Defense) leaning balance

**Tier 2 - Secondary Soft Constraints (High Penalty):**
- Granular P+/P/D/D+ balance
- Gender balance (Male/Female)

**Tier 3 - Tertiary Weighted Optimization:**
- Race distribution
- Age group distribution
- Education level distribution
- Marital status distribution

Users can customize the ranking of Tier 3 demographics (Race, Age, Education, Marital Status) to match case-specific priorities.

## Technical Stack

### Backend
- **Flask 2.0.1**: Web framework
- **PuLP 2.8.0**: Linear programming solver for optimization
- **pandas 2.1.4**: Data manipulation
- **NumPy 1.26.4**: Numerical operations
- **openpyxl 3.1.2**: Excel file handling

### Frontend
- **Bootstrap 5.1.0**: UI framework
- **Vanilla JavaScript**: Interactive features and filtering
- **Custom CSS**: Styling and responsive design

### Visualization
- **Matplotlib 3.8.3**: Charts and graphs
- **Seaborn 0.13.2**: Statistical visualizations

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/TrialBehavior-Automated-Split.git
cd TrialBehavior-Automated-Split
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Create required directories:**
The application will automatically create `uploads/` and `results/` directories on first run.

4. **Run the application:**
```bash
python app.py
```

5. **Access the application:**
Open your browser and navigate to `http://localhost:10000`

## Usage

### 1. Upload Data

**Required Excel Columns:**
- `Name`: Juror name
- `Final_Leaning`: Must be one of: P+, P, D, D+
- `Gender`: Male/Female (or M/F)
- `Race`: Demographic race categories
- `Age`: Numeric age value
- `Education`: Education level
- `Marital`: Marital status

**Optional Columns:**
The system can handle additional columns, but optimization focuses on the above demographics.

### 2. Configure Optimization

**Basic Settings:**
- **Number of Juries**: How many juries to create (2-10)
- **Jury Size**: Number of jurors per jury (6-18, typically 12)

**Demographic Rankings:**
Rank the importance of demographic variables (1 = Highest, 4 = Lowest):
- Race
- Age
- Education
- Marital Status

*Note: Final Leaning and Gender are always top priority and don't need ranking.*

**Optimization Method:**
- **Simultaneous Optimization** (Recommended): Optimizes all juries together to maximize similarity between them
- **Sequential Optimization**: Fills juries one at a time, guaranteeing complete assignment

### 3. Review and Edit Assignments

After optimization, you'll see an interactive editing interface with:

**Scoreboard Features:**
- Real-time balance tracking for each jury
- Color-coded warnings (green = balanced, yellow = warning, red = imbalanced)
- Visual indicators for balance violations
- P/D leaning tracking
- Gender distribution
- Demographic category counts

**Editing Features:**
- Dropdown menus to reassign jurors between juries
- Filter by jury or leaning
- Live updates to balance calculations
- Warning modal before confirming imbalanced assignments

### 4. Generate Final Report

Click "Confirm Final Split" to generate:
- **HTML Report**: Comprehensive analysis with visualizations
- **Excel Spreadsheet**: Detailed assignments with all demographic data

## File Structure

```
TrialBehavior-Automated-Split/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── modules/
│   ├── data_processing.py      # Sequential data processing
│   ├── data_processing_sim.py  # Simultaneous data processing
│   ├── optimization.py         # Sequential optimization logic
│   ├── optimization_sim.py     # Simultaneous optimization logic
│   ├── utils.py                # Sequential utility functions
│   └── utils_sim.py            # Simultaneous utility functions
├── templates/
│   ├── index.html              # Upload and configuration page
│   ├── edit.html               # Interactive editing interface
│   └── success.html            # Download page
├── static/
│   ├── css/
│   │   └── style.css           # Custom styles
│   └── js/
│       └── main.js             # Client-side JavaScript
├── uploads/                    # Temporary file storage
└── results/                    # Session-based results storage
```

## Optimization Details

### Sequential Optimization
- Fills Jury A first with optimal balance
- Then fills Jury B with remaining jurors
- Continues until all juries are complete
- Guarantees fully staffed juries
- May result in unassigned jurors if total count doesn't divide evenly

### Simultaneous Optimization
- Considers all juries in a single optimization problem
- Minimizes differences between juries across all demographics
- Best for creating similar juries
- More computationally intensive but yields better overall balance

### Constraint Hierarchy

The solver minimizes the following weighted objective function:

```
Minimize: 
  1000.0 × (P/D imbalances)
  + 100.0 × (Granular leaning imbalances)
  + 90.0 × (Gender imbalances)
  + [User-weighted] × (Race, Age, Education, Marital imbalances)
```

## Memory Management

The application includes memory tracking to monitor resource usage:
- Logs memory at each stage of optimization
- Tracks peak memory usage
- Useful for handling large juror pools

## Session Management

- Each upload creates a unique session with UUID
- Results stored in session-specific folders
- Automatic cleanup of old sessions recommended for production

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main upload page |
| `/upload` | POST | Process uploaded Excel file |
| `/edit` | GET | Interactive editing interface |
| `/save_changes` | POST | Save manual jury assignment changes |
| `/generate_report` | POST | Generate final HTML and Excel reports |
| `/success` | GET | Download page for reports |
| `/download/<filetype>` | GET | Download HTML or Excel files |

## Customization

### Changing Default Settings

Edit `config.py`:
```python
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
RESULTS_FOLDER = os.path.join(BASE_DIR, 'results')
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB file size limit
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
```

### Adjusting Optimization Weights

In `app.py`, modify the weight dictionaries:
```python
# Sequential optimization weights
rankings = {
    'Final_Leaning': 5.0,
    'Gender': 5.0,
    'Race': float(5 - race_rank),
    # ... etc
}

# Simultaneous optimization weights
tier_weights = {
    'tier1_pd_balance': 1000.0,
    'tier2_granular_balance': 100.0,
    'tier2_gender_balance': 90.0,
    # ... etc
}
```

## Troubleshooting

### Common Issues

**"Insufficient jurors" Error:**
- Ensure you have enough jurors: `(Number of Juries) × (Jury Size)` ≤ Total Jurors
- Check for missing data in required columns

**Optimization Takes Too Long:**
- Reduce the number of juries
- Use Sequential optimization instead of Simultaneous
- Simplify demographic rankings

**Excel File Not Recognized:**
- Ensure file extension is .xlsx or .xls
- Check that column headers match expected names
- Remove any blank rows at the top of the spreadsheet

**Session Expired:**
- Sessions are stored server-side and may expire if inactive
- Simply start a new optimization

## Production Deployment

### Environment Variables
```bash
export PORT=10000
export SECRET_KEY='your-secret-key-here'
```

### Gunicorn Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:10000 app:app
```

### Security Considerations
1. Change the default `SECRET_KEY` in `app.py`
2. Set up proper file upload validation
3. Implement rate limiting for uploads
4. Configure HTTPS in production
5. Set up session cleanup for old results

## Performance Considerations

- **Small pools (< 50 jurors)**: Both methods work well
- **Medium pools (50-100 jurors)**: Sequential is faster, Simultaneous gives better balance
- **Large pools (> 100 jurors)**: Sequential recommended for speed

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Database integration for historical data
- [ ] Advanced demographic constraints (e.g., occupation, geographic location)
- [ ] Export to additional formats (PDF, CSV)
- [ ] Batch processing for multiple cases
- [ ] API endpoints for programmatic access
- [ ] Docker containerization
- [ ] Advanced analytics dashboard

## Contributing

This is a proprietary tool for Trial Behavior Consulting. For internal feature requests or bug reports, please contact the development team.

## License

Proprietary software. All rights reserved by Trial Behavior Consulting.

## Contact

For questions or support:
- **Developer**: Nick Wilson
- **Company**: Trial Behavior Consulting
- **Location**: Los Angeles, CA

## Acknowledgments

- Built with Flask and PuLP optimization libraries
- Uses Bootstrap for responsive design
- Implements Mixed Integer Programming for optimal jury selection

---

**Version**: 1.0  
**Last Updated**: December 2024