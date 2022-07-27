# Hedwig

## About

A rewrite of [archimedes](https://github.com/utkdigitalinitiatives/archimedes) in Python.

This implements the SteelCase RoomWizard API and interfaces with the LibCal RoomBookings API.

## How Does This Work

Students book rooms in [LibCal](https://libcal.utk.edu/booking/studyrooms).

This application fetches data from the LibCal API and transforms it according to the RoomWizard API so that a RoomWizard
can consume it.

## Todo

- [ ] Add configuration for various LibCal APIs and how often to poll LibCal.

