class agencies(object):
    
    def __init__(self, filename):
        self._filename = filename
        self.load()
    
    def load(self):
        with open(self._filename, 'rt') as f:
            d = f.read()
            lines = d.split('\n')
        fields = lines[0].split(',')
        self._agencies = {}
        for l in lines[1:]:
            if l:
                record = l.split(',')
                a = agency(fields, record)
                self._agencies[a.agency_id] = a
    
    @property
    def agencies(self):
        return self._agencies
            
        
class agency(object):
    
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
        return self.agency_id + ' - ' + self.agency_name
    
    def __str__(self):
        return self.agency_id + ' - ' + self.agency_name