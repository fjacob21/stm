from dateutils import split_time

class stop_times(object):
    
    def __init__(self, filename):
        self._filename = filename
        self.load()
    
    def load(self):
        with open(self._filename, 'rt') as f:
            d = f.read()
            lines = d.split('\n')
        fields = lines[0].split(',')
        self._stop_times = {}
        for l in lines[1:]:
            if l:
                record = l.split(',')
                st = stop_time(fields, record)
                if st.trip_id not in self._stop_times:
                    self._stop_times[st.trip_id] = []
                self._stop_times[st.trip_id].append(st)
        for st in self._stop_times:
            self._stop_times[st] = sorted(self._stop_times[st], key=lambda k: k.stop_sequence)
    
    def get_stop(self, trip_id, sequence):
        if trip_id not in self._stop_times:
            return None
        st = self._stop_times[trip_id]
        for s in st:
            if int(s.stop_sequence) == sequence:
                return s
        return None

    @property
    def stop_times(self):
        return self._stop_times
            
        
class stop_time(object):
    
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
        self.arrival_time = split_time(self.arrival_time)
        self.departure_time	= split_time(self.departure_time)
        self.stop_sequence	= int(self.stop_sequence)

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