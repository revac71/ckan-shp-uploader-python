#!/usr/bin/python
# -------------------------------------------------------------------------------------------------
# Name:        verify_ckan_lib.py
# Purpose:     Verifies methods/functions in ckan_lib_v01.py
# Author:      Renato Enrique (revac71@gmail.com)
# Created:     2017-03-10
# Copyright:   (c) Code For San Jose 2017
#
# History:
# 2017-03-10 revac71 created
# -------------------------------------------------------------------------------------------------

from __future__ import print_function, unicode_literals

import os
import itertools
import ckan_lib_v01 as ckanlib


def verify_dataset_manipulation(dataset_id):
	"""Verifies creation, addition and update
	+ dataset_id - which one is correct: name, title or id?
	"""
	SAMPLE_FILE_1a = "samples/Sacramentorealestatetransactions_a.csv"
	SAMPLE_FILE_1b = "samples/Sacramentorealestatetransactions_b.csv"
	SAMPLE_FILE_2 = "samples/SalesJan2009.csv"

	if ckanlib.create_dataset(dataset_id, "Renato's sample", owner_org='test'):
		# Uploads the contents of SAMPLE_FILE_1b to a resource named SAMPLE_FILE_1a
		# under the 'renato_sample' dataset
		ckanlib.add_resource_to_dataset(dataset_id, SAMPLE_FILE_1a, name='SAMPLE_FILE_1a')

		# 4. Now we replace the contents of the resource named SAMPLE_FILE_1a
		# with the contents of the file in SAMPLE_FILE_1b
		ckanlib.update_resource(dataset_id, SAMPLE_FILE_1b, name='SAMPLE_FILE_1a', owner_org='test')


def verify_get_dataset_info():
	"""Verifies get_dataset_info()"""
	myds = ckanlib.get_dataset_info("testdata4renato")
	if myds is not None:
		# for key, value in myds.iteritems():
		# 	print("'{}' : '{}'".format(key, value))
		if "resources" in myds and "url" in myds["resources"][0]:
			print("URL to download data: '{}'".format(myds["resources"][0]["url"]))
		print("Done!")


def check_preview_file(filename):
	"""Checks that 'filename' exists and preview what we're going to upload"""
	if os.path.isfile(filename):
		with open(filename) as fp:
			head = list(itertools.islice(fp, 5))
		# for line in head[0].split("\r"):
		# 	print(line)
		print(head)
	else:
		print("The file '{}' is not a regular file or it is not found".format(filename))


if __name__ == "__main__":
	# TODO: why is it displaying all the data instead of just the first 5 lines?
	# check_preview_file(SAMPLE_FILE_1a)

	# verify_get_dataset_info()

	# TODO: why is the error 'URL is already in use' if dataset was already deleted?
	#       does it mean the dataset somehow still exists somewhere?
	# verify_dataset_manipulation('renato_sample')

	# Don't forget to change name next time it runs
	# TODO: why the update did not work? error says...
	# 'could not find the requested dataset; dataset title and organization not specific enough'
	# verify_dataset_manipulation('renato_sample_2')

	# TODO: 'purge' does not work but 'delete' does, why?
	# ckanlib.purge_dataset('renato_sample')
	ckanlib.delete_dataset('renato_sample_2')

