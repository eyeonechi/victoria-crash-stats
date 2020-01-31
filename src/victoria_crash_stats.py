import codecs as cd
import flask as fls
import json
import matplotlib.pyplot as plt
# import mpl_toolkits.basemap as bm
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sklearn.preprocessing as sp
import sklearn.decomposition as sd

# Mapping of renamed columns.
renameDict = {
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
    'SPEED_ZONE'            : 'Zone'
}

# Used when transferring data between client and server.
referenceDict = {
    'Reference Number'              : 'Number',
    'Accident Date'                 : 'Date',
    'Accident Time'                 : 'Time',
    'Accident Type Number'          : 'AccType',
    'Accident Type Description'     : 'AccDesc',
    'Day Number'                    : 'Day',
    'Day Description'               : 'DayDesc',
    'Accident Class Number'         : 'DCA',
    'Accident Class Description'    : 'DCADesc',
    'Lighting Number'               : 'Light',
    'Lighting Description'          : 'LightDesc',
    'Number of Vehicles Involved'   : 'NumVehicles',
    'Number of People Involved'     : 'NumPersons',
    'Number of People Injured'      : 'NumInjured',
    'Number of People Killed'       : 'NumKilled',
    'Number of Healthy People'      : 'NumHealthy',
    'Number of Police Involved'     : 'NumPolice',
    'Road Geometry Number'          : 'Geometry',
    'Road Geometry Description'     : 'GeometryDesc',
    'Accident Severity'             : 'Severity',
    'Speed Zone'                    : 'Zone'
}

# Maps Month to Month Number
monthDict = {
    'January'   : '01',
    'February'  : '02',
    'March'     : '03',
    'April'     : '04',
    'May'       : '05',
    'June'      : '06',
    'July'      : '07',
    'August'    : '08',
    'September' : '09',
    'October'   : '10',
    'November'  : '11',
    'December'  : '12'
}

# Aggregation methods used.
pivotDict = {
    'Average': np.mean,
    'Maximum': np.max,
    'Minimum': np.min,
    'Sum'    : np.sum
}

# Columns to be removed in selecting principle components.
removeCols = [
    'DCA',
    'Edition',
    'GridY',
    'Node',
    'Zone'
]

# Handles extracting data from its raw form.
def openData(location):
    return pd.read_csv(cd.open(location, 'r', 'utf-8-sig'))

# Saves data to the specified location in csv format.
def saveData(data, location):
    data.to_csv(location)

# Renames columns into managable indexes.
def renameData(data, rename):
    data = data.rename(columns=rename)
    return data

# Removes unwanted columns from the dataset.
def cleanData(data, columns):
    data.drop(columns, axis=1, inplace=True)
    return data

# Filters dataset and returns rows corresponding to year given.
def filterData(data, accident, date, day, definition, geometry, lighting,
		month, severity, year):
    data = data[data.AccDesc.str.contains(accident)] if accident else data
    data = data[data.Date.apply(
    	lambda x: date == str(x).split('/')[0])] if date else data
    data = data[data.DayDesc.str.contains(day)] if day else data
    data = data[data.DCADesc.str.contains(definition)] if definition else data
    data = data[data.GeometryDesc.str.contains(geometry)] if geometry else data
    data = data[data.LightDesc.str.contains(lighting)] if lighting else data
    data = data[data.Date.apply(
    	lambda x: monthDict[month] == str(x).split('/')[1])] if month else data
    data = data[data.GeometryDesc.str.contains(severity)] if severity else data
    data = data[data.Date.apply(
    	lambda x: year == str(x).split('/')[2])] if year else data
    return data.fillna(0)

# Visualises a pivot table based on a given pivot column.
def pivotData(data, index, values, method):
    return pd.pivot_table(data, index=index, values=values,
        aggfunc=method, fill_value=0) if index else data

