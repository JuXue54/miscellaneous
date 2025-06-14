import numpy as np

lat = 30.5539768004764778
lon = 104.05675167060852


def random_num(x, delta):
    return x + (np.random.rand() - 0.5) * delta * 2


def random_pos(latitude=lat, longitude=lon):
    return random_num(np.array([latitude, longitude]), 0.0005)


if __name__ == '__main__':
    x = random_pos()
    res = """<?xml version="1.0"?>
<gpx version="1.1" creator="Xcode">
    
    <!--
     Provide one or more waypoints containing a latitude/longitude pair. If you provide one
     waypoint, Xcode will simulate that specific location. If you provide multiple waypoints,
     Xcode will simulate a route visiting each waypoint.
     -->
    <wpt lat="%s" lon="%s">
        <name>Cupertino</name>
        
        <!--
         Optionally provide a time element for each waypoint. Xcode will interpolate movement
         at a rate of speed based on the time elapsed between each waypoint. If you do not provide
         a time element, then Xcode will use a fixed rate of speed.
         
         Waypoints must be sorted by time in ascending order.
         -->
        <time>2024-03-07T21:45:37Z</time>
    </wpt>
</gpx>
    """ % (x[0], x[1])
    path = '/Users/jon/Documents/appleProject/LocationChanger/LocationChanger/Location.gpx'
    with open(path, "w") as file:
        file.write(res)
    print(res)
