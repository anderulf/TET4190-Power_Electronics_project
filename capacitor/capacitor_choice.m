clear all
clc

# ---------------------------
# All values are taken from the capacitor datasheets. Assumption: 400V values used as these are assumed to be more or 
# less equal to the 385V values. 
# ---------------------------

% Needed capacitance for ripple requirement
capacitance_goal = 2.2*10^-3;

% Aluminum Electrolytic Capacitors Radial Miniature, High Voltage (notation: radial)
capacitance_radial = [2.2, 4.7, 4.7, 6.8, 10, 21.99, 22, 33, 47, 68, 100];
tand = 0.15;
capacitance_radial = capacitance_radial *10^-6;
equivalent_series_resistance_radial = tand/(2*3.14159 * 100) ./capacitance_radial;
capacitors_radial = ceil(capacitance_goal ./ capacitance_radial);

% Aluminum Electrolytic Capacitors, Power High Ripple Current Snap-In (notation:ripple)
capacitance_ripple = [56, 68, 100, 120, 120,150, 150,180, 180, 180, 220.01, 220.01, 220.01, 270, 270, 330, 330, 390, 390, 470, 560, 680];
equivalent_series_resistance_ripple = [918, 762, 520, 433, 438, 348, 351, 293, 305, 327, 241, 250, 259, 205, 222, 169, 181, 145, 154, 129, 110, 91];
capacitance_ripple = capacitance_ripple .* 10^-6
equivalent_series_resistance_ripple = equivalent_series_resistance_ripple .* 10^-3;
capacitors_ripple = ceil(capacitance_goal ./ capacitance_ripple)

% Aluminum Electrolytic Capacitors Power Ultra Miniature Snap-In (notation: ultra)
capacitance_ultra = [68, 82, 100, 120, 150, 150, 180, 180, 220.01, 220.01, 220.01, 270, 270, 270, 330, 330, 390, 390, 470, 470, 560, 680, 820];
equivalent_series_resistance_ultra = [1400, 1250, 1125, 990, 750, 750, 630, 630, 520, 520, 520, 430, 430, 430, 350, 350, 300, 300, 250, 250, 210, 190, 155];
capacitance_ultra = capacitance_ultra .* 10^-6;
equivalent_series_resistance_ultra = equivalent_series_resistance_ultra .* 10^-3;
capacitors_ultra = ceil(capacitance_goal ./ capacitance_ultra);

% Currents 
I_drms = 13.6; # Average diode current at full load
I_out = 10; # Average output current at full load

% Calculate capacitor current
I_c_tot = sqrt(I_drms^2-I_out^2);

% Calculate branch currents 
I_c_ultra = I_c_tot ./ capacitors_ultra;
I_c_ripple = I_c_tot ./ capacitors_ripple;
I_c_radial = I_c_tot ./ capacitors_radial;

% Calculate losses
losses_ultra = I_c_ultra.^2 .* equivalent_series_resistance_ultra .* capacitors_ultra
losses_ripple = I_c_ripple.^2 .* equivalent_series_resistance_ripple .* capacitors_ripple
losses_radial = I_c_radial.^2 .* equivalent_series_resistance_radial .* capacitors_radial

% Get minimum values
[minimum_ultra, i_ultra] = min(losses_ultra);
[minimum_ripple, i_ripple] = min(losses_ripple);
[minimum_radial, i_radial] = min(losses_radial);
disp('Lowest value for ultra, ripple, radial):')
disp('Ultra:')
disp(minimum_ultra)
disp('Ripple:')
disp(minimum_ripple)
disp('Radial: ')
disp(minimum_radial)
disp('Best capacitance value for ripple capacitor: ')
disp(ceil(capacitance_ripple(i_ripple)*1000000))
disp('Number of capacitors in series:')
disp(capacitors_ripple(i_ripple))
