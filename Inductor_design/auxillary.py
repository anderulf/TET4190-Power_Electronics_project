import cmath

class Inductor_design():
    """
    This class holds the data for the general system and should treat the iterative process isolated so that
    the main algorithm can treat this class as a black box
    """
    def __init__(self,a_initial, a_step, a_max, inductance_goal, copper_fill_factor, current_density_rms, flux_density_peak, mass_density_core, mass_density_copper):
        self.air_permability = 1.25663706212*10**-6 # equal to vaccum
        # Set from input data
        self.a_step = a_step
        self.a_max = a_max
        self.inductance_goal = inductance_goal
        self.copper_fill_factor = copper_fill_factor
        self.current_density_rms = current_density_rms
        self.flux_density_peak = flux_density_peak
        self.mass_density_core = mass_density_core
        self.mass_density_copper = mass_density_copper
        # Create core object
        self.core = Core(a_initial)
        # Initialize variables
        self.inductance = 0
        self.inductance_max = 0
        self.frequency = 0
        self.flux_density_ac = 0
        self.specific_winding_loss = 0
        self.specific_core_loss = 0
        self.number_of_airgaps = 0
        self.accumulated_airgap_length = 0
        self.number_of_turns = 0
        self.number_of_turns_max = 0
        self.A_cu = 0
        self.core_loss = 0
        self.winding_loss = 0
        self.total_loss = 0
        self.core_weight = 0
        self.winding_weight = 0
        self.total_weight = 0

    def calculate_inductance_requirement(self):
        """
        Eq 18-18 in book. the required coil inductance is frequency dependant in order to meet the ripple requirement
        of the task (1A)
        """
        self.inductance_goal = 385/4 /self.frequency

    def increment_a(self):
        if self.core.a + self.a_step <= self.a_max:
            self.core.a += self.a_step
            return True
        return False

    def calculate_specific_winding_loss(self):
        """
        Winding losses in W/m^3 from equation 30-12a. Multiplied with 1000 because formula is in mW/cm^3
        """
        self.specific_winding_loss = 22*self.copper_fill_factor*(self.current_density_rms*10**-6)**2*1000

    def calculate_specific_core_loss(self):
        """
        Core losses in W/m^3 from equation 30-2a (converted due to units) multiplied with 1000 to convert to W/m^3
        """
        self.specific_core_loss = 1.5*10**-6*(self.frequency/1000)**1.3*(self.flux_density_ac*1000)**2.5*1000

    def calculate_flux_density_ac(self):
        """
        From equation 30-27
        """
        self.flux_density_ac = self.flux_density_peak * (self.I_peak - self.I_dc) / self.I_peak

    def calculate_inductance(self):
        """
        The inductane from the current dimensions and properties are calculated using equation 30-28 but with current
        number of turns (todo: verify)
        """

        self.inductance = self.copper_fill_factor * self.current_density_rms * self.flux_density_peak * self.core.A_w * self.core.A_core/(self.I_peak*self.I_rms)
        #self.inductance = self.number_of_turns * self.core.A_core * self.flux_density_peak / self.I_peak

    def calculate_inductance_max(self):
        """
        Calculate the highest possible inductance based on the current core design from eq 30-28
        """
        self.inductance_max = self.number_of_turns_max*self.core.A_core*self.flux_density_peak/self.I_peak

    def calculate_cable_area(self):
        """

        """
        self.A_cu = self.I_rms/self.current_density_rms

    def calculate_current_density(self):
        """

        """
        self.current_density_rms = self.I_rms/self.A_cu

    def calculate_stored_energy(self):
        """
        Stored energy in the coil calculated from equation 30-23 (left)
        """
        self.stored_energy = self.inductance * self.I_peak * self.I_rms

    def not_enough_energy(self):
        """
        Compare stored energy requirement with possible energy in core
        """
        return self.stored_energy > self.copper_fill_factor * self.current_density_rms * self.flux_density_peak * self.core.A_w * self.core.A_core

    def inductance_insufficient(self):
        """
        Compares the inductance of the current with the inductance goal and returns True if the difference between them
        is smaller than the set error
        """
        return (self.inductance - self.inductance_goal) < 0

    def inductance_unrealistic(self):
        """
        Checks if the inductance is smaller than the maximal inductance for the current design
        """
        return self.inductance_goal > self.inductance

    def calculate_efficient_number_of_airgaps(self):
        """
        Calculates Ng. The double E core has three air gaps but with different sizes so in effect is should be close to
        two airgaps. However, due to fringing this isn't exactly true
        """
        self.number_of_airgaps = 2

    def calculate_maxmium_number_of_turns(self):
        """
        The physical maximum number of turns possible for the given design. Note that this will return a float. Found from eq 30-9

        """
        self.number_of_turns_max = self.copper_fill_factor*self.core.A_w/self.A_cu

    def calculate_accumulated_airgap_length(self):
        """
        Calculating the airgap length from equation 30-33
        """
        self.accumulated_airgap_length = self.core.A_core / ((self.core.A_core * self.flux_density_peak / (self.air_permability * self.number_of_turns * self.I_peak)) - ((self.core.a + self.core.d) / self.number_of_airgaps))

    def overdimensioned(self):
        if self.inductance > self.inductance_goal:
            return True
        return False

    def calculate_losses(self):
        # Calculates the losses and returns the sum
        self.core_loss = self.specific_core_loss * self.core.core_volume
        self.winding_loss = self.specific_winding_loss * self.core.winding_volume
        self.total_loss = self.core_loss + self.winding_loss

    def calculate_weights(self):
        self.core_weight = self.core.core_volume * self.mass_density_core
        self.winding_weight = self.core.winding_volume * self.mass_density_copper
        self.total_weight = self.core_weight + self.winding_weight

    def __str__(self):
        """
        Defines how the object is serialized into a string
        """
        core_loss = self.specific_core_loss* self.core.core_volume
        winding_loss = self.specific_winding_loss*self.core.winding_volume
        s = "Inductor parameters:\n" \
            "Inductance={} mH, goal={} mH. Maximum possible for current design={} mH\n" \
            "{} distributed airgaps with length: {} cm, number of turns: {}\n" \
            "Cable cross section area: {} mm2\n" \
            "Verification of turns: the ratio between the winding area and the area utilized by the cable is {}%\n" \
            "Specific losses: specific core loss: {} W/m3, specifid winding loss: {} W/m3\n" \
            "Losses: winding loss: {} W, core loss: {} W, total losses: {} W\n" \
            "Weight: winding weight: {} kg, copper weight: {} kg, total weight: {} kg".format(round(1000*self.inductance,3), round(1000*self.inductance_goal,3), round(1000*self.inductance_max,3), self.number_of_airgaps, round(100 * self.accumulated_airgap_length/self.number_of_airgaps, 3), self.number_of_turns, round(self.A_cu * 1000 ** 2, 3), round((self.A_cu/self.copper_fill_factor*self.number_of_turns)/self.core.A_core*100,3), round(self.specific_core_loss,3) , round(self.specific_winding_loss,3) ,round(winding_loss, 3), round(core_loss, 3), round(winding_loss + core_loss, 3), round(self.winding_weight, 3), round(self.core_weight, 3), round(self.winding_weight + self.core_weight, 3))
        return s


