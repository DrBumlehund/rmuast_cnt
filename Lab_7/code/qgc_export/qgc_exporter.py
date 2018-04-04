#
#  Copyright 2018 Chris Bang Sørensen, Niels Hvid, Thomas Lemqvist
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#  of the Software, and to permit persons to whom the Software is furnished to do so,
#  subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
#  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json


class qgc:
    def __init__(self):
        self.__version = 1
        self.__plan = {'fileType': 'Plan', 'version': self.__version, 'groundStation': 'QGroundControl'}

    def __create_mission(self, route_data):
        mission = {}
        items = []
        jumpId = 0
        for i in route_data:
            jumpId += 1
            item = {}
            item['autoContinue'] = True
            item['command'] = 16
            if jumpId == 1:
                item['command'] = 22  # takeoff
            elif jumpId == len(route_data):
                item['command'] = 21  # land
            item['doJumpId'] = jumpId
            item['frame'] = 3
            item['params'] = [0, 0, 0, 0, i['lat'], i['lon'], i['alt']]
            item['type'] = 'SimpleItem'
            items.append(item)
        mission['cruiseSpeed'] = 15
        mission['firmwareType'] = 3
        mission['hoverSpeed'] = 5
        mission['items'] = items
        mission['plannedHomePosition'] = [route_data[0]['lat'], route_data[0]['lon'], route_data[0]['alt']]
        mission['vehicleType'] = 2
        mission['version'] = self.__version
        self.__plan['mission'] = mission

    def __create_rally_points(self, rally_point_data):
        rally_points = {}
        points = []
        for i in rally_point_data:
            point = [i['lat'], i['lon'], i['alt']]
            points.append(point)
        rally_points['points'] = points
        rally_points['version'] = self.__version
        self.__plan['rallyPoints'] = rally_points

    def __create_geo_fence(self, geo_fence_parameters, geo_fence_data):
        geo_fence = {}
        parameters = []
        for i in geo_fence_parameters:
            parameter = {'compId': i['compId'], 'name': i['name'], 'value': i['value']}
            parameters.append(parameter)
        geo_fence['parameters'] = parameters
        points = []
        for i in geo_fence_data:
            point = [i['lat'], i['lon']]
            points.append(point)
        geo_fence['polygon'] = points
        geo_fence['version'] = self.__version
        self.__plan['geoFence'] = geo_fence

    @staticmethod
    def __check_file_name(file_name):
        if str(file_name).lower().split('.')[-1] != 'plan':
            file_name += '.plan'
        return file_name

    def __write_file(self, file_name):
        f_name = self.__check_file_name(file_name)
        plan_json = json.dumps(self.__plan, indent=4, sort_keys=True)
        file = open(f_name, 'w')
        file.write(plan_json)
        file.close()

    def export(self, route_data, file_name='route.plan', geo_fence_parameters=None, geo_fence_data=None,
               rally_points=None):

        if geo_fence_parameters is None:
            geo_fence_parameters = []
        if geo_fence_data is None:
            geo_fence_data = []
        if rally_points is None:
            rally_points = []

        self.__create_geo_fence(geo_fence_parameters, geo_fence_data)
        self.__create_mission(route_data)
        self.__create_rally_points(rally_points)

        self.__write_file(file_name)
