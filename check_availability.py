#!/usr/bin/env python3
"""
Check for 1 bedroom or 1 bedroom + den apartment availability at Union 346.
Exit code 0 if available, 1 if not available.
"""
import gzip
import json
import sys
import urllib.request

API_URL = "https://sightmap.com/app/api/v1/rkwnqjo8wd2/sightmaps/45000"

def check_one_bedroom_availability():
    """Check if any 1 bedroom or 1 bed + den apartments are available."""
    try:
        # Make API request with compression headers
        req = urllib.request.Request(
            API_URL,
            headers={
                'Accept-Encoding': 'gzip, deflate, br',
                'User-Agent': 'Mozilla/5.0'
            }
        )

        with urllib.request.urlopen(req) as response:
            # Handle gzip-compressed response
            content = response.read()
            if response.info().get('Content-Encoding') == 'gzip':
                content = gzip.decompress(content)
            data = json.loads(content.decode('utf-8'))

        # Get available units
        units = data.get('data', {}).get('units', [])
        floor_plans = data.get('data', {}).get('floor_plans', [])

        # Create a map of floor_plan_id to floor plan details
        floor_plan_map = {
            fp['id']: {
                'bedroom_count': fp.get('bedroom_count', -1),
                'filter_label': fp.get('filter_label', ''),
                'name': fp.get('name', '')
            }
            for fp in floor_plans
        }

        # Check if any available unit is a 1 bedroom or 1 bed + den
        target_units = []
        for unit in units:
            floor_plan_id = unit.get('floor_plan_id')
            if floor_plan_id:
                fp_info = floor_plan_map.get(floor_plan_id, {})
                bedroom_count = fp_info.get('bedroom_count', -1)
                filter_label = fp_info.get('filter_label', '').lower()

                # Match: bedroom_count == 1 OR filter_label contains "bed" and "den"
                is_one_bedroom = bedroom_count == 1
                is_den = 'den' in filter_label and 'bed' in filter_label

                if is_one_bedroom or is_den:
                    target_units.append({
                        'unit_number': unit.get('display_unit_number', 'Unknown'),
                        'price': unit.get('display_price', 'N/A'),
                        'available_on': unit.get('display_available_on', 'N/A'),
                        'type': fp_info.get('filter_label', 'Unknown')
                    })

        if target_units:
            print(f"✅ Found {len(target_units)} one-bedroom apartment(s) available!")
            print("\nDetails:")
            for unit in target_units:
                print(f"  • {unit['unit_number']} ({unit['type']}) - {unit['price']} - {unit['available_on']}")

            # Output JSON for GitHub Actions to parse
            print("\n__UNITS_JSON__")
            print(json.dumps(target_units))
            print("__END_JSON__")
            return True
        else:
            print("❌ No one-bedroom or one-bedroom + den apartments available.")
            print(f"Total available units: {len(units)} (all other types)")
            return False

    except Exception as e:
        print(f"❌ Error checking availability: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    available = check_one_bedroom_availability()
    sys.exit(0 if available else 1)
