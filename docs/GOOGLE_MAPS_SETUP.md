# Google Maps Integration Guide

## Overview

Hidden Gems now includes an interactive map view that displays all businesses in Richmond, VA with their locations. Users can:

- 🗺️ **View businesses on an interactive map** centered on Richmond, VA
- 🎨 **Color-coded markers** by business category (Food, Shopping, Entertainment, Services, Other)
- 🔍 **Filter by category, rating, and special deals**
- 📍 **Click markers** to see business details and get directions
- 📋 **Browse businesses in a side panel** sorted by rating
- 🔗 **Quick links** to business details and Google Maps navigation

## Setup Instructions

### 1. Get a Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API**
   - **Geocoding API**
4. Create an API key:
   - Go to **Credentials** > **Create Credentials** > **API Key**
   - Copy the generated key
5. **Restrict your API key** (important for security):
   - Click on the key to edit it
   - Under **Application restrictions**, select **HTTP referrers (web sites)**
   - Add your domain(s) (e.g., `localhost:5000/*` for local development)
   - Under **API restrictions**, select **Restrict key** and choose:
     - Maps JavaScript API
     - Geocoding API

### 2. Add Your Google Maps API Key

#### Option A: Using config.py (Recommended for development)

1. Copy `config.example.py` to `config.py` (if not already done)
2. Add your API key to `config.py`:
   ```python
   GOOGLE_MAPS_API_KEY = "YOUR_API_KEY_HERE"
   ```

#### Option B: Using Environment Variables (Recommended for production)

Add to your `.env` file:
```
GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
```

Or set the environment variable:
```bash
export GOOGLE_MAPS_API_KEY="YOUR_API_KEY_HERE"
```

### 3. Geocode Existing Businesses

The database already has `latitude` and `longitude` columns for all businesses. Use the geocoding utility to populate coordinates for existing businesses:

```bash
# From project root
python scripts/geocode_businesses.py
```

This script will:
- Find all businesses without coordinates
- Use the Google Geocoding API to convert addresses to lat/lng
- Update the database automatically
- Show a summary of successful and failed geocoding

Example output:
```
INFO: Found 25 businesses needing geocoding
INFO:   ✓ Business #1 (Local Coffee): (37.5412, -77.4360)
INFO:   ✓ Business #2 (Art Gallery): (37.5298, -77.4298)
...
==================================================
Geocoding Complete:
  ✓ Successfully geocoded: 23
  ✗ Failed to geocode: 2
  Total: 25
==================================================
```

## Using the Map

### For Users

1. **Navigate to the map**: Click the **🗺️ Map** link in the main navigation
2. **View businesses**: See all business locations marked on the map
3. **Filter results**:
   - Select a **Category** to show only businesses in that category
   - Set a **Minimum Rating** to filter by star rating
   - Check **Show Deals Only** to see only businesses with active promotions
   - Click **Reset Filters** to clear all filters
4. **View business details**:
   - Click a marker on the map
   - Or click a business in the **Nearby Businesses** side panel
   - Click **Directions** to open Google Maps navigation
   - Click **Details** to view the full business profile

### Features

#### Interactive Map
- **Zoom in/out** to explore specific areas
- **Drag to pan** across Richmond
- **Toggle satellite/map view** using the map type controls
- **Full screen mode** available in the top-right corner
- **Street View** available for detailed location exploration

#### Color-Coded Markers
- 🍽️ **Food & Dining** (Orange-Red) - Restaurants, Cafes, Bakeries
- 🛍️ **Shopping** (Orange) - Retail, Boutiques, Markets
- 🎭 **Entertainment** (Purple) - Events, Arts, Recreation
- 🔧 **Services** (Blue) - Salons, Repairs, Professional Services
- 📍 **Other** (Green) - Miscellaneous Businesses

#### Side Panel
- Lists all visible businesses sorted by rating
- Shows rating, review count, category, and address
- Displays **🎟️ Special Deal** badge for businesses with active promotions
- Click any business to highlight it and update the map

## Architecture

### Database Schema

Businesses table includes location fields:
```sql
CREATE TABLE businesses (
    ...
    latitude REAL,          -- Geographic latitude coordinate
    longitude REAL,         -- Geographic longitude coordinate
    address TEXT,           -- Full address string for geocoding
    average_rating REAL,    -- Calculated from reviews
    total_reviews INTEGER,  -- Number of user reviews
    ...
)
```

### New Files

1. **`src/logic/geocoding.py`** — Geocoding utilities
   - `geocode_address(address)` — Convert single address to coordinates
   - `geocode_batch(addresses)` — Batch geocode multiple addresses
   - `validate_coordinates(lat, lng)` — Check if coordinates are in Richmond area

