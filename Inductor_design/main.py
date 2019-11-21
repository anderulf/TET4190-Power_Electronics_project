from auxillary import Inductor_design
import math
import pandas as pd
"""
For each frequency and current density calculate the ideal inductor design with the minimum losses.
The minimum losses are acquired for the smalles inductor because the losses are volume dependant.
The losses accumulated 20%-70% losses are then stored and analyzed in another script together with the 
diode and mosfet losses to find the optimal frequency.

Running the script for frequency = 53kHz and J_rms = 2A/mm2 will give the found design. 

The script creates an inductor design object from auxillary.py to store information about the inductor

Inductor currents at different load currents 
2A - 3.3478A
3A - 5.0217A
4A - 6.6957A
5A - 8.3696A
6A - 10.0435A
7A - 11.7174A

Version 2.0 
    Optimizes for 20%-70% instead of 100% 
"""


"""
Settings
"""
a_initial = 0.005 #m
a_step = 0.00001 #m
a_max = 0.1 #m
frequency_start = 53000 # Hz
frequency_step = 1000 # Hz
frequency_stop = 54000 # Hz
J_rms_start = 2*10**6 # A/m2
J_rms_step = 1*10**6 # A/m2
J_rms_stop = 3*10**6 # A/m2

"""
Input data
"""
copper_fill_factor = 0.3 # litz cable
flux_density_peak = 0.325 #T

mass_density_copper = 8960 #kg/m3 from https://www.rsc.org/
mass_density_core = 4750 #kg/m3 from 3F3 datasheet

"""
Program
Start with a small a and check if this a gives a sufficient maximum inductance > target. If it does not,
skip it, if it does calculate all required values. Now stop iterating because increasing a further will increase
losses as the volume increases. 
"""

sys = Inductor_design(a_initial, a_step, a_max,
                          copper_fill_factor, flux_density_peak, mass_density_core, mass_density_copper)
losses = {} # dictionary to hold loss data
# Lists sent to matlab for plotting total losses with DIODE and MOSFET aswell
losses_arry = []
frequency_arry = []
iteration = 0

losses_at_less_than_peak_load = []

for frequency in range(frequency_start, frequency_stop, frequency_step):
    # Set the frequency
    sys.frequency = frequency
    # Calculate the needed inductance as this is frequency dependant
    sys.calculate_inductance_requirement()
    for current_density_rms in range(J_rms_start, J_rms_stop, J_rms_step):
        # Append an empty element in the list
        losses_at_less_than_peak_load.append(0)
        # Set coil current to maximum load (10 A)
        sys.I_rms = 16.7391 * (2 ** 0.5)
        sys.I_peak = sys.I_rms + 1
        sys.I_dc = sys.I_rms
        # Set the current density
        sys.current_density_rms = current_density_rms
        # Set the flux density
        sys.calculate_flux_density_ac()
        # Find the specific losses
        sys.calculate_specific_core_loss()
        sys.calculate_specific_winding_loss()
        # Get the cable area
        sys.calculate_cable_area()
        converged = False
        sys.core.a = a_initial
        # Increment a until the maximum value is reached
        while sys.increment_a():
            # Calculate the dimensions
            sys.core.calculate_dimensions()
            sys.calculate_maxmium_number_of_turns()
            sys.calculate_inductance_max()
            # The maximum number of turns is a float, so floor it to get the physical value
            sys.number_of_turns = math.floor(sys.number_of_turns_max)
            # Calculate the new inductance from decreasing the number of turns slightly
            sys.calculate_inductance()
            # Check if this a gives an acceptable inductance according to the error limit
            sys.calculate_stored_energy()
            # Gjør en sjekk på stored energy! kcuJrmsbAwAco > LII
            if sys.inductance_insufficient() or sys.not_enough_energy():
                pass
            else:
                # It converged so calculate the inductor parameters given the current design
                sys.calculate_efficient_number_of_airgaps()
                sys.calculate_accumulated_airgap_length()
                sys.calculate_losses()
                sys.calculate_weights()
                converged = True
                break
        # Iteration completed - perform post processing
        if converged:
            print("*----Iteration completed---*")
            print("Iteration number: {}".format(iteration))
            print("Frequency: {} Hz, J_rms: {} A/mm^2".format(frequency, sys.current_density_rms*10**-6))
            print(sys)
            print(sys.core)
            losses[iteration] = sys.total_loss
            losses_arry.append(sys.total_loss)
            frequency_arry.append(sys.frequency)
            print("\nTotal losses for each iteration so far")
            print(losses)
            print("\n")
            print("-- Inductor performance at different loads --")
            # Calculate losses for different loads
            load_currents = [2, 3, 4, 5, 6, 7]
            for load_current in load_currents:
                # Get the inductor current
                if load_current == 2:
                    sys.I_rms = 3.3478 * (2 ** 0.5)  # A at load: 2 A
                elif load_current == 3:
                    sys.I_rms = 5.0217 * (2 ** 0.5)  # A at load: 3 A
                elif load_current == 4:
                    sys.I_rms = 6.6957 * (2 ** 0.5)  # A at load: 4 A
                elif load_current == 5:
                    sys.I_rms = 8.3696 * (2 ** 0.5)  # A at load: 5 A
                elif load_current == 6:
                    sys.I_rms = 10.0435 * (2 ** 0.5)  # A at load: 6 A
                elif load_current == 7:
                    sys.I_rms = 11.7174 * (2 ** 0.5)  # A at load: 7 A
                elif load_current == 10:
                    sys.I_rms = 16.7391 * (2 ** 0.5) # A at load: 10 A
                # Get the peak and the dc component of the inductor current
                sys.I_peak = sys.I_rms + 1
                sys.I_dc = sys.I_rms
                # Get the new current density for the given cable thickness
                sys.calculate_current_density()
                # Get the new flux density
                sys.calculate_flux_density_ac()
                # Get the new specific losses
                sys.calculate_specific_core_loss()
                sys.calculate_specific_winding_loss()
                sys.calculate_losses()
                print("**Load current: {} A".format(round(load_current,2)))
                print("     Sp. core loss:    {} W/m^3".format(round(sys.specific_core_loss, 5)))
                print("     Sp. Winding loss: {} W/m^3".format(round(sys.specific_winding_loss, 5)))
                print("     Core losses:      {} W".format(round(sys.core_loss,2)))
                print("     Winding losses:   {} W".format(round(sys.winding_loss,2)))
                print("     Total losses:     {} W".format(round(sys.total_loss, 2)))
                losses_at_less_than_peak_load[iteration] += sys.total_loss


            iteration += 1


print("\n-- Post processing of results --")
print("Iteration {1} gave the lowest losses at: {0}W".format(round(min(losses.values()),3), min(losses, key=losses.get)))

print("For extraction to matlab. Verify that only one current density is used so that each frequency is represented only once")
print("Total losses at 10A:")
print(losses_arry)
print("Frequencies:")
print(frequency_arry)
print("Accumulated losses for all loads (2A, 3A,..,7A:")
print(losses_at_less_than_peak_load)
