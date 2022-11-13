# A class that plots the various parameters that are computed from the Sensitivity module
#Uses Plotly so they can be embedded in the Web application

import plotly
import plotly.graph_objects as go
import numpy as np
import psrqpy

class PlotParams:
    """
    A class that defines the plotting module for this exercise.
    Also uses psrqpy internally to save the pulsar parameters
    """
    def __init__(self):
        """
        Constructor for the class
        Parameters:
        """
        try:
            # Generate pulsar data
            query = psrqpy.QueryATNF(params=["P0", "S1400"])
            mask = query["S1400"].mask
            self.periods = query["P0"][np.invert(mask)]
            self.s1400 = query["S1400"][np.invert(mask)]
        except:
            raise ValueError("Error parsing arguments")


    def makesenseplots(self, periods, dcs, fluxlims, fcen):

        fluxes = self.s1400*pow(fcen/1400, -1.6)/1000.0  # From Jankowski et al. 2017
        # A plot of survey flux limits
        fig = go.Figure()

        for i in range(len(dcs)):
            fig.add_trace(go.Scatter(x=periods, y=fluxlims[:,i], mode="lines", name="Duty cycle: "+str(dcs[i])))

        fig.add_trace(go.Scatter(x=self.periods, y=fluxes, mode="markers", name="ATNF pulsars"))
        fig.update_layout(hovermode="y")
        fig.update_layout(title="Flux limit as a function of pulse period")
        fig.update_xaxes(type="log", title_text="Period (s)")
        fig.update_yaxes(type="log", title_text="Flux (Jy)")
        # Save the figure as an html
        plotly.offline.plot(fig,filename='/Users/rajwade/Work/Projects/django_test_project/public/radiosenseresults.html',config={'displayModeBar': False})

    def makeobsplots(self, periods, dcs, tobs, fcen):
        #scale the pulsar fluxes
        fluxes = self.s1400*pow(fcen/1400, -1.6)/1000.0  # From Jankowski et al. 2017
        # A plot of survey flux limits
        fig = go.Figure()

        for i in range(len(dcs)):
            fig.add_trace(go.Scatter(x=periods, y=tobs[:,i], mode="lines", name="Duty cycle: "+str(dcs[i])))


        fig.update_layout(hovermode="y")
        fig.update_layout(title="Observing time as a function of pulse period for a given flux limit")
        fig.update_xaxes(type="log", title_text="Period (s)")
        fig.update_yaxes(type="log", title_text="Observing Time (s)")
        # Save the figure as an html
        plotly.offline.plot(fig,filename='/Users/rajwade/Work/Projects/django_test_project/public/radiosenseresults.html',config={'displayModeBar': False})
