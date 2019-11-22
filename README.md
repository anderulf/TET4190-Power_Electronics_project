# TET4190-Power_Electronics_project

By: Anders Ulfsnes, Trude Birgitte Byre, Johan P. Hald, Ole Martin M. Flatjord, and Kjeld Fjeldberg

For: Project in TET4190 at NTNU

This project has multiple files used to calculate different components written in python and matlab


Inductor:
It uses an iterative algorithm from Mohan "Power Electronics: converters, applications and design" 3rd ediotion

To run the inductor design algorithm go to the folder inductor design:
 
    run main.py
  
  
Capacitor:
It has one script which will calculate the losses when using one one capacitor type to handle the capacitance need

To run the capacitor choice script go to the folder capacitor:

    run capacitor_choice.m
  
  
Mosfet and diode:
It has one script to calculate the mosfet and diode switching and conduction losses

To run the mosfet and diode loss script go to the folder mosfet_diode:
  
    run MOSFET_DIODE_selection.m  
  
Frequency:
It has one script which inputs the acummulated inductor losses from inductor_design/main.py and calculates the total mosfet and diode losses. The script then calculates the optimal frequency for a range of cable types

To run thefrequency selection script go to the folder frequency:
  
    run frequency_selection.m 
    
    
