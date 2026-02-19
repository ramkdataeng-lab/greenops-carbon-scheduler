
"""
GreenOps - Snowflake Query Carbon Calculator

Estimates the carbon footprint of a Snowflake query based on warehouse size, 
query duration, and region.

Based on the GreenOps Framework by Ramkumar Gudivada, IEEE Senior Member.
"""

WAREHOUSE_SIZES = {
    'X-Small': 1,    # Credits per hour
    'Small': 2,
    'Medium': 4,
    'Large': 8,
    'X-Large': 16,
    '2X-Large': 32,
    '3X-Large': 64,
    '4X-Large': 128
}

REGIONAL_INTENSITY = {
    'us-east-1': 380,   # Approx gCO2/kWh (Virginia - Coal/Gas Heavy)
    'us-west-2': 150,   # Approx gCO2/kWh (Oregon - Hydro Heavy)
    'eu-west-1': 230,   # Approx gCO2/kWh (Ireland)
    'ap-southeast-2': 500 # Approx gCO2/kWh (Sydney - Coal Heavy)
}

# Assume roughly 200W per credit (server) based on typical cloud instance specs
WATTS_PER_CREDIT = 200 
PUE = 1.1 # Power Usage Effectiveness for modern cloud provider

def estimate_query_carbon(warehouse_size, duration_seconds, region='us-east-1'):
    """
    Calculates the estimated carbon footprint of a single query execution.
    
    Formula: 
    Carbon (g) = Power (kW) * Time (hours) * PUE * Grid Intensity (gCO2/kWh)
    """
    credits_per_hour = WAREHOUSE_SIZES.get(warehouse_size, 1)
    power_watts = credits_per_hour * WATTS_PER_CREDIT
    power_kw = power_watts / 1000.0
    
    time_hours = duration_seconds / 3600.0
    
    carbon_intensity = REGIONAL_INTENSITY.get(region, 300) # Default to global avg if region unknown
    
    total_emissions_grams = power_kw * time_hours * PUE * carbon_intensity
    
    return {
        'warehouse_size': warehouse_size,
        'duration_seconds': duration_seconds,
        'region': region,
        'grid_intensity': carbon_intensity,
        'estimated_emissions_gCO2': round(total_emissions_grams, 2)
    }

if __name__ == "__main__":
    # Example usage:
    # A 5-minute query on a Large warehouse in Virginia
    result = estimate_query_carbon('Large', 300, 'us-east-1')
    
    print(f"--- Snowflake Query Carbon Estimate ---")
    print(f"Warehouse: {result['warehouse_size']}")
    print(f"Duration: {result['duration_seconds']}s")
    print(f"Region: {result['region']} ({result['grid_intensity']} gCO2/kWh)")
    print(f"Estimated Impact: {result['estimated_emissions_gCO2']} gCO2")
