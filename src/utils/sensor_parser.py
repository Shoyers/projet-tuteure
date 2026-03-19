import re
from typing import Dict, Optional


def parse_sensor_string(data_str: str) -> Dict[str, Optional[float]]:
    """
    Parse une chaîne de données capteurs et retourne un dictionnaire normalisé.
    
    Formats supportés:
    - Format standard: "AQ:800,DIST:2.5,LUM:800,TEMP:24.5,PRESS:1010,HUM:65"
    - Format Arduino: "Temperature = 24.97 *C", "Pression = 1012.39 hPa"
    - Format SI1145: "SI1145 - Visible: 262", "SI1145 - UV: 0.35", "SI1145 - IR: 348"
    - Format MQ135: "MQ135 - Air Quality: 8.94 ppm", "MQ135 - Valeur: 348"
    - Format BME680: "BME680 - Temperature: 25.65 *C"
    - Format HC-SR04: "HC_SR04 - Distance: 34 cm"
    - Format GPS: "GPS - Latitude: 48.856614"
    
    Returns:
        Dictionnaire avec clés normalisées: air_quality, distance, luminosity, 
        uv_index, ir_value, temperature, pressure, humidity, latitude, longitude, altitude
    """
    if not data_str:
        return {}
    
    result = {}
    
    # Format standard avec séparateurs (AQ:800,DIST:2.5,...)
    if ':' in data_str and ',' in data_str:
        pairs = data_str.strip().split(',')
        for pair in pairs:
            if ':' not in pair:
                continue
            key, value = pair.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            if not value:
                continue
                
            try:
                if key == 'AQ':
                    result['air_quality'] = float(value)
                elif key == 'DIST':
                    result['distance'] = float(value)
                elif key == 'LUM':
                    result['luminosity'] = int(float(value))
                elif key == 'UV':
                    result['uv_index'] = float(value)
                elif key == 'IR':
                    result['ir_value'] = int(float(value))
                elif key == 'TEMP':
                    result['temperature'] = float(value)
                elif key == 'HUM':
                    result['humidity'] = int(float(value))
                elif key == 'PRESS':
                    result['pressure'] = int(float(value))
                elif key == 'GAS':
                    result['gas'] = float(value)
                elif key == 'LAT':
                    result['latitude'] = float(value)
                elif key == 'LON':
                    result['longitude'] = float(value)
                elif key == 'ALT':
                    result['altitude'] = float(value)
            except (ValueError, TypeError):
                pass
    
    # Formats spécifiques Arduino/capteurs
    else:
        # BME680 - Temperature
        if 'BME680' in data_str and 'Temperature' in data_str:
            match = re.search(r'Temperature\s*[:=]\s*([\d.]+)', data_str)
            if match:
                result['temperature'] = float(match.group(1))
        
        # BME680 - Pression
        elif 'BME680' in data_str and 'Pression' in data_str:
            match = re.search(r'Pression\s*[:=]\s*([\d.]+)', data_str)
            if match:
                result['pressure'] = int(float(match.group(1)))
        
        # BME680 - Humidité
        elif 'BME680' in data_str and ('Humidité' in data_str or 'Humidite' in data_str):
            match = re.search(r'Humidit[ée]\s*[:=]\s*([\d.]+)', data_str)
            if match:
                result['humidity'] = int(float(match.group(1)))
        
        # BME680 - Gas
        elif 'BME680' in data_str and 'Gas' in data_str:
            match = re.search(r'Gas[:\s]+([\d.]+)', data_str)
            if match:
                result['gas'] = float(match.group(1))
        
        # SI1145 - Visible
        elif 'SI1145' in data_str and 'Visible' in data_str:
            match = re.search(r'Visible[:\s]+(\d+)', data_str)
            if match:
                result['luminosity'] = int(match.group(1))
        
        # SI1145 - UV
        elif 'SI1145' in data_str and 'UV' in data_str:
            match = re.search(r'UV[:\s]+([\d.]+)', data_str)
            if match:
                result['uv_index'] = float(match.group(1))
        
        # SI1145 - IR
        elif 'SI1145' in data_str and 'IR' in data_str:
            match = re.search(r'IR[:\s]+(\d+)', data_str)
            if match:
                result['ir_value'] = int(match.group(1))
        
        # MQ135 - Air Quality
        elif 'MQ135' in data_str and 'Air Quality' in data_str:
            match = re.search(r'Air Quality[:\s]+([\d.]+)', data_str)
            if match:
                result['air_quality'] = float(match.group(1))
        
        # MQ135 - Valeur (brut)
        elif 'MQ135' in data_str and 'Valeur' in data_str:
            match = re.search(r'Valeur[:\s]+(\d+)', data_str)
            if match:
                result['air_quality'] = float(match.group(1))
        
        # HC-SR04 / HC SR04 - Distance (avec ou sans underscore)
        elif ('HC_SR04' in data_str or 'HC SR04' in data_str) and 'Distance' in data_str:
            match = re.search(r'Distance[:\s]+([\d.]+)', data_str)
            if match:
                # Convertir cm en m
                result['distance'] = float(match.group(1)) / 100.0
        
        # GPS - Latitude
        elif 'GPS' in data_str and 'Latitude' in data_str:
            match = re.search(r'Latitude[:\s]+([-\d.]+)', data_str)
            if match:
                result['latitude'] = float(match.group(1))
        
        # GPS - Longitude
        elif 'GPS' in data_str and 'Longitude' in data_str:
            match = re.search(r'Longitude[:\s]+([-\d.]+)', data_str)
            if match:
                result['longitude'] = float(match.group(1))
        
        # GPS - Altitude
        elif 'GPS' in data_str and 'Altitude' in data_str:
            match = re.search(r'Altitude[:\s]+([-\d.]+)', data_str)
            if match:
                result['altitude'] = float(match.group(1))
        
        # Formats génériques (fallback)
        elif 'Temperature' in data_str and '=' in data_str:
            match = re.search(r'Temperature\s*[:=]\s*([\d.]+)', data_str)
            if match:
                result['temperature'] = float(match.group(1))
        
        elif 'Pression' in data_str and '=' in data_str:
            match = re.search(r'Pression\s*[:=]\s*([\d.]+)', data_str)
            if match:
                result['pressure'] = int(float(match.group(1)))
        
        elif ('Humidité' in data_str or 'Humidite' in data_str) and '=' in data_str:
            match = re.search(r'Humidit[ée]\s*[:=]\s*([\d.]+)', data_str)
            if match:
                result['humidity'] = int(float(match.group(1)))
    
    return result


