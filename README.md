# ⬡ Oil & Gas Market Intelligence Dashboard

A real-time market dashboard for the oil & gas sector built with Python and Dash. Tracks live prices, daily performance and historical trends for key energy assets.

## Features

- **Live price cards** — WTI Crude, Brent Crude, Natural Gas, SLB Corp and ExxonMobil with daily % change
- **7-day sparklines** per asset with green/red coloring based on performance
- **Historical price chart** with 20-day moving average and configurable time range
- **Auto-refresh** every 60 seconds via `dcc.Interval`

## Stack

| Layer | Technology |
|---|---|
| Framework | [Dash](https://dash.plotly.com/) |
| Visualization | [Plotly](https://plotly.com/python/) |
| Data | [yfinance](https://github.com/ranaroussi/yfinance) |
| UI Components | [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) |
| Data Processing | [Pandas](https://pandas.pydata.org/) |

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/ramiromantero/SLB_Dashboard.git
cd SLB_Dashboard
```

**2. Create and activate a virtual environment**
```bash
# Using venv
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # macOS/Linux

# Or using conda
conda create -n slb-dashboard python=3.12
conda activate slb-dashboard
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

Open your browser at `http://127.0.0.1:8050`

## Project Structure

```
SLB_Dashboard/
├── app.py              # Main application — layout, helpers and callbacks
├── requirements.txt    # Python dependencies
├── README.md
└── .gitignore
```

## Roadmap

- [ ] Correlation heatmap between assets
- [ ] Multi-asset comparison chart
- [ ] Technical indicators (RSI, Bollinger Bands)
- [ ] News feed integration