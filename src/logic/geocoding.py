"""
Geocoding Module - Convert Addresses to Coordinates

Utilizes Google Geocoding API to convert business addresses into latitude/longitude
coordinates for map display and location-based queries.

Hidden Gems | FBLA 2026
"""
import requests
from typing import Optional, Dict, Tuple
import os
import logging

logger = logging.getLogger(__name__)

# Try to import from config, fall back to env variable
try:
    from config import GOOGLE_MAPS_API_KEY
except ImportError:
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")

GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"
RICHMOND_VA_BOUNDS = {
    "northeast": {"lat": 37.6, "lng": -77.3},
    "southwest": {"lat": 37.4, "lng": -77.5}
}


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """
    Convert an address to latitude and longitude coordinates.
    
    Uses Google Geocoding API to find coordinates for a given address string.
    Results are biased toward Richmond, VA area.
    
    Parameters:
        address (str): Full address string (e.g., "123 Main St, Richmond, VA 23219")
    
    Returns:
        tuple: (latitude, longitude) if successful, None if geocoding fails
    
    Example:
        >>> coords = geocode_address("1424 Westwood Ave, Richmond, VA 23227")
        >>> if coords:
        ...     lat, lng = coords
    """
    if not GOOGLE_MAPS_API_KEY:
        logger.warning("GOOGLE_MAPS_API_KEY not configured. Skipping geocoding.")
        return None
    
    if not address or not address.strip():
        logger.warning("Empty address provided to geocoding function")
        return None
    
    try:
        # Ensure Richmond, VA context for biased results
        geocoding_address = f"{address}, Richmond, VA" if "Richmond" not in address else address
        
        payload = {
            "address": geocoding_address,
            "key": GOOGLE_MAPS_API_KEY,
            "bounds": f"{RICHMOND_VA_BOUNDS['southwest']['lat']},{RICHMOND_VA_BOUNDS['southwest']['lng']}|{RICHMOND_VA_BOUNDS['northeast']['lat']},{RICHMOND_VA_BOUNDS['northeast']['lng']}"
        }
        
        # Make request with 5-second timeout
        response = requests.get(GEOCODING_API_URL, params=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for successful response
        if data.get("status") == "OK" and data.get("results"):
            location = data["results"][0]["geometry"]["location"]
            latitude = location.get("lat")
            longitude = location.get("lng")
            
            if latitude is not None and longitude is not None:
                logger.info(f"Geocoded '{address}' -> ({latitude}, {longitude})")
                return (latitude, longitude)
        elif data.get("status") == "ZERO_RESULTS":
            logger.warning(f"No geocoding results for address: {address}")
        else:
            logger.error(f"Geocoding API error: {data.get('status')} - {data.get('error_message', 'Unknown error')}")
        
        return None
        
    except requests.exceptions.RequestException as error:
        logger.error(f"Geocoding request failed for '{address}': {error}")
        return None
    except (KeyError, ValueError) as error:
        logger.error(f"Error parsing geocoding response for '{address}': {error}")
        return None


def geocode_batch(addresses: Dict[int, str]) -> Dict[int, Optional[Tuple[float, float]]]:
    """
    Geocode multiple addresses in bulk.
    
    Converts a dictionary of business IDs to addresses and returns coordinates
    for each address. Handles errors gracefully without stopping on individual failures.
    
    Parameters:
        addresses (dict): Mapping of business_id -> address_string
    
    Returns:
        dict: Mapping of business_id -> (latitude, longitude) or None
    
    Example:
        >>> to_geocode = {
        ...     1: "1424 Westwood Ave, Richmond, VA 23227",
        ...     2: "500 East Broad St, Richmond, VA 23219"
        ... }
        >>> results = geocode_batch(to_geocode)
    """
    results = {}
    for business_id, address in addresses.items():
        results[business_id] = geocode_address(address)
    return results


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate that coordinates represent a location in Richmond, VA area.
    
    Checks if provided coordinates fall within reasonable bounds for Richmond.
    
    Parameters:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        bool: True if coordinates are valid and in Richmond area, False otherwise
    """
    if latitude is None or longitude is None:
        return False
    
    # Richmond, VA approximate bounds
    lat_min, lat_max = 37.4, 37.6
    lng_min, lng_max = -77.5, -77.3
    
    is_valid = lat_min <= latitude <= lat_max and lng_min <= longitude <= lng_max
    
    if not is_valid:
        logger.warning(f"Coordinates ({latitude}, {longitude}) outside Richmond area bounds")
    
    return is_valid
