from models import Calculations, Fips_Codes

def lookup_district(response):
# create list to store district information in
    district = []
    geoid = None
    state = None

    # get the values from name keys under divisions in JSON
    for division in response['divisions'].items():
        for name in division[1].items():
            if len(name[1][0]) == 1:
                district.append(name[1])
            else:
                district.append(name[1][0])
    
    # remove items containing 'ocd-division/country:us/state:' from list
    district = [i for i in district if 'ocd-division/country:us/state:' not in i]
    
    # remove "United States" from list and sort so [0] is state and [1] is full congressional district
    district.remove('United States')
    district.sort()
    
    # if no district, append with 'at-large congressional district'
    if len(district) == 1:
       district.append(district[0] + '\'s at-large congressional district')

    # get fips code
    fips_code = Fips_Codes.query.filter_by(state=district[0]).first().fips_code
    district.append(fips_code)
    
    # get whether or not state is an at-large district
    at_large = Fips_Codes.query.filter_by(state=district[0]).first().at_large
    
    # determine GEOID
    if at_large == False:
        district_number = int(''.join(list(filter(str.isdigit, district[1]))))
        if district_number < 10:
            district_number = '0' + str(district_number)
        else:
            district_number = str(district_number)
    else:
        district_number = '00'
    geoid = fips_code + district_number
    district.append(geoid)
    
    # get Polsby-Popper Score
    polsby_popper = Calculations.query.filter_by(geoid=district[3]).first().polsby_popper_score
    if polsby_popper:
        district.append(polsby_popper)
    else:
        district.append('0')
    
    # get intpt_lat
    intpt_lat = Calculations.query.filter_by(geoid=district[3]).first().intpt_lat
    if intpt_lat:
        district.append(intpt_lat)
    else:
        district.append('0')
    
    # get intpt_lon
    intpt_lon = Calculations.query.filter_by(geoid=district[3]).first().intpt_lon
    if intpt_lon:
        district.append(intpt_lon)
    else:
        district.append('0')
        
    # if Polsby-Popper score is less than 14, the district is gerrymandered
    if polsby_popper < 14:
        district.append(['Your district is likely gerrymandered!', 'text-danger'])
    else:
        district.append(['Your district is likely not gerrymandered!', 'text-success'])
    
    # district should contain state, full district name, district (number), GeoID, Polsby-Popper Score, INTLAT, INTLONG, gerrymandered message/class
    return {
        'state': district[0],
        'full district name': district[1],
        'district': district[2],
        'geoid': district[3],
        'polsy_popper': district[4],
        'intpt_lat': district[5],
        'intpt_lon': district[6],
        'gerrymandered': district[7]
    }