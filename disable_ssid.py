#!/usr/bin/env python3
"""
Copyright (c) 2022 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import meraki
import os
import sys
from dotenv import load_dotenv


def main(argv):
    # assign variables from env file
    load_dotenv()
    API_KEY = os.environ.get("API_KEY")
    ORG_ID = os.environ.get("ORG_ID")
    SSID_NAME = os.environ.get("SSID_NAME")

    # connect to Meraki
    dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)

    # retrieve networks in organization
    try:
        networks = dashboard.organizations.getOrganizationNetworks(ORG_ID)
    except Exception as e:
        print("Failed to get networks for organization with id " + ORG_ID)
        print(e)

        return

    # retrieve all SSIDs for each network in the organization
    for network in networks:
        network_id = network["id"]
        try:
            ssids = dashboard.wireless.getNetworkWirelessSsids(network_id)
        except Exception as e:
            print("Failed to get SSIDs of network " + network['name'])
            print(e)

            continue

        # go through all the SSIDs and disable the SSIDs that match the SSID in the env file
        for ssid in ssids:
            if ssid["name"] == SSID_NAME:
                ssid_number = ssid["number"]
                try:
                    response = dashboard.wireless.updateNetworkWirelessSsid(network_id, ssid_number, enabled=False)
                    print("Updated SSID " + SSID_NAME + " of network " + network['name'])
                except Exception as e:
                    print("Failed to disable " + SSID_NAME + " of network " + network['name'])
                    print(e)

                    continue


if __name__ == "__main__":
    sys.exit(main(sys.argv))
