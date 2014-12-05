#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  importData.py
#
#  Copyright 2014 Michael Comerford <michael.comerford@glasgow.ac.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import urllib2
import urllib
import requests
import json
import os
import traceback
import xml.etree.ElementTree as ET

# set debug mode 
#1=parse but don't call api
#0=parse and call api
dry_run = 1

pathtoData = "/path/to/data/"
pathtoMetadata = "/path/to/metadata/"

namespaces = {
    'dcat': "http://www.w3.org/ns/dcat#",
    'dct': "http://purl.org/dc/terms/",
    'foaf': "http://xmlns.com/foaf/0.1/",
    'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    'dc': "http://purl.org/dc/elements/1.1/",
    'skos': "http://www.w3.org/2004/02/skos/core#",
}

fileListData = os.listdir(pathtoData)
#print(fileListData)
fileListMetadata = os.listdir(pathtoMetadata)
#print(fileListMetadata)

#print(len(fileListData))
for x in range(0, len(fileListMetadata)):
#for x in range(0,1):
    datamatches = []
    print fileListMetadata[x]
    xid = str((fileListMetadata[x])).split("---")
    identifierMeta = xid[0]
    #print(identifierMeta)
    #print(fileListMetadata[x])
    for y in range(0, len(fileListData)):
        yid = str((fileListData[y])).split("---")
        #print(yid)
        identifierData = yid[0]
        #print(yid[0])
        if identifierData == identifierMeta:
            #print("\tmatch!")
            #print(identifierData)
            datamatches.append(fileListData[y])
            print '\t'+fileListData[y]
    if len(datamatches):
    # Put the details of the dataset we're going to create into a dict.
        f = open((pathtoMetadata+fileListMetadata[x]), "r")
        try:
            tree = ET.parse(f)
            root = tree.getroot()
            try:
                dataset = root.findall('dcat:Dataset', namespaces)[0]
            except IndexError:
                print "cannot find 'dcat:Dataset' in metadata"
                dataset = ET.Element('blank', attrib={})
            try:
                identifier = dataset.findall('dct:identifier', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:identifier' in metadata"
                identifier = ET.Element()
            try:
                title = dataset.findall('dct:title', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:title' in metadata"
                title = ET.Element()
            try:
                contactPoint = dataset.findall('dcat:contactPoint', namespaces)[0]
            except IndexError:
                print "cannot find 'dcat:contactPoint' in metadata"
                contactPoint = ET.Element()
            try:
                description = dataset.findall('dct:description', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:description' in metadata"
                description = ET.Element()
            try:
                landingPage = dataset.findall('dcat:landingPage', namespaces)[0]
            except IndexError:
                print "cannot find 'dcat:landingPage' in metadata"
                landingPage = ET.Element()
            try:
                issued = dataset.findall('dct:issued', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:issued' in metadata"
                issued = ET.Element()
            try:
                modified = dataset.findall('dct:modified', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:modified' in metadata"
                modified = ET.Element()
            try:
                language = dataset.findall('dc:language', namespaces)[0]
            except IndexError:
                print "cannot find 'dc:language' in metadata"
                language = ET.Element()
            try:
                spatial = dataset.findall('dct:spatial', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:spatial' in metadata"
                spatial = ET.Element()
            try:
                temporal = dataset.findall('dct:temporal', namespaces)[0]
            except IndexError:
                print "cannot find 'dct:temporal' in metadata"
                temporal = ET.Element()
            try:
                accrualPeriodicity = dataset.findall('dct:accrualPeriodicity',
                                             namespaces)[0]
            except IndexError:
                print "cannot find 'dct:accrualPeriodicity' in metadata"
                accrualPeriodicity = ET.Element()
            #publisher = dataset.findall('dct:publisher', namespaces)[0]
            try:
                keyword = dataset.findall('dcat:keyword', namespaces)[0]
            except IndexError:
                print "cannot find 'dcat:keyword' in metadata"
                keyword = ET.Element('blank', attrib={'text': ' '})
            #theme = dataset.findall('dcat:theme', namespaces)[0]
            #definition = dataset.findall('dct:definition', namespaces)

            # copy elements to another dict for the api call
            dcat_dict = dict({
                'identifier': identifier.text,
                'name': title.text,
                'title': title.text,
                'contactPoint': contactPoint.text,
                'notes': description.text,
                'landingPage': landingPage.text,
                'issued': issued.text,
                'modified': modified.text,
                'language': language.text,
                'spatial': spatial.text,
                'temporal': temporal.text,
                'accrualPeriodicity': accrualPeriodicity.text,
                #'publisher': publisher_schema(),
                'keyword': keyword.text,
                #'distribution': dataset_dict['distribution'],
                #'theme': dataset_dict['identifier'],
                #'definition': dataset_dict['identifier'],
            })

        # Use the json module to dump the dictionary to a string for posting.
            data_string = urllib.quote(json.dumps(dcat_dict))
            #print data_string

            if dry_run == 0:
                # We'll use the package_create function to create a new dataset.
                request = urllib2.Request(
                    'URL_OF_CKAN/api/action/package_create')
                # Creating a dataset requires an authorization header.
                # Replace *** with your API key, from your user account on the CKAN site
                # that you're creating the dataset on.
                request.add_header('Authorization', '***')
                # Make the HTTP request.
                response = urllib2.urlopen(request, data_string)
                assert response.code == 200
                # Use the json module to load CKAN's response into a dictionary.
                response_dict = json.loads(response.read())
                assert response_dict['success'] is True
                # package_create returns the created package as its result.
                created_package = response_dict['result']
                #pprint.pprint(created_package)
                package_id = created_package['id']

            for index in range(len(datamatches)):
                resource = str(datamatches[index]).split("---")[1]
                resource_format = (resource.split("."))[1]
                resource_name = (resource.split("."))[0]
                #print resource
                #print resource_format
                #print resource_name
                if dry_run == 0:
                    requests.post('URL_OF_CKAN/api/action/resource_create',
                        data={"package_id": package_id, "format": resource_format, "name": resource_name},
                        headers={"X-CKAN-API-Key": "***"},
                        files=[('upload', file(pathtoData+datamatches[index]))])

        except ET.ParseError, e:
            print "XML not well formed for "+fileListMetadata[x]
            print traceback.format_exc()
    else:
        print "No match found"
