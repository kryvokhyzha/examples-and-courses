import csv, os, sys

def convertToCSV(root, direc):

	# read tab-delimited file
    with open(root + '/' + direc + '/' + 'labels.txt','rt') as fin:
        cr = csv.reader(fin, delimiter='\t')
        filecontents = [line for line in cr]
	# write comma-delimited file (comma is the default delimiter)
    with open(root + '/' + direc + '/' + 'labels_csv.csv','w') as fou:
    	cw = csv.writer(fou, lineterminator='\n')
    	cw.writerows(filecontents)

    #os.remove(root + '/' + direc + '/' + 'labels.txt')

thedir = "D:\\Big_Data_School_5\DataFrame\Lesson_2\Geolife_Trajectories_1_3\Data_copy"

dirs = [name for name in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, name))]

for direc in dirs:
	if 'labels.txt' in os.listdir(thedir + '/' + direc):
		convertToCSV(thedir, direc)