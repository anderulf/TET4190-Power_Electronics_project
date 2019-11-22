## -------------------------
# Script written to find the best mostfet and diode combination
# --------------------------

%% Common constans
Vd=230*0.9; # rectified voltage
V0=385; # output voltage

D=1-(Vd/V0); %Duty cycle
I_D_avg=4; %average load current (within operation range 2A - 7A)
total_losses=zeros(133,5);
P_on_mos_sic=zeros(133,1);
P_on_mos_si=zeros(133,1);
P_on_diode_si=zeros(133,1);
P_on_diode_sic=zeros(133,1);
counter=1;

%For I_rms_MOSFET=3.8824 from LTSpice (turn off + turn on losses)
E_sl_sic_sic=14.94+27.418-7.6926+7.8167;
E_sl_sic_si=20.343+65.103-1.1574+1.3006;
E_sl_si_sic=9.3704+23.055-7.6568+7.9277;
E_sl_si_si=16.163+56.22-1.1508+1.4246;

for fs=18000:1000:150000
    
    P_sl_sic_sic=E_sl_sic_sic*10^(-6)*fs;
    P_sl_sic_si=E_sl_sic_si*10^(-6)*fs; 
    P_sl_si_sic=E_sl_si_sic*10^(-6)*fs;
    P_sl_si_si=E_sl_si_si*10^(-6)*fs;

    %%MOSFET Sic
    r_mosfet_sic=0.0875673907; 

    I_L_avg_sic=(I_D_avg*0.81)/(1-D);

    I_L_rms_sic=I_L_avg_sic/0.9;

    I_mos_rms_sic=I_L_rms_sic*sqrt(1-(1-D)*(1/0.81));

    P_on_mos_sic(counter)=I_mos_rms_sic^2*r_mosfet_sic;


    %%MOSFET Si
    r_mosfet_si=0.1912125876;  
    
    I_L_avg=(I_D_avg*0.81)/(1-D);
    
    I_L_rms=I_L_avg/0.9;
    
    I_mos_rms_si=I_L_rms*sqrt(1-(1-D)*(1/0.81));
    
    P_on_mos_si(counter)=I_mos_rms_si^2*r_mosfet_si;
    
    
    %%Diode Si
    r_on_diode_si=0.08180391719; %Si
    V_f_si=0.365; %Si

    I_D_rms_si=I_L_rms*sqrt((1-D)*(1/0.81));

    P_on_diode_si(counter)=V_f_si*I_D_avg+r_on_diode_si*I_D_rms_si^2;



    %%Diode Sic
    r_on_diode_sic=0.03585; %Si
    V_f_sic=0.8081; %Si
    
    I_D_rms_sic=I_L_rms*sqrt((1-D)*(1/0.81));
    
    P_on_diode_sic(counter)=V_f_sic*I_D_avg+r_on_diode_sic*I_D_rms_sic^2;
    %---------------------------------------------------------------------%
    %Total losses
    
    P_tot_sic_sic=P_sl_sic_sic+P_on_mos_sic(counter)+P_on_diode_sic(counter);
    P_tot_sic_si=P_sl_sic_si+P_on_mos_sic(counter)+P_on_diode_si(counter);
    P_tot_si_sic=P_sl_si_sic+P_on_mos_si(counter)+P_on_diode_sic(counter);
    P_tot_si_si=P_sl_si_si+P_on_mos_si(counter)+P_on_diode_si(counter);
    p_tot=[P_tot_sic_sic P_tot_sic_si P_tot_si_sic P_tot_si_si];
    
    total_losses(counter,1)=fs/1000; 
    total_losses(counter,2:end)=p_tot; 
    counter=counter+1; 
end
disp('-----------------------------------------------------------------')
fprintf('fs[kHz]    M=Sic,D=Sic    M=Sic,D=Si    M=Si,D=Sic    M=Si,D=Si\n')
disp('-----------------------------------------------------------------')
for i=1:length(total_losses)
fprintf('%d           %.4f         %.4f        %.4f       %.4f\n',total_losses(i,1),total_losses(i,2),total_losses(i,3),total_losses(i,4),total_losses(i,5))
end
%disp(total_losses)
