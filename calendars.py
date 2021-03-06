from dateutils import parse_date

class calendars(object):
    
    def __init__(self, filename):
        self._filename = filename
        self.load()
    
    def load(self):
        with open(self._filename, 'rt') as f:
            d = f.read()
            lines = d.split('\n')
        fields = lines[0].split(',')
        self._calendars = {}
        for l in lines[1:]:
            if l:
                record = l.split(',')
                c = calendar(fields, record)
                self._calendars[c.service_id] = c
    
    @property
    def calendars(self):
        return self._calendars
            
        
class calendar(object):
    
    DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
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
        self.start_date = parse_date(self.start_date)
        self.end_date = parse_date(self.end_date)
        self.week = {}
        for d in calendar.DAYS:
            val = getattr(self, d) == '1'
            setattr(self, d, val)
            self.week[d] = val 
        

    def __repr__(self):
        result = ''
        for f in self._fields:
            result += f + ':' + str(getattr(self, f)) + ', '
        return result[:-2]
    
    def __str__(self):
        result = ''
        for f in self._fields:
            result += f + ':' + str(getattr(self, f)) + ', '
        return result[:-2]