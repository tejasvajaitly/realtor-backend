from flask import Flask, request, jsonify
from flask_cors import CORS
from homeharvest import scrape_property
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        location = data.get('location', 'San Diego, CA')
        listing_type = data.get('listing_type', 'sold')
        past_days = data.get('past_days', 30)

        # Generate filename based on current timestamp
        current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"HomeHarvest_{current_timestamp}.csv"

        properties = scrape_property(
            location=location,
            listing_type=listing_type,
            past_days=past_days
        )
        print(f"Number of properties: {len(properties)}")

        # Export to csv
        properties.to_csv(filename, index=False)
        print(properties.head())

        # Create a list of dictionaries from the properties DataFrame for JSON response
        properties_list = properties.to_dict(orient='records')

        return jsonify({'filename': filename, 'property_count': len(properties), 'properties': properties_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
