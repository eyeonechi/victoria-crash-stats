import victoria_crash_stats as py

pivot = 'Severity'

indexes = {
    'ACCIDENT_NO'           : 'Number',
    'ACCIDENTDATE'          : 'Date',
    'ACCIDENTTIME'          : 'Time',
    'ACCIDENT_TYPE'         : 'AccType',
    'Accident Type Desc'    : 'AccDesc',
    'DAY_OF_WEEK'           : 'Day',
    'Day Week Description'  : 'DayDesc',
    'DCA_CODE'              : 'DCA',
    'DCA Description'       : 'DCADesc',
    'DIRECTORY'             : 'Directory',
    'EDITION'               : 'Edition',
    'PAGE'                  : 'Page',
    'GRID_REFERENCE_X'      : 'GridX',
    'GRID_REFERENCE_Y'      : 'GridY',
    'LIGHT_CONDITION'       : 'Light',
    'Light Condition Desc'  : 'LightDesc',
    'NODE_ID'               : 'Node',
    'NO_OF_VEHICLES'        : 'NumVehicles',
    'NO_PERSONS'            : 'NumPersons',
    'NO_PERSONS_INJ_2'      : 'NumInjured2',
    'NO_PERSONS_INJ_3'      : 'NumInjured3',
    'NO_PERSONS_KILLED'     : 'NumKilled',
    'NO_PERSONS_NOT_INJ'    : 'NumHealthy',
    'POLICE_ATTEND'         : 'NumPolice',
    'ROAD_GEOMETRY'         : 'Geometry',
    'Road Geometry Desc'    : 'GeometryDesc',
    'SEVERITY'              : 'Severity',
    'SPEED_ZONE'            : 'Zone'}

def main():
    data = py.openData('datasets/accident_2016.csv')
    data = py.cleanData(data, 'Unnamed: 0')
    print(data[data.Date.apply(lambda x: '2016' in str(x).split('/')[2])])

if __name__ == '__main__':
    main()
