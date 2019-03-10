TYPE_TRAM = '0'
TYPE_METRO = '1'
TYPE_TRAIN = '2'
TYPE_BUS = '3'
TYPE_FERRY = '4'
TYPE_CABLETRAM = '5'
TYPE_AERIAL = '6'
TYPE_FENICULAR = '7'

route_type = {}
route_type[TYPE_TRAM] = 'Tram'
route_type[TYPE_METRO] = 'Metro'
route_type[TYPE_TRAIN] = 'Train'
route_type[TYPE_BUS] = 'Bus'
route_type[TYPE_FERRY] = 'Ferry'
route_type[TYPE_CABLETRAM] = 'Cable tram'
route_type[TYPE_AERIAL] = 'Aerial lift'
route_type[TYPE_FENICULAR] = 'Funicular'

class routes(object):
    
    def __init__(self, filename):
        self._filename = filename
        self.load()
    
    def load(self):
        with open(self._filename, 'rt') as f:
            d = f.read()
            lines = d.split('\n')
        fields = lines[0].split(',')
        self._routes = {}
        for l in lines[1:]:
            if l:
                record = l.split(',')
                r = route(fields, record)
                self._routes[r.route_id] = r
    
    @property
    def routes(self):
        return self._routes

class route(object):
    
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
        result = ''
        for f in self._fields:
            result += f + ':' + getattr(self, f) + ', '
        return result[:-2]
    
    def __str__(self):
        result = ''
        for f in self._fields:
            result += f + ':' + getattr(self, f) + ', '
        return result[:-2]