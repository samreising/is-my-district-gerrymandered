from models import Calculations, Fips_Codes

class District:

    def __init__(self):
        self.__district_list = []

        self.response = None
        self.state = None
        self.congressional_district = None
        self.geoid = None
        self.intpt_lat = None
        self.intpt_lon = None
        self.message = None
        self.message_class = None
        self.__fips_code = None
        self.__at_large = None
        self.__polsby_popper = None

    def lookup_district(self):
        self.__set_name_key_values()
        self.__remove_string_items('ocd-division/country:us/state:')
        self.__clean_up()
        self.__append_with_string('\'s at-large congressional district')
        self.__set_state()
        self.__set_congressional_district()
        self.__set_fips_code()
        self.__set_at_large()
        self.__set_geoid()
        self.__set_polsby_popper_score()
        self.__set_intpt_lat()
        self.__set_intpt_lon()
        self.__set_message_and_message_class()

    # get the values from name keys under divisions in JSON; district_list.[0] = state; district_list.[1] = congressional district
    def __set_name_key_values(self):
        self.__district_list = []
        for division in self.response['divisions'].items():
            for name in division[1].items():
                if len(name[1][0]) == 1:
                    self.__district_list.append(name[1])
                else:
                    self.__district_list.append(name[1][0])

    # remove items containing a string from list, remove 'United States', sort
    def __remove_string_items(self, string):
        self.__district_list = [x for x in self.__district_list if string not in x]

    # remove "United States" from list and sort so [0] is state and [1] is full congressional district
    def __clean_up(self):
        self.__district_list.remove('United States')
        self.__district_list.sort()

    # if no district, append with 'at-large congressional district'
    def __append_with_string(self, string):
        if len(self.__district_list) == 1:
            self.__district_list.append(self.__district_list[0] + string)

    # set state
    def __set_state(self):
        self.state = self.__district_list[0]

    # set congressional district
    def __set_congressional_district(self):
        self.congressional_district = self.__district_list[1]

    # set fips code
    def __set_fips_code(self):
        self.__fips_code = Fips_Codes.query.filter_by(state=self.state).first().fips_code
        self.__district_list.append(self.__fips_code)

    # set whether or not state is an at-large district
    def __set_at_large(self):
        self.__at_large = Fips_Codes.query.filter_by(state=self.state).first().at_large

    # set GEOID
    def __set_geoid(self):
        if self.__at_large == False:
            district_number = int(''.join(list(filter(str.isdigit, self.congressional_district))))
            if district_number < 10:
                district_number = '0' + str(district_number)
            else:
                district_number = str(district_number)
        else:
            district_number = '00'
        self.geoid = self.__fips_code + district_number

    # set Polsby-Popper Score
    def __set_polsby_popper_score(self):
        self.__polsby_popper = Calculations.query.filter_by(geoid=self.geoid).first().polsby_popper_score

    # set intpt_lat
    def __set_intpt_lat(self):
        self.intpt_lat = Calculations.query.filter_by(geoid=self.geoid).first().intpt_lat

    # set intpt_lon
    def __set_intpt_lon(self):
        self.intpt_lon = Calculations.query.filter_by(geoid=self.geoid).first().intpt_lon

    # if Polsby-Popper score is less than 14, the district is gerrymandered
    def __set_message_and_message_class(self):
        if self.__polsby_popper < 14:
            self.message = 'Your district is likely gerrymandered!'
            self.message_class = 'text-danger'
        else:
            self.message = 'Your district is likely not gerrymandered!'
            self.message_class = 'text-success'