class stops(object):
    
    def __init__(self, filename):
        self._filename = filename
        self.load()
    
    def load(self):
        with open(self._filename, 'rt') as f:
            d = f.read()
            lines = d.split('\n')
        fields = lines[0].split(',')
        self._stops = {}
        for l in lines[1:]:
            if l:
                record = l.split(',')
                s = stop(fields, record)
                self._stops[s.stop_id] = s
    
    @property
    def stops(self):
        return self._stops
            
        
class stop(object):
    
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