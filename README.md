
# Alcohol Consumption Dashboard

This project is a web-based dashboard that provides insights into alcohol consumption trends, demographics, quarterly insights, and global comparisons. Built with Dash and Plotly, the dashboard offers interactive visualizations and a user-friendly interface.

## Features
1. **Global Comparison**: Compare alcohol consumption in Ireland with other countries using an interactive globe.
2. **Trends in Ireland**: Visualize alcohol consumption trends across different age groups in Ireland.
3. **Demographics**: Explore alcohol consumption by gender and age group.
4. **Quarterly Insights**: Analyze alcohol consumption trends by quarter and alcohol type in Ireland.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/alcohol-consumption-dashboard.git
   cd alcohol-consumption-dashboard
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure the `Cleaned_datasets` directory contains the following CSV files:
   - `cleaned_alcohol_consumption_data.csv`
   - `cleaned_quarterly_alcohol.csv`
   - `cleaned_alcohol_world.csv`
   - `world_country_and_usa_states_latitude_and_longitude_values.csv`

4. Run the application:
   ```bash
   python app.py
   ```

5. Open the app in your browser:
   - The app will run at `http://127.0.0.1:8050/`.

## Project Structure
```
alcohol-consumption-dashboard/
│
├── app.py                 # Main application file
├── requirements.txt       # List of dependencies
├── README.md              # Project documentation
├── Cleaned_datasets/      # Folder containing required CSV files
│   ├── cleaned_alcohol_consumption_data.csv
│   ├── cleaned_quarterly_alcohol.csv
│   ├── cleaned_alcohol_world.csv
│   ├── world_country_and_usa_states_latitude_and_longitude_values.csv
```

## Usage
- Navigate through the sections:
  - **Global Comparison**: Select a year and click on a country for comparisons.
  - **Trends**: Choose an age group to view alcohol consumption trends in Ireland.
  - **Demographics**: Select a year to see consumption by gender and age.
  - **Quarterly Insights**: Choose alcohol type and year to explore quarterly trends.
    

## Author
- Nishanth Gopinath