2. **`scripts/geocode_businesses.py`** — Geocoding utility script
   - Populates coordinates for all businesses without them
   - Can be run multiple times safely (idempotent)

3. **`web/templates/map.html`** — Map page template
   - Interactive Google Map with all features
   - Filter controls and business list sidebar
   - Responsive design (works on desktop and mobile)

4. **`web/static/map.css`** — Map styling (included via styles)

### Flask Routes

#### GET `/map`
Displays the interactive map page. Requires user authentication.

Response includes:
- `businesses` — All businesses with coordinates (GeoJSON-compatible JSON)
- `google_maps_api_key` — API key for JavaScript map initialization
- `categories` — Available business categories for filter dropdown

Example response structure:
```json
{
  "businesses": [
    {
      "id": 1,
      "name": "Local Coffee",
      "category": "Food",
      "latitude": 37.5412,
      "longitude": -77.4360,
      "address": "123 Main St, Richmond, VA 23219",
      "average_rating": 4.5,
      "total_reviews": 12,
      "phone": "(804) 555-0100",
      "deals": [{"id": 1, "description": "Free coffee on 2nd visit"}]
    }
    ...
  ]
}
```

## Troubleshooting

### Map not loading

**Problem**: "Loading map..." message persists
- **Solution**: Check that `GOOGLE_MAPS_API_KEY` is set correctly
- **Solution**: Verify API key has Maps JavaScript API enabled
- **Solution**: Check browser console (F12) for JavaScript errors

### No businesses showing on map

**Problem**: Map loads but no business markers appear
- **Solution**: Run `python scripts/geocode_businesses.py` to populate coordinates
- **Solution**: Verify businesses have address data: `SELECT COUNT(*) FROM businesses WHERE address IS NULL`
- **Solution**: Check that latitude/longitude values are valid: `SELECT id, latitude, longitude FROM businesses WHERE latitude IS NULL`

### "Geocoding failed" errors

**Problem**: `geocode_businesses.py` can't find addresses
- **Solution**: Verify `GOOGLE_MAPS_API_KEY` is set
- **Solution**: Check that Geocoding API is enabled in Google Cloud Console
- **Solution**: Ensure addresses are in format: "Street, City, State ZIP"
- **Solution**: Check API quota limits at [Google Cloud Console Quotas](https://console.cloud.google.com/apis/dashboard)

### API key appears in client-side code

**Problem**: "API key exposed in JavaScript"
- **Solution**: This is normal and expected. Google Maps API keys are meant to be public.
- **Mitigation**: Use API key restrictions in Google Cloud Console:
  - Set **Application restrictions** to your domain(s)
  - Set **API restrictions** to Maps JavaScript API + Geocoding API only
  - Monitor API usage regularly

## Performance Considerations

### Map with 100+ businesses

- All businesses load into map at initialization
- Filtering is done client-side (fast, no server requests)
- Marker clustering can be added for large datasets
- Consider pagination or limiting initial load if > 500 businesses

### API Quotas

**Free tier limits** (check at [Google Cloud Console](https://console.cloud.google.com/apis/dashboard)):
- Maps JavaScript API: 25,000 loads per day ($5 per 1000 after)
- Geocoding API: 40,000 requests per month ($0.50 per 1000 after)

Monitor usage:
```bash
# Log all geocoding requests
tail -f sys.log | grep geocoding
```

## Future Enhancements

Potential features to add:

1. **Marker Clustering** — Group nearby markers at low zoom levels
2. **Heat Maps** — Visualize business density and popularity
3. **Route Optimization** — Plot the most efficient route through multiple businesses
4. **User Location** — "My Location" button to show user on map
5. **Favorites on Map** — Highlight user's favorite businesses
6. **Search Box** — Google Places autocomplete for addresses
7. **Street View** — Embedded Street View for business locations
8. **Traffic Layer** — Real-time traffic overlay
9. **Reverse Geocoding** — Click map to search for nearby businesses
10. **Distance Matrix** — Show estimated travel time from user location

## Resources

- [Google Maps JavaScript API Documentation](https://developers.google.com/maps/documentation/javascript)
- [Google Geocoding API Documentation](https://developers.google.com/maps/documentation/geocoding)
- [Advanced Markers Documentation](https://developers.google.com/maps/documentation/javascript/advanced-markers)
- [Maps API Quotas and Limits](https://developers.google.com/maps/billing-and-pricing/usage-and-billing)

## Support

For issues or questions about the map implementation:

1. Check troubleshooting section above
2. Review Google Cloud Console API quotas and usage
3. Check browser console (F12) for JavaScript errors
4. Verify all setup instructions completed

---

**Last updated**: 2024  
**Compatible with**: Hidden Gems v1.0+
