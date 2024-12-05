import requests
import json
from loguru import logger

siteNames = [
    "CHATTAHOOCHEE RIVER ABOVE ROSWELL, GA",
    "CHATTAHOOCHEE R 0.27 MI US WILLEO CR, ROSWELL, GA",
    "CHATTAHOOCHEE R 0.25 MI US WILLEO CR, ROSWELL, GA",
    "CHATTAHOOCHEE R .18 MI US WILLEO CR, ROSWELL, GA",
    "CHATTAHOOCHEE RIVER AT MORGAN FALLS DAM, GA",
    "CHATTAHOOCHEE RIVER BELOW MORGAN FALLS DAM, GA",
    "CHATTAHOOCHEE RIVER NEAR BUFORD, GA",
    "CHATTAHOOCHEE R 0.96 MI US MCGINNIS FY SUWANEE GA",
    "CHATTAHOOCHEE R 0.76 MI US MCGINNIS FY SUWANEE GA",
    "CHATTAHOOCHEE R 0.5 MI US MCGINNIS FY SUWANEE, GA",
    "CHATTAHOOCHEE RIVER NEAR NORCROSS, GA",
    "CHATTAHOOCHEE R 0.09 MI DS GA140, ALPHARETTA, GA",
    "CHATTAHOOCHEE R 0.39 MI DS GA140, ALPHARETTA, GA",
    "CHATTAHOOCHEE R 0.47 MI DS GA140, ALPHARETTA, GA"
]

desiredStats = {
    'Temperature, water, degrees Fahrenheit': 'waterTemp',
    'Temperature, water, degrees Celsius': 'waterTemp',
    'Gage height, feet': 'gageHeight',
    'Discharge, cubic feet per second': 'discharge',
    'Escherichia coli, estimated by regression equation, water, colonies per 100 milliliters': 'eColi',
    'Turbidity, water, unfiltered, monochrome near infra-red LED light, 780-900 nm, detection angle 90 +-2.5 degrees, formazin nephelometric units (FNU)': 'clarity',
    'Temperature, air, degrees Celsius': 'airTempC',
    'Wind speed, miles per hour': 'windSpeed',
    'Relative humidity, percent': 'humidity',
    'Precipitation, total, inches': 'precipitation'
}

recommendations = {
    'waterTemp': {'recommended': 'above 60°F', 'check': lambda x: float(x) > 60},
    'gageHeight': {'recommended': 'varies', 'check': lambda x: True},
    'discharge': {'recommended': 'below 5000 cfs', 'check': lambda x: float(x) < 5000},
    'eColi': {'recommended': 'below 235 colonies/100mL', 'check': lambda x: float(x) < 235},
    'clarity': {'recommended': 'low turbidity', 'check': lambda x: float(x) < 5},
    'airTempC': {'recommended': 'varies', 'check': lambda x: True},
    'windSpeed': {'recommended': 'below 15 mph', 'check': lambda x: float(x) < 15},
    'humidity': {'recommended': 'varies', 'check': lambda x: True},
    'precipitation': {'recommended': 'minimal recent rainfall', 'check': lambda x: float(x) == 0}
}

def celsiusToFahrenheit(celsius):
    return (celsius * 9/5) + 32

def extractSiteCodesByKeyword(data, keyword):
    siteCodes = set()
    for entry in data:
        siteName = entry.get("sourceInfo", {}).get("siteName")
        siteCode = entry.get("sourceInfo", {}).get("siteCode", [{}])[0].get("value")
        if keyword.lower() in siteName.lower() and siteCode:
            siteCodes.add(siteCode)
    return siteCodes

def extractSiteCodes(data, siteNames):
    siteCodes = set()
    for entry in data:
        siteName = entry.get("sourceInfo", {}).get("siteName")
        siteCode = entry.get("sourceInfo", {}).get("siteCode", [{}])[0].get("value")
        if siteName in siteNames and siteCode:
            siteCodes.add(siteCode)
    return siteCodes

def fetchUsgsFullData():
    params = {
        "format": "json",
        "indent": "on",
        "stateCd": "ga",
        "siteStatus": "active",
    }

    baseUrl = "https://waterservices.usgs.gov/nwis/iv/"
    response = requests.get(baseUrl, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def fetchUsgsData(siteCodes):
    params = {
        "format": "json",
        "sites": ",".join(list(siteCodes)),
        "indent": "on",
        "siteStatus": "active",
        "siteType": "ES,LK,ST"
    }

    baseUrl = "https://waterservices.usgs.gov/nwis/iv/"
    response = requests.get(baseUrl, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def extractParameters(data):
    extractedData = {}
    for series in data['value']['timeSeries']:
        siteName = series['sourceInfo']['siteName']
        latitude = series['sourceInfo']['geoLocation']['geogLocation']['latitude']
        longitude = series['sourceInfo']['geoLocation']['geogLocation']['longitude']
        variableName = series['variable']['variableDescription']
        values = series['values'][0]['value']

        if siteName not in extractedData:
            extractedData[siteName] = {
                'latitude': latitude,
                'longitude': longitude,
                'variables': {}
            }
        
        for valueEntry in values:
            value = valueEntry['value']
            dateTime = valueEntry['dateTime']
            if variableName in desiredStats:
                key = desiredStats[variableName]
                if variableName == 'Temperature, water, degrees Celsius':
                    value = celsiusToFahrenheit(float(value))
                    recommendations[key]['recommended'] = 'above 60°F'
                extractedData[siteName]['variables'][key] = {
                    'value': value,
                    'date': dateTime,
                    'passed': recommendations[key]['check'](value),
                    'recommended': recommendations[key]['recommended']
                }
    
    return extractedData

def processDataBySiteNames(data, siteNames):
    siteCodes = extractSiteCodes(data, siteNames)
    fetchedData = fetchUsgsData(siteCodes)
    return extractParameters(fetchedData)

def processDataByKeyword(data, keyword):
    siteCodes = extractSiteCodesByKeyword(data, keyword)
    fetchedData = fetchUsgsData(siteCodes)
    return extractParameters(fetchedData)

if __name__ == "__main__":
    logger.info("Fetching full USGS data...")
    jsonData = fetchUsgsFullData()

    keyword = "ROSWELL"
    logger.info(f"Processing data by keyword: {keyword}")
    finalData = processDataByKeyword(jsonData['value']['timeSeries'], keyword)
    logger.info("Final Extracted Data by Keyword:")
    print(json.dumps(finalData, indent=2))

    logger.info("Processing data by pre-populated site names...")
    finalData = processDataBySiteNames(jsonData['value']['timeSeries'], siteNames)
    logger.info("Final Extracted Data by Site Names Pre-Populated:")
    print(json.dumps(finalData, indent=2))
