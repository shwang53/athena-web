# -*- coding: utf-8 -*-

import time
import os
import sys
import json
import pprint
import s2sphere
import geopy.distance

from athena.common.name import Name

def latlon_to_cellID(latlng, length):
    lat, lng = latlng
    cell_id = s2sphere.CellId.from_lat_lng(s2sphere.LatLng.from_degrees(lat, lng))
    token = []
    for i in range(30):
        token.append(cell_id.to_token())
        cell_id = cell_id.parent()

    token = token[::-1] 
    token = token[:length]
    return '/'+'/'.join(token)


if __name__ == "__main__":        

    with open('route_from_client.json', 'r') as f:
        routes = json.load(f)

    with open('/home/jdlee/works/athena-framework/applications/sa-demo/prefix.json', 'r') as f:
        prefix = json.load(f)
        
    route_coordinates = dict()
    route_names = dict()
    for route_name, route in routes.items():
        points = route['overview_path']
        new_points = []
        new_names = []        
        for point in points:            
            new_point = [point['lat'], point['lng']]
            if new_points:
                dist = geopy.distance.vincenty(new_points[-1], new_point).m
                extra_points_num = int(dist / 50)                
                # extra_points_num = 0
                prev_point = new_points[-1]
                lan_pad = (prev_point[0] - new_point[0]) / (extra_points_num+1)
                lng_pad = (prev_point[1] - new_point[1]) / (extra_points_num+1)

                for i in range(extra_points_num):                    
                    extra_point = (new_point[0]+lan_pad*(i+1), new_point[1]+lng_pad*(i+1))
                    # print("%sth extra point between %s and %s is %s" % (i+1, prev_point, new_point, extra_point))
                    temp_name = "/image"+latlon_to_cellID(extra_point, 17)
                    for k, v in prefix.items():
                        if Name(temp_name).is_prefix_of(Name(k)):
                            new_points.append(extra_point)                
                            new_names.append(temp_name)

            temp_name = "/image"+latlon_to_cellID(new_point, 17)
            for k, v in prefix.items():
                if Name(temp_name).is_prefix_of(Name(k)):                        
                    new_points.append(new_point)                
                    new_names.append(temp_name)
        
        compressed_points = []
        compressed_names = []
        for i in range(len(new_points)):
            if i % 5 == 0:
                compressed_points.append(new_points[i])
                compressed_names.append(new_names[i])

        route_coordinates[route_name] = compressed_points
        route_names[route_name] = compressed_names   

        blue_bridge = [50.08956, 14.41267]
        route_coordinates['blue'].append(blue_bridge)
        route_names['blue'].append("/image"+latlon_to_cellID(blue_bridge, 17))

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/route_coordinates.json", "w", encoding='utf8') as f:
        json.dump(route_coordinates, f, indent=4, ensure_ascii=False)

    with open(os.getenv("HOME")+"/works/athena-web/public/rr/route_names.json", "w", encoding='utf8') as f:
        json.dump(route_names, f, indent=4, ensure_ascii=False)