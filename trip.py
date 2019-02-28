class trips(object):
    
    def __init__(self, filename):
        self._filename = filename
        self.load()
    
    def load(self):
        with open(self._filename, 'rt') as f:
            d = f.read()
            lines = d.split('\n')
        fields = lines[0].split(',')
        self._trips = {}
        for l in lines[1:]:
            if l:
                record = l.split(',')
                t = trip(fields, record)
                self._trips[t.trip_id] = t
    
    @property
    def trips(self):
        return self._trips
            
        
class trip(object):
    
    def __init__(self, fields, record):
        self._fields = fields
        self._record = record
        self.load()
    
    def load(self):
        self._values = {}
        for i in range(len(self._record)):
            value = self._record[i]
            field = self._fields[i]
            self.__dict__[field] = value
            self._values[field] = value

    def __repr__(self):
        return self.trip_id + ' - ' + self.route_id
    
    def __str__(self):
        return self.trip_id + ' - ' + self.route_id