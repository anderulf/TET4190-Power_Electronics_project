%% Common constans
Vd=230*0.9;
V0=385;

D=1-(Vd/V0); %Duty cycle
I_D_avg=10; %average load current


%%Mosfet
r_mosfet=0.08757; %Sic 


I_L_avg=(I_D_avg*0.81)/(1-D);

I_L_rms=I_L_avg/0.9;

I_mos_rms=I_L_rms*sqrt(1-(1-D)*(1/0.81));

P_on_mos=I_mos_rms^2*r_mosfet;

disp(P_on_mos)

%%Diode Si
r_on_diode=0.08180; %Si
V_f=0.365; %Si

I_D_rms=I_L_rms*sqrt((1-D)*(1/0.81));

P_on_diode=V_f*I_D_avg+r_on_diode*I_D_rms^2;

fprintf('Diode Si: %d \n',P_on_diode);

%%Diode Si
r_on_diode=0.08180; %Si
V_f=0.365; %Si

I_D_rms=I_L_rms*sqrt((1-D)*(1/0.81));

P_on_diode=V_f*I_D_avg+r_on_diode*I_D_rms^2;


