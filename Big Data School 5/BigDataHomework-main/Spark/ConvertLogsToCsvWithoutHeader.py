import csv, os, sys

colNames = ['Latitude','Longitude','AllZero','Altitude','NumberOfDays','Date','Time']

def cleanPlt(root, direc1, direc2, colNames):

	# read plt file
	with open(root + '/' + direc1 + '/Trajectory/' + direc2,'rt') as fin:
		cr = csv.reader(fin)
		filecontents = [line for line in cr][6:]
		filecontents.insert(0, colNames)

	# write csv file without header
	with open(root +'/' + direc1 + '/Trajectory/' + direc2[:-4] + '.csv','w') as fou:
		cw = csv.writer(fou, lineterminator='\n')
		cw.writerows(filecontents)

	os.remove(root + '/' + direc1 + '/Trajectory/' + direc2)

thedir = "D:\\Big_Data_School_5\DataFrame\Lesson_2\Geolife_Trajectories_1_3\Data_copy"

dirs = [name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name))]

for direc in dirs:
    if 'labels_csv.csv' in os.listdir(thedir + '/' + direc):
       	print('Cleaning:', direc)
       	tempdirs = os.listdir(thedir + '/' + direc + '/Trajectory')
       	subdirs = []
       	for item in tempdirs:
       		if not item.endswith('.DS_Store'):
       			subdirs.append(item)
       	for subdir in subdirs:
       		cleanPlt(thedir, direc, subdir, colNames)