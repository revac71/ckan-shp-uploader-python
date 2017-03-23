#!/usr/bin/python
# -------------------------------------------------------------------------------------------------
# Name:        ckan_lib_v01.py
# Purpose:     Used for communicating with a CKAN repo for open data.
# Author:      Renato Enrique (revac71@gmail.com)
# Created:     2017-03-10
# Copyright:   (c) Code For San Jose 2017
#
# History:
# 2017-03-10 revac71 created
# -------------------------------------------------------------------------------------------------

from __future__ import print_function, unicode_literals

import ckanapi
import os.path

# Renato's info to talk to VTA's CKAN repo
API_KEY = r"2405b0f8-a4c6-499d-bd01-7f40028ab31f"
SERVER = r'http://data2.vta.org'
USER_AGENT = r'CKAN SHP Uploader'
ckan_inst = ckanapi.RemoteCKAN(SERVER, apikey=API_KEY, user_agent=USER_AGENT)


def get_dataset_info(dataset_title):
	"""
	Retrieves the data set object with the title 'dataset_title'.
	"""
	ds = None
	try:
		ds = ckan_inst.action.package_show(id=dataset_title)
	except ckanapi.NotFound as caught:
		print("Error retrieving the data set '{}': '{}'".format(dataset_title, caught))

	return ds


def create_dataset(dataset_name, dataset_title, owner_org='vta'):
	"""
	Create a dataset with an associated resource
	"""
	try:
		ckan_inst.action.package_create(
			name=dataset_name,
			title=dataset_title,
			owner_org=owner_org)
	except ckanapi.ValidationError as caught:
		print("{}".format(caught))
		return
	except ckanapi.NotAuthorized as caught:
		print('Access denied. Is your API key valid?')
		print("{}".format(caught))
		return

	# If we reach this point it is all good
	return True


def add_resource_to_dataset(package_id, filepath, name=None, url='dummy-value', data_format='csv'):
	"""
	Upload a new resource and associate it with a dataset
	"""
	if name is None:
		name = os.path.basename(filepath)
	try:
		print('uploading...')
		res = ckan_inst.action.resource_create(
			package_id=package_id,
			name=name,
			upload=open(filepath, 'rb'),
			url=url,
			format=data_format)
		print('done')
		return res
	except ckanapi.ValidationError as ex:
		print(ex)
	except ckanapi.NotAuthorized as ex:
		print('access denied. Is your API key valid?')
		print(ex)
		return
	print('done')


def update_resource(dataset_title, filepath, name=None, url='dummy-value', data_format='csv', owner_org='vta'):
	"""
	For this to work, the resource names should be unique (this is not enforced).
	If the names are not unique, only the last one with the same name will be updated.

	http://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.update.resource_update
	"""
	# run a SOLR search for the package
	# http://data2.vta.org/api/3/action/package_search?q=&fq=title:ins_sample%20AND%20organization:city-of-san-jose
	solr_query = 'title:{0} AND organization:{1}'.format(dataset_title, owner_org)
	res = ckan_inst.action.package_search(q=solr_query)
	if res.get('count') is not 1:
		print('could not find the requested dataset; dataset title and organization not specific enough')
		return

	print('looking for file "{0}" inside the "{1}" dataset'.format(name, dataset_title))
	resource_id = None
	for r in res.get('results')[0].get('resources'):
		print (str(r.get('name')) + ' : ' + str(r.get('id')))
		if str(r.get('name')) == str(name):
			resource_id = r.get('id')

	if resource_id is None:
		print('could not find the requested resource')
		return
	else:
		print('found resource id "{0}"'.format(resource_id))

	print('uploading...')
	try:
		res = ckan_inst.action.resource_update(
			id=resource_id,
			name=name,
			upload=open(filepath, 'rb'),
			url=url,
			format=data_format)
		print('done')
		return res
	except ckanapi.ValidationError as ex:
		print(ex)
	except ckanapi.NotAuthorized as ex:
		print('access denied. Is your API key valid?')
		print(ex)
		return
	print('done')


def purge_dataset(dataset_id):
	"""
	WARNING: cannot be undone
	This frees up the URL of the resource
	"""
	try:
		ckan_inst.call_action('dataset_purge', {'id': dataset_id})
	except ckanapi.ValidationError as caught:
		print("{}".format(caught))
	except ckanapi.NotAuthorized as caught:
		print('Access denied. Is your API key valid?')
		print("{}".format(caught))
		return


def delete_dataset(dataset_id):
	"""
	Delete a dataset
	"""
	try:
		ckan_inst.action.package_delete(id=dataset_id)
	except ckanapi.ValidationError as caught:
		print("{}".format(caught))
	except ckanapi.NotAuthorized as caught:
		print('Access denied. Is your API key valid?')
		print("{}".format(caught))
		return
