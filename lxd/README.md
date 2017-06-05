# Lxd Integration

## Overview

Get metrics from lxd containers in real time to:

* Visualize and monitor lxd states

## Installation

Install the `dd-check-lxd` package manually or with your favorite configuration manager

## Configuration

The dd-agent account needs to be included in the lxd group to gain access to the
LXD API.

!!! WARNING !!!
THIS IS A MAJOR SECURITY ISSUE AS THE DD-AGENT WILL GAIN FULL R/W ACCESS TO THE
API, HENCE BE ABLE TO CREATE/DELETE/SHUTDOWN ANY CONTAINER. THIS IS FOR PROOF OF
CONCEPT ONLY
!!!

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        lxd
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The lxd check is compatible with ubuntu Xenial and later.
