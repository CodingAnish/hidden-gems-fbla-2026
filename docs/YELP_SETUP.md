# Richmond, VA Businesses from Yelp

Hidden Gems can load real businesses in the Richmond, Virginia area from the Yelp Fusion API.

## 1. Get a Yelp API key

1. Go to [Yelp Developers](https://www.yelp.com/developers/v3/manage_app).
2. Sign in or create a Yelp account.
3. Click **Create App** and fill in app name, industry, contact email, description.
4. Choose the **Starter** (free) plan — no payment required.
5. Copy your **API Key** from the app page.

## 2. Add the key to config

Open **config.py** in the project folder and set:

```python
YELP_API_KEY = "your-api-key-here"
```

Or set the environment variable: `YELP_API_KEY=your-api-key-here`

## 3. Run the app

When you run `python -m web.app`:

- If **YELP_API_KEY** is set, the app will fetch businesses in **Richmond, VA** from Yelp (Food, Retail, Services, Entertainment, Health & Wellness) and add them to the database.
- If the key is missing or invalid, the app uses built-in sample businesses instead.

## 4. Refresh later (optional)

From the main menu you can use **Refresh Richmond businesses** (when the key is set) to fetch new businesses from Yelp and add any that aren’t already in the app. Existing businesses and your reviews/favorites are not removed.

## Limits

- Yelp’s free tier allows a limited number of API calls per day (e.g. 150–300). The app uses a few calls at startup when the key is set.
- Businesses are fetched by category (restaurants, shopping, local services, nightlife, gyms) and mapped to Hidden Gems categories. Only businesses with at least one Yelp review are returned by the API.
