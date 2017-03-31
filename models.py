from app import db

# create database model
class Calculations(db.Model):
    __tablename__ = 'calculations'
    area = db.Column(db.Float)
    perimeter = db.Column(db.Float)
    polsby_popper_score = db.Column(db.Float)
    geoid = db.Column(db.String(6), primary_key=True)
    name_lsad = db.Column(db.String(120))
    lsad = db.Column(db.String(4))
    congressional_session = db.Column(db.Integer)
    intpt_lat = db.Column(db.Float)
    intpt_lon = db.Column(db.Float)

    def __init__(self, area, perimeter, polsby_popper_score, geoid, name_lsad, lsad, congressional_session, intpt_lat, intpt_lon):
        self.area = area
        self.perimeter = perimeter
        self.polsby_popper_score = polsby_popper_score
        self.geoid = geoid
        self.name_lsad = name_lsad
        self.lsad = lsad
        self.congressional_session = congressional_session
        self.intpt_lat = intpt_lat
        self.intpt_lon = intpt_lon

    def __repr__(self):
        return "<Calculations(area='%s', perimeter='%s', polsby_popper_score='%s', geoid='%s', name_lsad='%s', lsad='%s', congressional_session='%s', intpt_lat='%s', intpt_lon='%s')>" % (self.area, self.perimeter, self.polsby_popper_score, self.geoid, self.name_lsad, self.lsad, self.congressional_session, self.intpt_lat, self.intpt_lon)

class Fips_Codes(db.Model):
    __tablename__ = 'fips_codes'
    fips_code = db.Column(db.String(4), primary_key=True)
    state = db.Column(db.String(30))
    st = db.Column(db.String(4))
    at_large = db.Column(db.Boolean)

    def __init__(self, fips_code, state, st, at_large):
        self.fips_code = fips_code
        self.state = state
        self.st = st
        self.at_large = at_large

    def __repr__(self):
        return "<Fips_Codes(fips_code='%s', state='%s', st='%s', at_large='%s')>" % (self.fips_code, self.state, self.st, self.at_large)