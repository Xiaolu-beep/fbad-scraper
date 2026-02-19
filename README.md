# fbad-scraper

A Python tool to scrape Facebook Marketplace ads (mainly Mercedes Sprinter, Volkswagen Crafter, Renault Master, Fiat Ducato, Ford Transit vans in Western Australia) and extract key details into a CSV for analysis.

### Goal
Collect historical and current van sale data to:
- Understand real market values in Perth/Bunbury/WA
- Track price trends over time
- Identify good deals for car flipping / camper conversions
- Build a personal archive of listings (kms, transmission, price, location, seller, etc.)

### Features (current & planned)
- Selenium scraper for Marketplace item pages
- Persistent Chrome profile to minimize 2FA/login issues
- Llama 3.1 8B (via Ollama) for smart extraction from messy descriptions
- Daily scheduled runs (via Windows Task Scheduler)
- CSV output with columns: Camper/Van, Model, A/M, WB/H, Year, Kms, Price, Location, Market Time, Sold, Seller, Link

### Planned improvements
- Auto-search for new listings (e.g. "Sprinter Perth under 320000kms")
- Better handling of FB anti-bot measures and dynamic loading
- Error logging and retry logic
- Data cleaning / duplicate detection

### Requirements
- Python 3.10+
- Ollama running locally with llama3.1:8b-instruct-q4_K_M
- Chrome browser installed
- pip install selenium webdriver-manager pandas requests

### Usage
1. Run `ollama serve` in one terminal
2. Double-click `run_scraper.bat`
3. Complete FB login/2FA once (persistent profile remembers after)
4. Check `Van_sales.csv` for results
5. Debug log in `scraper_debug.log`

### Notes
- Use a dedicated FB account to avoid main account bans
- Respect FB terms — this is for personal research only