# Visualisation of dataset.
def visualiseData(data):
    plotA(data.groupby('DayDesc', as_index=False).sum(),
          'Total Involved in Accidents by Day')
    plotA(data.groupby('DayDesc', as_index=False).mean(),
          'Average Involved in Accidents by Day')
    plotB(data.groupby('AccDesc', as_index=False).sum(),
          'Total Involved in Accidents by Type')
    plotB(data.groupby('AccDesc', as_index=False).mean(),
          'Average Involved in Accidents by Type')
    plotC(data.groupby('LightDesc', as_index=False).sum(),
          'Total Involved in Accidents by Lighting')
    plotC(data.groupby('LightDesc', as_index=False).mean(),
          'Average Involved in Accidents by Lighting')
    plotD(data.groupby('GeometryDesc', as_index=False).sum(),
          'Total Involved in Accidents by Road Geometry')
    plotD(data.groupby('GeometryDesc', as_index=False).mean(),
          'Average Involved in Accidents by Road Geometry')
    plotE(data)
    plotF(data)
    node = openData('data/node.csv')
    plotG(node)

# Plot graphs related to day.
def plotA(data, title):
    plt.figure()
    ax = plt.subplot(111)
    x = np.arange(len(data.DayDesc))
    y = ['NumVehicles', 'NumPersons', 'NumInjured', 'NumKilled']
    plt.xticks(x, data.DayDesc)
    width = 0.3
    palette = ['red', 'blue', 'green', 'yellow']
    for i in range(len(y)):
        ax.bar(x + (i * width), data[y[i]], width, align='center',
        	color=palette[i])
    ax.legend(y, loc='best')
    plt.xlabel('Day')
    plt.ylabel('Number')
    plt.title(title)
    plt.show()

# Plot graphs related to accident type.
def plotB(data, title):
    plt.figure()
    ax = plt.subplot(111)
    x = np.arange(len(data.AccDesc))
    y = ['NumVehicles', 'NumPersons', 'NumInjured', 'NumKilled']
    plt.xticks(x, data.AccDesc, rotation=70)
    width = 0.3
    palette = ['cyan', 'skyblue', 'blue', 'darkblue']
    for i in range(len(y)):
        ax.bar(x + (i * width), data[y[i]], width, align='center',
        	color=palette[i])
    ax.legend(y, loc='best')
    plt.xlabel('Type')
    plt.ylabel('Number')
    plt.title(title)
    plt.show()

# Plots graphs related to lighting.
def plotC(data, title):
    plt.figure()
    ax = plt.subplot(111)
    x = np.arange(len(data.LightDesc))
    y = ['NumVehicles', 'NumPersons', 'NumInjured', 'NumKilled']
    plt.xticks(x, data.LightDesc, rotation=70)
    width = 0.3
    palette = ['yellow', 'orange', 'red', 'black']
    for i in range(len(y)):
        ax.bar(x + (i * width), data[y[i]], width, align='center',
        	color=palette[i])
    ax.legend(y, loc='best')
    plt.xlabel('Lighting')
    plt.ylabel('Number')
    plt.title(title)
    plt.show()

# Plots graphs related to road geometry.
def plotD(data, title):
    plt.figure()
    ax = plt.subplot(111)
    x = np.arange(len(data.GeometryDesc))
    y = ['NumVehicles', 'NumPersons', 'NumInjured', 'NumKilled']
    plt.xticks(x, data.GeometryDesc, rotation=70)
    width = 0.3
    palette = ['pink', 'maroon', 'violet', 'purple']
    for i in range(len(y)):
        ax.bar(x + (i * width), data[y[i]], width, align='center',
        	color=palette[i])
    ax.legend(y, loc='best')
    plt.xlabel('Road Geometry')
    plt.ylabel('Number')
    plt.title(title)
    plt.show()

# Plots a scatterplot of number of people in different speed zones.
def plotE(data):
    sns.set(style='ticks', context='talk', font_scale=1.75)
    data['DateTime'] = data.Date + ':' + data.Time
    data['DateTime'] = pd.to_datetime(data.DateTime.astype(str),
    	format='%d/%m/%Y:%H.%M.%S')
    data = data[data['Zone'] < 200]
    fig = sns.FacetGrid(data=data, hue='AccType', height=8, aspect=1.4)
    fig.map(plt.scatter, 'Zone', 'NumPersons').add_legend()
    plt.title('Number of People Involved in Different Speed Zones')
    plt.show()

