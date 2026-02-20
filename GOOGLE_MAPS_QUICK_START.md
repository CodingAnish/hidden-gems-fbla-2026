# Google Maps Integration - Quick Reference

## 🎯 What Was Added

A complete interactive map feature for Hidden Gems that displays all businesses in Richmond, VA with:
- **Color-coded markers** by business category
- **Filtering** by category, rating, and deals
- **Sidebar** with business list sorted by rating  
- **Info windows** with directions and details links
- **Responsive design** for desktop and mobile

## 📦 New Files

```
src/logic/geocoding.py           # Geocoding utilities
scripts/geocode_businesses.py    # Geocoding script
web/templates/map.html           # Map page template
GOOGLE_MAPS_SETUP.md             # Complete setup guide
GOOGLE_MAPS_IMPLEMENTATION.md    # Implementation details
```

## 🚀 Quick Setup (5 minutes)

### 1. Get API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a project and enable:
   - **Maps JavaScript API**
   - **Geocoding API**
3. Create an API Key (Credentials > API Key)

### 2. Add to Config
```python
# config.py
GOOGLE_MAPS_API_KEY = "YOUR_KEY_HERE"
```

Or use environment variable:
```bash
export GOOGLE_MAPS_API_KEY="YOUR_KEY_HERE"
```

### 3. Geocode Businesses
```bash
python scripts/geocode_businesses.py
```

This populates lat/lng for all businesses without coordinates.

### 4. Done!
- Login to the app
- Click **🗺️ Map** in navigation
- Explore the interactive map

## 📍 Route

- **URL**: `/map`
- **Requires**: User authentication (login)
- **Returns**: Interactive map with all geolocated businesses

## 🎨 Features

### Markers
- 🍽️ Orange-Red: Food & Dining
- 🛍️ Orange: Shopping
- 🎭 Purple: Entertainment
- 🔧 Blue: Services
- 📍 Green: Other

### Filters
- **Category** — Filter by business type
- **Rating** — Show only 3+ or 4+ star businesses
- **Deals** — Show only businesses with active promotions
- **Reset** — Clear all filters

### Sidebar
- Lists all visible businesses
- Sorted by rating (highest first)
- Click to highlight on map
- Shows rating, reviews, address, deals

### Info Window
- Click marker to open details
- Shows: Name, Category, Address, Phone, Rating
- **Directions** — Open Google Maps navigation
- **Details** — Link to business profile page

## 🔧 Files Modified

- `web/app.py` — Added `/map` route
- `web/templates/base.html` — Added Map nav link
- `config.example.py` — Added API key field
- `requirements.txt` — Added requests library
- `README.md` — Updated features list

## ⚙️ Configuration

### Database
Already has `latitude` and `longitude` columns. No schema changes needed.

### Geocoding
Converts addresses to coordinates. Optional but required for map to show businesses.

### Markers
Auto-generated from business data. Size/color based on category and rating.

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Loading map..." | Check API key in config.py or .env |
| No businesses visible | Run `python scripts/geocode_businesses.py` |
| Markers not showing | Verify businesses have address data in database |
| API errors | Check Google Cloud Console quotas |

See [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md) for detailed troubleshooting.

## 📱 Mobile

- Responsive design (tested on all breakpoints)
- Touch-friendly markers and controls
- Auto-fits to portrait/landscape
- Filter controls stack vertically
- Sidebar becomes collapsible on small screens

## 🔐 Security Notes

- API key can be restricted in Google Cloud Console
- Set to your domain(s) only
- Select Maps JavaScript API + Geocoding API (not all APIs)
- Monitor usage in Cloud Console

## 📊 Performance

- Filters work client-side (instant response)
- All data sent with page (no API calls after load)
- Supports 100+ businesses efficiently
- Consider pagination for 500+ businesses

## 🎓 Learning Resources

- [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md) — Complete guide
- [GOOGLE_MAPS_IMPLEMENTATION.md](GOOGLE_MAPS_IMPLEMENTATION.md) — Technical details
- `src/logic/geocoding.py` — Geocoding functions (docstrings)
- `web/templates/map.html` — Map implementation (comments)

## ✨ Future Ideas

- Heat maps (density visualization)
- Marker clustering (large datasets)
- "My Location" button
- Search box with autocomplete
- Reverse geocoding (click map to search)
- Route optimization (visit multiple businesses)

---

**Need Help?** See [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md) for comprehensive guide.
