# gps_nav.py

from __future__ import with_statement

import time
import math
import contextlib
import gps

# lat long long_radius north east angle_true angle_magnetic
Output_filename = '/tmp/gps_direction.out'

Earth_radius = 6371000

def run(target_lat, target_long, variation):
    r'''

    variation > 0 for W, < 0 for E.
    '''

    # Radius of the circle of longitude at the target latitude.
    long_radius = Earth_radius * math.cos(math.radians(target_lat))
    #print "long_radius", long_radius

    with contextlib.nested(contextlib.closing(gps.gps()),
                           contextlib.closing(open(Output_filename, 'wt', 1))) \
      as (session, outfile):

        while True:
            session.query('o')

            lat = session.fix.latitude
            long = session.fix.longitude
            #print 'lat', lat, 'long', long

            north, east, angle_true, angle_magnetic = \
              calc_angle(target_lat, target_long, variation, long_radius,
                         lat, long)

            #print 'north', north
            #print 'east', east
            #print 'angle, true', angle_true
            #print 'angle, magnetic', angle_magnetic

            print >> outfile, lat, long, long_radius, \
                              north, east, angle_true, angle_magnetic

            time.sleep(1)

def calc_angle(target_lat, target_long, variation, long_radius, lat, long):
    # distance in meters north to target (< 0 if target is south)
    north = Earth_radius * math.radians(target_lat - lat)

    # distance in meters east to target (< 0 if target is west)
    east = long_radius * math.radians(target_long - long)

    # True heading to target. -180 to 180
    angle_true = math.degrees(math.atan2(east, north))

    # Magnetic heading to target. -180 to 180
    angle_magnetic = angle_true + variation

    return north, east, angle_true, angle_magnetic