from google.transit import gtfs_realtime_pb2
from agency import agencies
from route import routes
from trip import trips
from stop import stops
from stop_time import stop_times
from calendars import calendars
from calendar_date import calendar_dates
from fare_attribute import fare_attributes
from fare_rule import fare_rules
from frequencie import frequencies
from shapes import shapes
from dateutils import build_datetime
import requests
import datetime
import geopy.distance
import os
import requests
import zipfile
import tempfile
import time

class stm(object):
    
    def __init__(self):
        self._download_data()
        self.load()
            
    def _download_data(self):
        if not os.path.exists('./stmdata'):
            start = time.time()
            print('-->Download data')
            r = requests.get('http://www.stm.info/sites/default/files/gtfs/gtfs_stm.zip')
            fi = os.path.join(tempfile.gettempdir(), 'stm.zip')
            open(fi, 'wb').write(r.content)
            zip_ref = zipfile.ZipFile(fi, 'r')
            zip_ref.extractall('./stmdata')
            zip_ref.close()
            end = time.time()
            print('<--Download data', end-start)

    def load(self):
        start = time.time()
        print('-->Load data')
        self._agencies = agencies('./stmdata/agency.txt')
        self._routes = routes('./stmdata/routes.txt')
        self._trips = trips('./stmdata/trips.txt')
        self._stops = stops('./stmdata/stops.txt')
        self._stop_times = stop_times('./stmdata/stop_times.txt')
        self._calendars = calendars('./stmdata/calendar.txt')
        self._calendar_dates = calendar_dates('./stmdata/calendar_dates.txt')
        self._fare_attributes = fare_attributes('./stmdata/fare_attributes.txt')
        self._fare_rules = fare_rules('./stmdata/fare_rules.txt')
        self._frequencies = frequencies('./stmdata/frequencies.txt')
        self._shapes = shapes('./stmdata/shapes.txt')
        self._build_trips()
        self._build_routes()
        self._sort_routes()
        end = time.time()
        print('<--Load data', end-start)
    
    def _build_trips(self):
        start = time.time()
        print('-->Build trips')
        self._trips_build = {}
        for trip_id in self._trips.trips:
            trip = self._trips.trips[trip_id]
            calendar = self._calendars.calendars[trip.service_id]
            if datetime.date.today() < calendar.end_date:
                trip_info = {'trip': trip, 'stops':[]}
                stop_times = self._stop_times.stop_times[trip.trip_id]
                stops = []
                for stop_time in stop_times:
                    stops.append({'stop_time': stop_time, 'stop':self._stops.stops[stop_time.stop_id]})
                stops = sorted(stops , key=lambda k: k['stop_time'].departure_time)
                trip_info['stops'] = stops
                self._trips_build[trip_id] = trip_info
        end = time.time()
        print('<--Build trips', end-start)

    def _build_routes(self):
        start = time.time()
        print('-->Build routes')
        self._routes_build = {}
        for trip_id in self._trips.trips:
            trip = self._trips.trips[trip_id]
            calendar = self._calendars.calendars[trip.service_id]
            if datetime.date.today() < calendar.end_date:
                if trip.route_id not in self._routes_build:
                    self._routes_build[trip.route_id] = {'id': trip.route_id, 'inbound': {'week':[], 'weekend':[]}, 'outbound': {'week':[], 'weekend':[]}}
                route = self._routes_build[trip.route_id]
                stop_times = self._stop_times.stop_times[trip.trip_id]
                route_stop_times = []
                for stop_time in stop_times:
                    route_stop_times.append({'stop_time': stop_time, 'stop':self._stops.stops[stop_time.stop_id]})
                trip_build = {'id': trip_id, 'stops': route_stop_times}
                if trip.direction_id == '0':
                    if calendar.monday:
                        route['outbound']['week'].append(trip_build)
                    else:
                        route['outbound']['weekend'].append(trip_build)
                else:
                    if calendar.monday:
                        route['inbound']['week'].append(trip_build)
                    else:
                        route['inbound']['weekend'].append(trip_build)
        end = time.time()
        print('<--Build routes', end-start)

    def _sort_routes(self):
        start = time.time()
        print('-->Sort routes')
        for route_id in self._routes_build:
            route = self._routes_build[route_id]
            route['inbound']['week'] = sorted(route['inbound']['week'] , key=lambda k: k['stops'][0]['stop_time'].departure_time)
            route['inbound']['weekend']  = sorted(route['inbound']['weekend'] , key=lambda k: k['stops'][0]['stop_time'].departure_time)
            route['outbound']['week']  = sorted(route['outbound']['week'] , key=lambda k: k['stops'][0]['stop_time'].departure_time)
            route['outbound']['weekend']  = sorted(route['outbound']['weekend'] , key=lambda k: k['stops'][0]['stop_time'].departure_time)
        end = time.time()
        print('<--Sort routes', end-start)
    
    @property
    def agency(self):
        return self._agencies.agencies.agencies[0]
    
    @property
    def routes(self):
        return self._routes_build
    
    def get_current_schedule(self, route_id, is_inbound):
        route = self._routes_build[route_id]
        is_week = datetime.date.today().weekday() in [0, 1 , 2, 3, 4]
        if is_inbound:
            direction = route['inbound']
        else:
            direction = route['outbound']
        if is_week:
            trips = direction['week']
        else:
            trips = direction['weekend']
        n = datetime.datetime.now()
        currents = []
        for trip in trips:
            start_trip = trip['stops'][0]['stop_time'].departure_time
            start = build_datetime(n.year, n.month, n.day, start_trip[0], start_trip[1], start_trip[2])
            end_trip = trip['stops'][-1]['stop_time'].departure_time
            end = build_datetime(n.year, n.month, n.day, end_trip[0], end_trip[1], end_trip[2])
            if n > start and end > n:
                currents.append(trip)
        return currents
    
    def get_today_schedule(self, route_id, is_inbound):
        route = self._routes_build[route_id]
        is_week = datetime.date.today().weekday() in [0, 1 , 2, 3, 4]
        if is_inbound:
            direction = route['inbound']
        else:
            direction = route['outbound']
        if is_week:
            trips = direction['week']
        else:
            trips = direction['weekend']
        return trips
    
    @property
    def trips(self):
        return self._trips_build

    @property
    def stops(self):
        return self._stops.stops
    
    @property
    def stop_times(self):
        return self._stop_times.stop_times
    
    def get_stop(self, trip_id, sequence):
        return self._stop_times.get_stop(trip_id, sequence)
        
    
    
    
    
    