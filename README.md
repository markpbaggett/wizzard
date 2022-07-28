# Wizzard :mage_man:

![Wizzard](https://i.ytimg.com/vi/BiQCvAnyyQI/hqdefault.jpg)
 
Wiz! Totally Wizzed Out! Room booking with my #$@&%*! son! :guitar: :notes:

Wiz! Totally Wizzed Out! [Archimedes](https://github.com/utkdigitalinitiatives/archimedes) is dead but that doesn't mean we can't have fun! :guitar: :notes:

## About

Wizzard is a rewrite of [archimedes](https://github.com/utkdigitalinitiatives/archimedes) in Python.

This implements the SteelCase RoomWizard API and interfaces with the LibCal RoomBookings API.

## How Does This Work

Students book rooms in [LibCal](https://libcal.utk.edu/booking/studyrooms).

This application fetches data from the LibCal API and transforms it according to the RoomWizard API so that a RoomWizard
can consume it.

## Installation

Installation is easiest with [poetry](https://python-poetry.org/):

```shell
poetry install

```

## Configuration

Configuration is done via environmental variables. The following are expected:

* **client_id**: your LibCal client_id
* **secret**: your LibCal secret
* **name**: what you want to name your connector
* **version**: the version of your connector
* **short**: a short name for your connector

## Todo

- [ ] Add configuration for various LibCal APIs and how often to poll LibCal.