def normalize_sensor_dict(data: Dict) -> Dict:
    """
    Normalise un dictionnaire de capteurs avec différents formats de clés
    vers un format unifié.
    
    Supporte les alias: airQuality/air_quality/AQ/co2, uvIndex/uv_index/UV, etc.
    
    Returns:
        Dictionnaire avec clés normalisées
    """
    if not data or not isinstance(data, dict):
        return {}
    
    normalized = {}
    
    # Mapping des clés possibles vers clés normalisées
    key_mappings = {
        'air_quality': ['air_quality', 'airQuality', 'AQ', 'co2'],
        'distance': ['distance', 'dist', 'DIST'],
        'luminosity': ['luminosity', 'lum', 'LUM'],
        'uv_index': ['uv_index', 'uvIndex', 'UV'],
        'ir_value': ['ir_value', 'irValue', 'IR'],
        'temperature': ['temperature', 'temp', 'TEMP'],
        'pressure': ['pressure', 'press', 'PRESS'],
        'humidity': ['humidity', 'hum', 'HUM'],
        'gas': ['gas', 'Gas', 'GAS'],
        'latitude': ['latitude', 'lat', 'LAT'],
        'longitude': ['longitude', 'lon', 'lng', 'LONG'],
        'altitude': ['altitude', 'alt', 'ALT'],
        'timestamp': ['timestamp', 'time', 'date'],
        'raw_data': ['raw_data', 'rawData', 'raw']
    }
    
    # Chercher chaque clé normalisée
    for normalized_key, possible_keys in key_mappings.items():
        for key in possible_keys:
            if key in data and data[key] is not None:
                # Convertir 'N/A' en None
                if data[key] == 'N/A':
                    normalized[normalized_key] = None
                else:
                    normalized[normalized_key] = data[key]
                break
    
    return normalized
