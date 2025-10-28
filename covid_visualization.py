import pandas as pd
import matplotlib.pyplot as plt
import os

# Set file path
DATA_PATH = "data/owid-covid-data.csv"
OUT_DIR = "visuals"
os.makedirs(OUT_DIR, exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH)
print("Columns in file:\n", df.columns.tolist(), "\n")

# Rename for convenience
df = df.rename(columns={
    'Entity': 'location',
    'Day': 'date',
    'Cumulative excess deaths per 100,000 people (central estimate)': 'excess_deaths',
    'Total confirmed deaths due to COVID-19 per 100,000 people': 'covid_deaths'
})

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Filter for India (or change to another country)
india = df[df['location'].str.lower() == 'india'].copy()
india = india.sort_values('date')

if india.empty:
    print("⚠️ No data found for India. Check available countries:\n")
    print(df['location'].unique()[:10])
    raise SystemExit

# Plot 1: Excess deaths over time
plt.figure(figsize=(10, 6))
plt.plot(india['date'], india['excess_deaths'], label='Excess deaths per 100k (central estimate)', color='blue')
plt.title('Excess Deaths per 100,000 People in India (2020–2023)')
plt.xlabel('Date')
plt.ylabel('Deaths per 100,000')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'excess_deaths_india.png'), dpi=200)
plt.show()

# Plot 2: Confirmed COVID-19 deaths per 100k
plt.figure(figsize=(10, 6))
plt.plot(india['date'], india['covid_deaths'], label='Confirmed COVID-19 deaths per 100k', color='red')
plt.title('Confirmed COVID-19 Deaths per 100,000 People in India')
plt.xlabel('Date')
plt.ylabel('Deaths per 100,000')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'covid_deaths_india.png'), dpi=200)
plt.show()

print("\n✅ Charts saved in the 'visuals' folder:")
print(" - excess_deaths_india.png")
print(" - covid_deaths_india.png")

df = pd.read_csv("data/owid-covid-data.csv", parse_dates=['date'])

# Show first few rows
print(df[['date', 'location', 'total_cases', 'new_cases']].head())


#3.1 Total confirmed cases (cumulative)
plt.figure(figsize=(11,6))
plt.plot(india['date'], india['total_cases'], linewidth=2)
plt.title('Figure 3.1 — Total Confirmed COVID-19 Cases in India')
plt.xlabel('Date')
plt.ylabel('Cumulative Confirmed Cases')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/total_cases_india.png', dpi=200)
plt.show()

#3.2 Daily new cases (7- day average)
plt.figure(figsize=(11,6))
plt.plot(india['date'], india['new_cases_7d'], linewidth=1.5)
plt.title('Figure 3.2 — Daily New Cases (7-day avg) - India')
plt.xlabel('Date')
plt.ylabel('New Cases (7-day avg)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/new_cases_7d_india.png', dpi=200)
plt.show()

#3.3 Total confirmed deaths (cummalative)
fig, ax1 = plt.subplots(figsize=(11,6))
ax1.plot(india['date'], india['total_deaths'], color='tab:red', label='Total deaths')
ax1.set_ylabel('Total Deaths', color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')

ax2 = ax1.twinx()
ax2.plot(india['date'], india['new_deaths_7d'], color='tab:orange', alpha=0.8, label='New deaths (7d)')
ax2.set_ylabel('New Deaths (7-day avg)', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')

plt.title('Figure 3.3 — Deaths: cumulative and 7-day new deaths')
fig.tight_layout()
plt.savefig('visuals/deaths_india.png', dpi=200)
plt.show()


#3.4 Vaccinations (cummulative)
plt.figure(figsize=(11,6))
plt.plot(india['date'], india['people_vaccinated'], linewidth=2, color='green')
plt.title('Figure 3.4 — People vaccinated in India')
plt.xlabel('Date')
plt.ylabel('People vaccinated (cumulative)')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/vaccinated_india.png', dpi=200)
plt.show()

#4.1 Per-100k normalization (compare between countries)
df['cases_per_100k'] = 100000 * df['total_cases'] / df['population']

#4.2 Peak detection (dates of major waves)
peak_row = india.loc[india['new_cases_7d'].idxmax()]
print("Peak new cases (7d-avg):", peak_row['date'], peak_row['new_cases_7d'])

#5.1 Plotly line (browser interactive)
import plotly.express as px

fig = px.line(india, x='date', y='new_cases_7d',
              title='Daily New Cases (7-day avg) — India',
              labels={'new_cases_7d':'New cases (7-day avg)'})
fig.update_layout(template='plotly_white')
fig.write_html('visuals/interactive_new_cases_india.html')
fig.show()

#5.2 Choropleth (global view) — if you want world map
df_latest = df[df['date'] == '2021-05-01']   # choose date string or pd.Timestamp
fig = px.choropleth(df_latest, locations='iso_code', color='total_cases',
                    hover_name='location', title='Total cases on 2021-05-01',
                    color_continuous_scale='OrRd')
fig.write_html('visuals/choropleth_2021-05-01.html')
fig.show()

