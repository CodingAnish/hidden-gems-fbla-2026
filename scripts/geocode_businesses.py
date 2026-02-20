"""
Database Geocoding Utility - Populate latitude/longitude for existing businesses

This script geocodes all businesses without coordinates using the Google Geocoding API.
Run this after setting up your GOOGLE_MAPS_API_KEY in config.py.

Usage: python scripts/geocode_businesses.py
"""
import sys
import os

# Setup path to allow imports from root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, '.env'))
except ImportError:
    pass

from src.database.db import get_connection
from src.logic.geocoding import geocode_address, validate_coordinates
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def geocode_businesses():
    """
    Geocode all businesses in the database that don't have coordinates.
    """
    connection = get_connection()
    cursor = connection.cursor()
    
    # Get all businesses without coordinates
    cursor.execute("""
        SELECT id, name, address, latitude, longitude 
        FROM businesses 
        WHERE (latitude IS NULL OR longitude IS NULL) 
        AND address IS NOT NULL
        ORDER BY id
    """)
    
    businesses_to_geocode = cursor.fetchall()
    
    if not businesses_to_geocode:
        logger.info("✓ All businesses already have coordinates!")
        connection.close()
        return
    
    logger.info(f"Found {len(businesses_to_geocode)} businesses needing geocoding")
    
    geocoded_count = 0
    failed_count = 0
    
    for business_row in businesses_to_geocode:
        business_id = business_row['id']
        name = business_row['name']
        address = business_row['address']
        
        if not address or not address.strip():
            logger.warning(f"  ✗ Business #{business_id} ({name}): No address provided")
            failed_count += 1
            continue
        
        # Geocode this business
        coords = geocode_address(address)
        
        if coords:
            latitude, longitude = coords
            
            # Validate coordinates
            if validate_coordinates(latitude, longitude):
                # Update database
                cursor.execute("""
                    UPDATE businesses 
                    SET latitude = ?, longitude = ? 
                    WHERE id = ?
                """, (latitude, longitude, business_id))
                
                connection.commit()
                logger.info(f"  ✓ Business #{business_id} ({name}): ({latitude:.4f}, {longitude:.4f})")
                geocoded_count += 1
            else:
                logger.warning(f"  ✗ Business #{business_id} ({name}): Coordinates outside Richmond area")
                failed_count += 1
        else:
            logger.warning(f"  ✗ Business #{business_id} ({name}): Geocoding failed for '{address}'")
            failed_count += 1
    
    connection.close()
    
    # Print summary
    logger.info("")
    logger.info("=" * 50)
    logger.info(f"Geocoding Complete:")
    logger.info(f"  ✓ Successfully geocoded: {geocoded_count}")
    logger.info(f"  ✗ Failed to geocode: {failed_count}")
    logger.info(f"  Total: {geocoded_count + failed_count}")
    logger.info("=" * 50)
    
    if geocoded_count > 0:
        logger.info("You can now view businesses on the map at /map")

if __name__ == "__main__":
    try:
        geocode_businesses()
    except KeyboardInterrupt:
        logger.info("\nGeocoding cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during geocoding: {e}")
        sys.exit(1)
