import requests
import folium

# Overpass API
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Approximate bounding box for Worcester, MA
WORCESTER_BBOX = {
    "lat_min": 42.249,  # south
    "lat_max": 42.307,  # north
    "lon_min": -71.822, # west
    "lon_max": -71.772, # east
}

def build_query(business_type, city="Worcester"):
    """
    Build a dynamic Overpass QL query for a specific business type in a city.
    """
    query = f"""
    [out:json][timeout:90];
    area["name"="{city}"]["boundary"="administrative"]["admin_level"="8"]->.searchArea;
    (
      node["amenity"="{business_type}"](area.searchArea);
      way["amenity"="{business_type}"](area.searchArea);
      relation["amenity"="{business_type}"](area.searchArea);
    );
    out center;
    """
    return query

def query_overpass(business_type):
    """
    Query the Overpass API for a given business type and return results with a simple score.
    """
    response = requests.post(OVERPASS_URL, data={"data": build_query(business_type)})
    if response.status_code != 200:
        print("Error querying Overpass API:", response.status_code)
        return []

    data = response.json()
    results = []
    for element in data.get("elements", []):
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")
        if lat is None or lon is None:
            continue
        name = element.get("tags", {}).get("name", "N/A")
        score = len(element.get("tags", {}))  # simple proxy for "prominence"
        results.append({"name": name, "lat": lat, "lon": lon, "score": score})
    return results

def filter_within_bbox(results, bbox):
    """
    Filter results to only include those within the specified bounding box.
    """
    filtered = []
    for r in results:
        if bbox["lat_min"] <= r["lat"] <= bbox["lat_max"] and bbox["lon_min"] <= r["lon"] <= bbox["lon_max"]:
            filtered.append(r)
    return filtered

def plot_top10_on_map(results, filename="top10_businesses.html"):
    """
    Plot top 10 results on a Folium map.
    """
    top10 = results[:10]
    if not top10:
        print("No results to plot.")
        return

    # Center map on average coordinates of top 10
    avg_lat = sum(r['lat'] for r in top10) / len(top10)
    avg_lon = sum(r['lon'] for r in top10) / len(top10)
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=14)

    for r in top10:
        folium.Marker(
            [r['lat'], r['lon']],
            popup=f"{r['name']} (score: {r['score']})"
        ).add_to(m)

    # Fit map bounds to markers
    m.fit_bounds([[r['lat'], r['lon']] for r in top10])
    m.save(filename)
    print(f"Map saved to {filename}")

def main():
    print("Overpass Business Query for Worcester, MA")
    business_type = input("Enter business type (e.g., 'cafe', 'car_dealer'): ").strip()

    print(f"\nSearching for '{business_type}' in Worcester, MA...")
    results = query_overpass(business_type)

    # Filter results to bounding box
    results = filter_within_bbox(results, WORCESTER_BBOX)

    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)

    if not results:
        print("No results found within Worcester bounding box.")
        return

    print("\nTop 10 results:")
    for idx, r in enumerate(results[:10], start=1):
        print(f"{idx}. {r['name']} (score: {r['score']})")

    # Plot on map
    plot_top10_on_map(results)

if __name__ == "__main__":
    main()