class Core():
    """
    This class holds the data for the core
    - Dimensions
    - Airgaps
    ..
    """
    def __init__(self, a_initial):
        """
        Initialize the core object for a because all other values are optimized for ratios of it
        """

        self.a = a_initial
        # Initialize dimension parameters
        self.b_a = 0                                # space between E arms
        self.d = 0                                  # depht of E arms
        self.h_a = 0                                # height of bobbin slot
        self.b_w = 0                                # bobbin width
        self.h_w = 0                                # bobbin height h_w = 2a
        self.A_core = 0                             # Core area A_core = a * d
        self.A_w = 0                                # Winding area A_w = h_w * b_w (cross section of winding area in bobbin)
        # Calculate dimensions based on initial a
        self.calculate_dimensions()

    def calculate_dimensions(self):
        """
        Calculate optimized double E core dimensions from current value of a (ref. table 30-1 and ch. 30-1-5)
        """
        self.b_a = self.a
        self.d = 1.5 * self.a
        self.h_a = 2.5 * self.a
        self.b_w = 0.7 * self.a
        self.h_w = 2 * self.a
        self.A_core = 1.5 * self.a**2
        self.A_w = 1.4 * self.a**2
        self.core_volume = 13.5*self.a**3
        self.winding_volume = 12.3*self.a**3

    def __str__(self):
        """
        Defines how the object is serialized to a string
        """
        s = "Core dimensions:\na = {} cm, b_a = {} cm, d = {} cm, h_a = {} cm\nb_w = {} cm, h_w = {} cm, A_core = {} cm2, A_w = {} cm2,\nCore volume= {} cm3, winding volume = {} cm3".format(
            round(100*self.a,3), round(100*self.b_a,3), round(100*self.d,3), round(100*self.h_a,3), round(100*self.b_w,3), round(100*self.h_w,3), round(100**2*self.A_core, 3), round(100**2*self.A_w,3), round(100**3*self.core_volume, 3), round(100**3*self.winding_volume,3))
        return s