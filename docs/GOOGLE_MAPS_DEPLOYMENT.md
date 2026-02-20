# Google Maps Integration - Deployment Checklist

## Pre-Deployment

- [ ] **Get Google Maps API Key**
  - [ ] Create Google Cloud project
  - [ ] Enable Maps JavaScript API
  - [ ] Enable Geocoding API
  - [ ] Create API key (HTTP referrer restrictions recommended)

- [ ] **Update Configuration**
  - [ ] Copy `config.example.py` to `config.py`
  - [ ] Add `GOOGLE_MAPS_API_KEY` to `config.py`
  - [ ] OR set `GOOGLE_MAPS_API_KEY` environment variable

- [ ] **Update Dependencies**
  - [ ] Run `pip install -r requirements.txt`
  - [ ] Verify `requests` library installed: `python -c "import requests; print(requests.__version__)"`

## Deployment

### Local Development
```bash
cd /path/to/hidden-gems

# Install requirements (if not already done)
pip install -r requirements.txt

# Geocode existing businesses (populates lat/lng)
python scripts/geocode_businesses.py

# Start the Flask app
python -m web.app

# Open http://127.0.0.1:5000 in browser
# Navigate to /map after logging in
```

- [ ] Flask app starts without errors
- [ ] Map page loads at `/map`
- [ ] Markers visible on map
- [ ] Filters work (category, rating, deals)
- [ ] Clicking markers shows info window
- [ ] Clicking "Directions" opens Google Maps
- [ ] Clicking "Details" opens business profile

### Production Deployment (e.g., Render, Railway)

1. **Add Environment Variable**
   ```bash
   GOOGLE_MAPS_API_KEY=YOUR_KEY_HERE
   ```

2. **Ensure `requests` in requirements.txt**
   ```
   requests>=2.28.0
   ```

3. **Run Geocoding After Deployment**
   ```bash
   python scripts/geocode_businesses.py
   ```

4. **Verify Map Works**
   - [ ] Login to deployed app
   - [ ] Visit `/map`
   - [ ] Map loads and displays markers
   - [ ] Filters work correctly

## Database Migrations

- [ ] No migrations needed! (columns already exist)
- [ ] Run geocoding script to populate coordinates
- [ ] Verify businesses have non-null latitude/longitude

## Files to Deploy

```
✓ src/logic/geocoding.py
✓ scripts/geocode_businesses.py
✓ web/templates/map.html
✓ web/app.py (updated)
✓ web/templates/base.html (updated)
✓ config.example.py (updated)
✓ requirements.txt (updated)
✓ GOOGLE_MAPS_SETUP.md
✓ GOOGLE_MAPS_IMPLEMENTATION.md
✓ GOOGLE_MAPS_QUICK_START.md
✓ README.md (updated)
```

## Verification Steps

### Backend Routes
```bash
# Verify /map route loads
curl -I http://localhost:5000/map

# Should redirect to login (302) if not authenticated
```

### Frontend
- [ ] Open Developer Tools (F12)
- [ ] Check Console tab for JavaScript errors
- [ ] Verify `google` object is available
- [ ] Check Network tab for successful Google Maps API calls

### Functionality
- [ ] Map initializes and centers on Richmond, VA
- [ ] Business markers load (colored circles)
- [ ] Map controls work (zoom, pan, fullscreen)
- [ ] Click marker → info window appears
- [ ] Click business in sidebar → map highlights it
- [ ] Category filter → updates markers and count
- [ ] Rating filter → filters by star rating
- [ ] Deals checkbox → shows only deal businesses
- [ ] Reset button → clears all filters
- [ ] "Directions" link → opens Google Maps
- [ ] Responsive on mobile devices

## Monitoring

### API Usage
Check Google Cloud Console regularly:
1. Go to [APIs & Services > Dashboard](https://console.cloud.google.com/apis/dashboard)
2. Monitor usage of:
   - Maps JavaScript API (quota: 25,000/day free)
   - Geocoding API (quota: 40,000/month free)

### Logs
```bash
# Check Flask app logs for errors
tail -f app.log | grep -i "map\|geocod\|google"

# Monitor geocoding attempts
python scripts/geocode_businesses.py 2>&1 | tee geocoding.log
```

## Rollback Plan

If map feature needs to be disabled:

1. **Remove map navigation link**
   - Edit `web/templates/base.html`
   - Remove or comment out the Map nav link

2. **Disable /map route**
   - Edit `web/app.py`
   - Comment out the `@app.route("/map")` and `map_view()` function

3. **Optional: Remove files**
   - Delete `src/logic/geocoding.py`
   - Delete `scripts/geocode_businesses.py`
   - Delete `web/templates/map.html`
   - Remove `requests` from `requirements.txt`

## Troubleshooting

### Map won't load
1. Check browser console (F12) for errors
2. Verify API key in Google Cloud Console > Credentials
3. Check that Maps JavaScript API is enabled
4. Verify API key hasn't hit daily quota

### No markers showing
1. Confirm businesses have addresses: `SELECT COUNT(*) FROM businesses WHERE address IS NOT NULL`
2. Confirm businesses have coordinates: `SELECT COUNT(*) FROM businesses WHERE latitude IS NOT NULL`
3. Run `python scripts/geocode_businesses.py` to populate coordinates
4. Check for SQL errors in `geocoding.py` log output

### Geocoding fails
1. Verify `GOOGLE_MAPS_API_KEY` is set correctly
2. Check that Geocoding API is enabled in Google Cloud Console
3. Ensure API key doesn't have application restrictions preventing localhost
4. Monitor API quota in Cloud Console

### Performance issues
1. Check number of businesses: `SELECT COUNT(*) FROM businesses WHERE latitude IS NOT NULL`
2. If > 500, consider implementing marker clustering
3. Monitor browser memory usage (F12 > Performance)
4. Check network waterfall for slow requests

## Post-Deployment

- [ ] Update user documentation
- [ ] Announce map feature to users
- [ ] Monitor API usage for first week
- [ ] Collect user feedback
- [ ] Plan future enhancements (clustering, heat maps, etc.)

## Documentation Updates

- [ ] Link to [GOOGLE_MAPS_QUICK_START.md](GOOGLE_MAPS_QUICK_START.md) in main README
- [ ] Update Help/FAQ page with map instructions
- [ ] Create video tutorial (optional)
- [ ] Update deployment documentation

---

**Deployment Date**: ___________  
**Deployed By**: ___________  
**API Key Status**: ✓ Active / ⚠️ Needs Renewal  
**Geocoding Status**: ✓ Complete / ⏳ In Progress  

**Sign Off**:  
- Developer: ___________
- QA: ___________
- Deployment: ___________
