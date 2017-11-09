#!/usr/bin/env python3
import sys
from subprocess import call
from multiprocessing import Pool

def iter_months(start_year, start_month, end_year, end_month):
	year, month = start_year, start_month

	while True:
		if (year, month) == (end_year, end_month):
			return
		yield year, month
		month += 1
		if month > 12:
			month = month % 12
			year += 1

def download(year, month):
	filename = 'consensuses-{}-{:02}.tar.xz'.format(year, month)
	url = "https://collector.torproject.org/archive/relay-descriptors/consensuses/" + filename
	print("Downloading {}".format(url))
	ret = call(['wget', '-q', '-O', filename, url])
	if ret != 0:
		print("{} download failed!".format(filename))
	return ret

if __name__ == '__main__':
	if len(sys.argv) != 3:
		sys.exit('usage: {} start_time end_time'.format(sys.argv[0]))

	start_time = sys.argv[1]
	end_time = sys.argv[2]

	if start_time >= end_time:
		sys.exit('Error: please check start_time and end_time')

	start_year = int(start_time.split('-')[0])
	start_month = int(start_time.split('-')[1])
	end_year = int(end_time.split('-')[0])
	end_month = int(end_time.split('-')[1])

	with Pool(5) as p:
		print(p.starmap(download, iter_months(start_year, start_month, end_year, end_month)))