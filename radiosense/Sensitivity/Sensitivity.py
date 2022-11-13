# A class to compute the sensitivity of a given survey to pulsars and FRBs
# Takes in a set of parameters of the survey
# Can account for the added system temperature due to the Galaxy
import numpy as np

class Sensitivity:

    def __init__(self, G, BW, Trec, Galcon, fcen, snr):
        """
        Constructor for the Sensitivity class
        Parameters:
        G (float) :  Gain of the telescope in K Jy^-1
        BW (float):  Bandwidth of the receiver in Hz
        Trec (float):  Receiver temperature in K
        Galcon (bool): Compute Galactic contribution at a given frequency
        Tobs (float):  Observing time in seconds
        fcen (float): Centre Frequency in MHz
        snr (float):  signal to noise ratio
        """
        try:
            self.G = float(G) # K Jy^-1
            self.bw = float(BW) # Hertz
            self.Trec = float(Trec)
            self.Galcon = int(Galcon) # Should be 0 or 1
            self._fcen = float(fcen) # MHz
            self.snr = float(snr)
            self._periods = np.arange(0.001, 50, 0.1)
            self._dcs = np.array([0.005, 0.01, 0.05, 0.07, 0.1])
            self._fluxlims = np.zeros((len(self._periods), len(self._dcs)))
            self._Tobserves = np.zeros((len(self._periods), len(self._dcs)))
            self._tscatter = np.arange(0.0001, 0.01, 0.0001) # for FRBs
            self._widths = np.zeros(len(self._tscatter)) # for FRBs
            #self._pfluxlims = np.zeros( len(self._tscatter),len(self._widths))  # for FRBs
            self.Tsys = 0.0

            #Get the system temperature
            Tgal = 5 # Typical galactic background contribution
            if(self.Galcon == 1):
                self.Tsys = self.Trec + 2.8 + Tgal*pow(self._fcen/1400, -2.86)
            else:
                self.Tsys = self.Trec + 2.8

        except:
            raise ValueError("Error in parsing values")
            exit()

    def getflux(self, tscat, tobs):
        """
        Get the flux limit for various duty cycles and periods
        """

        try:
            for i in range(len(self._dcs)):
                widths = np.sqrt(pow(self._dcs[i]* self._periods,2.0) + pow(tscat, 2.0))
                A = (self.snr * self.Tsys)/(self.G*np.sqrt(2.0 * self.bw * tobs))
                B = np.sqrt((widths/self._periods)/(1-(widths/self._periods)))
                self._fluxlims[:,i] = A*B
        except:
            raise ArithmeticError("Error in calculations")

    """
    # A method for FRBs (single pulse search)
    def getpflux(self):

        try:
            width = np.arange(0.0001, 0.01, 0.0001)
            for i in range(len(widths)):
                self._widths[i] = np.sqrt(pow(width[i] ,2.0) + pow(self._tscatter, 2.0))
                self._pfluxlims[:,i] = (self.snr * self.Tsys)/(self.G*np.sqrt(2.0 * self.bw * self._widths[i]))
        except:
            raise ArithmeticError("Error in calculations")
    """

    def getTobs(self, fluxlim, tscat):
        """
        Get the observing time for a given flux limit
        Parameters:
        fluxlim (float):  Flux limit in Jy
        """
        try:

            for i in range(len(self._dcs)):
                widths = np.sqrt(pow(self._dcs[i] *self._periods,2.0)  + pow(tscat, 2.0))
                A = pow(fluxlim*self.G/self.Tsys/self.snr,2.0) * 2.0*self.bw
                B = (1-(widths/self._periods))/(widths/self._periods)
                self._Tobserves[:,i] = 1/(A*B)
        except:
            raise ArithmeticError("Error in calculations")

    # Define all the getters for the class

    @property
    def fluxlims(self):
        return self._fluxlims

    @property
    def Tobserves(self):
        return self._Tobserves

    @property
    def periods(self):
        return self._periods

    @property
    def dcs(self):
        return self._dcs

    @property
    def fcen(self):
        return self._fcen

    @property
    def frbwidths(self):
        return self._widths