# Plots a heatmap of the datasets principle components
def plotF(data):
    data = data.select_dtypes(include=[np.number])
    data = data.drop(removeCols, axis=1)
    data_std = sp.StandardScaler().fit_transform(data)
    sklearn_pca = sd.PCA()
    sklearn_pca.fit(data_std)
    plt.plot(range(len(data.columns)), sklearn_pca.explained_variance_ratio_)
    plt.xticks(range(len(data.columns)))
    plt.xlabel('Principle Component')
    plt.ylabel('Percentage of Variance Explained')
    plt.show()
    sns.heatmap(data_std, cmap='magma', xticklabels=False, yticklabels=False)
    plt.title('Heatmap')
    plt.show()

# Plots a map of accident coordinates.
def plotG(data):
    plt.figure(figsize=(16,10))
    # datamap = bm.Basemap(projection='merc', lat_0=-37.4713, lon_0=144.7852,
    #     resolution='l', epsg=4326, area_thresh=0.1, llcrnrlat=-39.188314,
    #     llcrnrlon=140.711512, urcrnrlat=-33.922496, urcrnrlon=150.052936)
    datamap.arcgisimage(service='ESRI_Imagery_World_2D',
        xpixels=1024, verbose=True)
    datamap.drawrivers(color="aqua")
    data['Region Name'] = data['Region Name'].astype(str)
    categories = np.unique(data['Region Name'])
    colors = np.linspace(0, 1, len(categories))
    colordict = dict(zip(categories, colors))
    data['color'] = data['Region Name'].apply(lambda x: colordict[x])
    x, y = datamap(data.Long, data.Lat)
    datamap.scatter(x, y, c=data['color'], cmap='rainbow', marker='o')
    plt.title('Accident Locations in Victoria')
    plt.show()

# Handles the main process of data wrangling.
def main():
    data = openData('data/accident.csv')
    data = renameData(data, renameDict)
    data['NumInjured'] = data.NumInjured2 + data.NumInjured3
    data = cleanData(data, ['NumInjured2', 'NumInjured3'])
    saveData(data, 'data/accident_cleaned.csv')
    data = openData('data/accident_cleaned.csv')
    data = cleanData(data, 'Unnamed: 0')
    visualiseData(data)

# Interacts with javascript through client-server processing.
app = fls.app.Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return fls.render_template('victoria_crash_stats.html', title='Home')

@app.route('/submission', methods=['GET', 'POST'])
def submission():
    callback = fls.request.args.get('callback')
    method = json.loads(fls.request.data)['method']
    if method == 'dataset':
        return json.dumps(dataset(method))
    elif method == 'pivotTable':
        return json.dumps(pivotTable(method))
    else:
        return '{}({})'.format(callback, error())

# Processes dataset and returns it to client.
def dataset(method):
    requestData = json.loads(fls.request.data)
    accident = requestData['accident']
    date = requestData['date']
    day = requestData['day']
    definition = requestData['definition']
    geometry = requestData['geometry']
    lighting = requestData['lighting']
    month = requestData['month']
    severity = requestData['severity']
    year = requestData['year']
    data = openData('data/accident_cleaned.csv')
    data = cleanData(data, 'Unnamed: 0')
    data = filterData(data, accident, date, day, definition, geometry, lighting, month, severity, year)
    if method == 'pivotTable':
        return data
    data['Index'] = range(len(data))
    data = data.fillna(0).to_dict()
    return data

# Returns pivoted dataset to client.
def pivotTable(method):
    requestData = json.loads(fls.request.data)
    agg = requestData['aggregation']
    agg = pivotDict[agg] if agg in pivotDict else 'Mean'
    column = requestData['column']
    column = referenceDict[column] if column in referenceDict else None
    row = requestData['row']
    row = referenceDict[row] if row in referenceDict else None
    data = dataset(method)
    data = pivotData(data, column, row, agg)
    data = data.reset_index().to_dict()
    return data

# Returns an empty dict if nothing valid is specified.
def error():
    return 'error'

if __name__ == '__main__':
    # Run data processing section.
    # main()
    # Run server handling section.
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))
