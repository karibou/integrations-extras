# Lxd Integration

## Overview

Get metrics from lxd service in real time to:

* Visualize and monitor lxd states
* Be notified about lxd failovers and events.

## Installation

Install the `dd-check-lxd` package manually or with your favorite configuration manager

## Configuration

Edit the `lxd.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        lxd
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The lxd check is compatible with all major platforms
