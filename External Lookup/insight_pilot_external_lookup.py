#!/usr/bin/env python

import csv
import sys
import socket
import json
import requests as req

def dummy_api_call(requestURL, parameters):
    response=req.get(url=requestURL,params=parameters)
    if response.status_code != 200:
        print('Status: ', response.status_code,'Headers: ',response.headers,'Error Response: ',response.json())
        exit()
    data=response.json()
    return json.dumps(data)

# Given a productid, find the productdesc
def lookup(productid):
    try:
        descriptions = []
        requestURL = "https://dummyjson.com/products?limit=0&select=description"
        parameter = {}
        description_list = dummy_api_call(requestURL, parameter)
        data = json.loads(description_list)
        for description in data["products"]:
            if productid == "*":
                descriptions.append(description)
            elif str(description["id"]) == str(productid):
                descriptions.append(description)
                break
        return descriptions
    except:
        return []

# Given an productdesc, return the productid
def rlookup(productdesc):
    try:
        descriptions = []
        requestURL = "https://dummyjson.com/products?limit=0&select=description"
        parameter = {}
        description_list = dummy_api_call(requestURL, parameter)
        data = json.loads(description_list)
        for description in data["products"]:
            if productdesc == "*":
                descriptions.append(description)
            elif str(description["description"]) == str(productdesc):
                descriptions.append(description)
                break
        return descriptions
    except:
        return []

def main():
    if len(sys.argv) != 3:
        print("Usage: python insight_pilot_external_lookup.py [productid field] [productdesc field]")
        sys.exit(1)

    productid = sys.argv[1]
    productdesc = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        # Perform the lookup or reverse lookup if necessary
        if result[productid] and result[productdesc]:
            # both fields were provided, just pass it along
            w.writerow(result)

        elif result[productid]:
            # only productid was provided, add productdesc
            productdescs = lookup(result[productid])
            for desc in productdescs:
                result[productdesc] = desc["description"]
                w.writerow(result)

        elif result[productdesc]:
            # only productdesc was provided, add productid
            productids = rlookup(result[productdesc])
            for pid in productids:
                result[productid] = pid["id"]
                w.writerow(result)

main()
