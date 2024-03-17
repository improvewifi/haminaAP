



import json
import pandas as pd
from datetime import datetime

# Regularly used conversions first work is input and second is output
def imperialMetric(val) -> float:
    return val*.3048

def metricImperial(val) -> float:
    return val/.3048

def imperialFormatted(val) -> str:
    return str(int(val)) + 'ft ' + str(int(val %1 * 12)) + 'in'

def apLocation(zeroPoint: float, apCoordinate: float) -> str: #Only one coordinate at a time
    return apCoordinate - zeroPoint
    
#Manipulation of Data copied out of Hamina
def haminaData(units,copiedData) -> list:
    haminaData = json.loads(copiedData)
    #Set Logical Zero Point
    measurementSystem = 'metric'
    zeroPointX, zeroPointY = 0,0
    data = [] # for manipulated data
    if 'mapNotes' in haminaData.keys():
        for notes in haminaData['mapNotes']:
            if 'zero point' in notes['text'].lower():
                zeroPointX = notes['x']
                zeroPointY = notes['y']
                if 'feet' in notes['text'].lower() or 'imperial' in notes['text'].lower() or 'ft' in notes['text'].lower() or units == 'imperial':
                    measurementSystem = 'imperial'
                if 'setxy=' in notes['text'].lower():
                    tempList = notes['text'].lower().split(' ')
                    for temp in tempList:
                        if 'setxy=' in temp:
                            tem = temp.strip('setxy=')
                            temList = tem.split(':')
                            if len(temList) == 2:
                                zeroPointX = float(temList[0])
                                zeroPointY = float(temList[1])
                                if measurementSystem == 'imperial':
                                    zeroPointX = imperialMetric(zeroPointX)
                                    zeroPointY = imperialMetric(zeroPointY)
                if 'setxy=' not in notes['text'].lower():
                        if measuringSystem == 'metric':
                            notes['text'] = notes['text'] + ' setXY=' + str(zeroPointX) + ':' + str(zeroPointY) + ' setXY in meters'
                        else:
                            notes['text'] = notes['text'] + ' setXY=' + str(metricImperial(zeroPointX)) + ':' + str(metricImperial(zeroPointY)) + ' setXY is in feet'
                break
    #Loop through APs and add X & Y coordinates to names. Return manipulated data and measures for reporting
    for aps in haminaData['accessPoints']:
        tempY = apLocation(zeroPointY, aps['y'])
        tempY = tempY * (-1)
        if measurementSystem == 'imperial':
            logicalX = imperialFormatted(metricImperial(apLocation(zeroPointX, aps['x'])))
            logicalY = imperialFormatted(metricImperial(tempY))
            logicalZ = imperialFormatted(metricImperial(aps['installHeight']))
        else:
            logicalX = '%.3f'%(str(apLocation(zeroPointX, aps['x']))) + ' m'
            logicalY = '%.3f'%(str(tempY)) + ' m'
            logicalZ = '%.3f'%(aps['installHeight'])
        absoluteZeroX, absoluteZeroY, absoluteZeroZ = aps['x'], aps['y'], aps['installHeight']
        apName = aps['name']+ ' X:'+ str(logicalX) +' Y:'+ str(logicalY)
        aps['name'] = apName
        data.append([aps, {'logicalX': logicalX, 'logicalY': logicalY, 'logicalZ': logicalZ, 'absoluteZeroX': absoluteZeroX, 'absoluteZeroY': absoluteZeroY, 'absoluteZeroZ': absoluteZeroZ}])

    for aps in haminaData['accessPoints']:
        for ap in data:
            if aps['x'] == ap[1]['absoluteZeroX'] and aps['y'] == ap[1]['absoluteZeroY'] and aps['installHeight'] == ap[1]['absoluteZeroZ']:
                aps['name'] = ap[0]['name']

    #Generate Files
    fileName = delivery(haminaData, data)
    return fileName

#Export data to CSV file to be used as check list
def delivery(haminaData, data) -> str:
    results = []
    for aps in haminaData['accessPoints']:
        for ap in data:
            if ap[1]['absoluteZeroX'] == aps['x'] and ap[1]['absoluteZeroY'] == aps['y'] and ap[1]['absoluteZeroZ'] ==aps['installHeight']:
                results.append({'AP Name': ap[0]['name'],'X':ap[1]['logicalX'], 'Y': ap[1]['logicalY'], 'Install Height': ap[1]['logicalZ'], 'Make & Model': (ap[0]['make'] + ' ' + ap[0]['model']), 'Antenna': (str(ap[0]['externalAntennaMake']) + ' ' + str(ap[0]['externalAntennaModel'])), 'Mount': ap[0]['mount'], 'Elevation tilt': str(ap[0]['elevation']), 'Azimuth': str(ap[0]['azimuth'])})
    df = pd.DataFrame(results)
    fileName = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    df.to_csv('/home/walrus/env/hamina/uploads/' + fileName + '.csv', index=False) 
    with open('/home/walrus/env/hamina/uploads/' + fileName + '.txt', 'w') as f:
        hamina =  json.dumps(haminaData, indent=2)
        f.write(hamina)
    return fileName
