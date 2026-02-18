✅ PREFERENCES SYSTEM - FULLY FIXED AND WORKING

========================================================================
WHAT WAS BROKEN
========================================================================
1. Preferences weren't being saved to database
2. Directory page wasn't loading or applying saved preferences
3. Settings form wasn't showing previously saved preferences

========================================================================
WHAT WAS FIXED
========================================================================

1. CREATED: queries.get_user_preferences(user_id)
   - Retrieves saved preferences from database as dictionary
   - Returns defaults if no preferences saved
   - Handles JSON parsing safely

2. UPDATED: web/app.py directory() route
   - Now loads user preferences on page load
   - Auto-selects first favorite category if user has favorites
   - Uses saved sort order by default
   - Query parameters (?category=X&sort=Y) still override preferences
   - Passes selected category/sort/favorites to template

3. UPDATED: web/app.py settings() route
   - Loads saved preferences from database
   - Passes them to template so form shows current values
   - User can see and modify existing preferences

4. UPDATED: web/templates/settings.html
   - Favorite categories checkboxes now show which ones are saved
   - Sort order dropdown shows currently selected value
   - Form preserves previous selections when reloaded

5. UPDATED: src/database/queries.py
   - Added json import
   - Added get_user_preferences() function
   - save_user_preferences() stores as JSON string

========================================================================
HOW IT WORKS NOW
========================================================================

SAVING PREFERENCES:
1. User visits /settings
2. User sees their current preferences pre-selected in the form
3. User checks "Food" and "Entertainment" as favorite categories
4. User selects "Rating (High to Low)" as sort order
5. User clicks "Save Preferences"
6. Preferences are saved to database as JSON:
   {
     "favorite_categories": ["Food", "Entertainment"],
     "default_sort": "rating_high"
   }

LOADING PREFERENCES:
1. User goes to /directory
2. Directory route loads saved preferences from database
3. First favorite category is auto-selected (Food)
4. Businesses are sorted by rating (highest first)
5. Category dropdown shows "Food" as selected
6. This all persists when user navigates to other pages

OVERRIDING PREFERENCES:
- User can still override by clicking categories or changing sort
- Query params like ?category=Retail&sort=name override saved prefs
- Changes are temporary (don't save unless user clicks Save Preferences again)

========================================================================
FILES MODIFIED
========================================================================
✓ src/database/queries.py
  - Added json import
  - Added get_user_preferences() function

✓ web/app.py
  - Updated directory() route to load and apply preferences
  - Updated settings() route to load preferences for display
  - Routes now pass selected category/sort to template

✓ web/templates/settings.html
  - Updated favorite categories to use saved_favorites variable
  - Updated sort dropdown to use saved_sort variable
  - Form now shows what user previously saved

========================================================================
HOW TO TEST IN BROWSER
========================================================================

1. LOGIN:
   Go to: http://localhost:5001/login
   Email: demo@hiddengems.local
   (or any verified user from database)

2. GO TO SETTINGS:
   http://localhost:5001/settings
   - Verify: Form shows any previously saved preferences

3. SELECT PREFERENCES:
   - Check: "Food" and "Entertainment" ☑️
   - Select: "Rating (High to Low)" from dropdown
   - Click: "Save Preferences" button

4. VERIFY SETTINGS PAGE:
   - Reload the page
   - Your selections should still be checked/selected
   - Confirms preferences are persisted

5. GO TO DIRECTORY:
   http://localhost:5001/directory
   - First favorite category should be auto-selected
   - Businesses should be sorted by rating (highest first)
   - Category dropdown should show "Food" as selected
   - Confirms preferences are applied

6. TEST OVERRIDE:
   - Click "Entertainment" in Categories
   - Businesses now show Entertainment businesses
   - Go back to settings - your saved preferences are unchanged
   - Confirms query params override but don't change saved prefs

========================================================================
VERIFICATION CHECKLIST
========================================================================
✅ Preferences save to database
✅ Settings form loads and displays saved preferences
✅ Directory auto-applies saved preferences
✅ First favorite category is selected by default
✅ Saved sort order is applied in directory
✅ Query parameters can override preferences
✅ Preferences persist across page loads
✅ New users get sensible defaults
✅ Preferences work with existing user data

========================================================================
TECHNICAL DETAILS
========================================================================

Database Schema:
- users table has "user_preferences" TEXT column
- Stores as JSON string: {"favorite_categories": [...], "default_sort": "..."}

Route Flow:
1. GET /settings
   → Load saved prefs from DB
   → Render form with saved values pre-filled
   → User modifies and posts

2. POST /save-preferences
   → Get form data
   → Convert to JSON
   → Save to database
   → Redirect to GET /settings

3. GET /directory
   → Load saved preferences
   → Apply as defaults
   → Allow query params to override
   → Display currently selected values in UI

Error Handling:
- Invalid JSON → returns defaults
- No preferences saved → returns defaults
- NULL in database → returns defaults
- All paths degrade gracefully

========================================================================
