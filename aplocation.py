import json, os
from datetime import datetime

class hamina:
    def __init__(self, copiedData: str, measuringSystem: str ='metric', measuringSystemInputType: str = 'default', logicalZeroPointX: float = 0, logicalZeroPointInputType: str = 'default', logicalZeroPointY: float = 0, filePath: str = os.path.join(os.path.expanduser('~'), 'Documents') +'/', fileName: str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')):
        """Object that keeps track of project attributes ans structures returned data

        Args:
            copiedData (str): This is for the copy and pasted data out of Hamina
            measuringSystem (str, optional): set to 'metric' or 'imperial'. Defaults to 'metric'.
            measuringSystemInputType (str, optional): This defines how the data was inputed used for trust levels ['user' > script(map note) > default]. Defaults to 'default'.
            logicalZeroPointX (float, optional): set logical X coordinates to measure AP distance from. Defaults to 0.
            logicalZeroPointInputType (str, optional): This defines how the data was inputed used for trust levels ['user' > script(setXY) > script(map note) > default]. Defaults to 'default'.
            logicalZeroPointY (float, optional): set logical Y coordinates to measure the AP distance from. Defaults to 0.
            filePath(str, optional): Set the file path where to save data. Defaults to users Documents folder
            fileName(str, optional): Set the file name if not provided use datetime. default = Year-Month-Day_Hour_Minutes_Seconds
        """
        self.measuringSystem = measuringSystem
        self.measuringSystemInputType = measuringSystemInputType
        self.logicalZeroPointX = logicalZeroPointX
        self.logicalZeroPointInputType = logicalZeroPointInputType
        self.logicalZeroPointY = logicalZeroPointY
        self.filePath = filePath 
        self.fileName = fileName
        self.haminaData: dict = json.loads(copiedData)
    
        #Check copied data for measurement system if no value was provided
        if measuringSystemInputType == 'default':
            for mapNote in self.haminaData['mapNotes']:
                if 'zero point' in mapNote['text'].lower() or 'zeropoint' in mapNote['text'].lower():
                    if 'feet' in mapNote['text'].lower() or 'imperial' in mapNote['text'].lower():
                        self.measuringSystem = 'imperial'
                        self.measuringSystemInputType = 'Script(map note)'

        #Check copied data for higher level logical zero point if default or script(map note)
        if logicalZeroPointInputType == 'default' or logicalZeroPointInputType == 'Script(map note)':
            for mapNote in self.haminaData['mapNotes']:
                if 'setxy=' not in mapNote['text'].lower():
                    self.logicalZeroPointX = mapNote['x']
                    self.logicalZeroPointY = mapNote['y']
                    self.logicalZeroPointInputType = 'Script(map note)'
                else:
                    tempList = mapNote['text'].lower().split(' ')
                    for element in tempList:
                        if 'setxy=' in element:
                            temp = element.strip('setxy=')
                            coords = temp.split(':')
                            if self.measuringSystem == 'imperial':
                                self.logicalZeroPointX = imperialMetric(float(coords[0]))
                                self.logicalZeroPointY = imperialMetric(float(coords[1]))
                            else:
                                self.logicalZeroPointX = float(coords[0])
                                self.logicalZeroPointY = float(coords[1])
                            
                            self.logicalZeroPointInputType = "Script (SetXY from map notes)"
                break

        #Loop through APs and Update names:
        for aps in self.haminaData['accessPoints']:
            originalName = aps['name']
            if self.measuringSystem == 'imperial':
                logicalX = str(imperialFormatted(metricImperial(aps['x'] - self.logicalZeroPointX)))
                logicalY = str(imperialFormatted(metricImperial((aps['y'] - self.logicalZeroPointY) * (-1))))
            else:
                logicalX = '%.3f'%(aps['x'] - self.logicalZeroPointX) + 'm'
                logicalY = '%.3f'%((aps['y'] - self.logicalZeroPointY) * (-1)) + 'm'
            aps['name'] = f'{originalName} X:{logicalX} Y:{logicalY}'

    def to_txt(self) -> None:
        """Write data to text file in json format
        """
        with open(self.filePath + self.fileName + '.txt', 'w') as f:
            f.write(json.dumps(self.haminaData, indent=2))
    
    def to_json(self) -> None:
        """Write data to json file
        """
        with open(self.filePath + self.fileName + '.json', 'w') as f:
            f.write(json.dumps(self.haminaData, indent=2))
    
    def to_csv(self) -> None:
        import pandas as pd
        results = []
        for ap in self.haminaData['accessPoints']:
            results.append({
                'AP Name': ap['name'],
                'Make & Model': (ap['make'] + ' ' + ap['model']), 
                'Antenna': str(ap['externalAntennaMake']) + ' ' + str(ap['externalAntennaModel']), 
                'Mount': ap['mount'], 
                'Elevation tilt': str(ap['elevation']), 
                'Azimuth': str(ap['azimuth'])
            })
        df = pd.DataFrame(results)
        df.to_csv(self.filePath + self.fileName + '.csv', index=False)

# Conversions between Imperial and Metric also formatting imperial to Ft and Inches instead of decimal
def imperialMetric(val: float) -> float:
    """This function takes a measurement in Feet and converts it into Meters

    Args:
        val (float): Distance in Feet

    Returns:
        float: Distance in Meters
    """
    return val*.3048

def metricImperial(val: float) -> float:
    """This function takes a measurement in Meters and converts it into Feet

    Args:
        val (float): Distance in Meters

    Returns:
        float: Distance in Feet
    """
    return val/.3048

def imperialFormatted(val: float) -> str:
    """This function takes a value in Feet and converts the remainder into the closest inch. It then returns it in a string to be appended to an AP name.

    Args:
        val (float): _description_

    Returns:
        str: _description_
    """
    return str(int(val)) + 'ft ' + str(int(val %1 * 12)) + 'in'
