# TET4190-Power_Electronics_project



This project has multiple files used to calculate different components written in python and matlab


Inductor:
It uses an iterative algorithm from Mohan "Power Electronics: converters, applications and design" 3rd ediotion
To run the inductor design algorithm:

    Under inductor design (make sure auxillary.py is in same folder)
 
    run main.py
  
  
Capacitor:
It has one script which will calculate the losses when using one one capacitor type to handle the capacitance need
To run the capacitor choice script:

    Under capacitor
  
    run capacitor_choice.m
  
  
Mosfet and diode:
It has one script to calculate the mosfet and diode switching and conduction losses
To run the mosfet and diode loss script:

    Under mosfet_diode
  
    run mosfet_diode_losses.m  
  
Frequency:
It has one script which inputs the acummulated inductor losses from inductor_design/main.py and calculates the total mosfet and diode losses. The script then calculates the optimal frequency for a range of cable types
To run the mosfet and diode loss script:

    Under frequency
  
    run frequency_choice.m 
    
    
