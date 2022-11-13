from django.shortcuts import render
from radiosense.Sensitivity import Sensitivity
from radiosense.PlotParams import PlotParams

# Create your views here.
def home(request):
    return render(request, "params.html")

# Computes the sensitivity and makes plots
def sensitivity(request):
    gain = request.POST['gain']
    Tobs = request.POST['tobs']
    SNR = request.POST['snr']
    Trec = request.POST['trec']
    bw = request.POST['bw']
    fcen = request.POST['fcen']
    tscatter = request.POST['tscatter']
    galcon = request.POST["galcon"]


    fluxcalc = Sensitivity.Sensitivity(float(gain), float(bw), float(Trec), int(galcon), float(fcen), float(SNR))
    fluxcalc.getflux(float(tscatter), float(Tobs))

    # Make the plot and save it to the html file
    plotter = PlotParams.PlotParams()
    plotter.makesenseplots(fluxcalc.periods, fluxcalc.dcs, fluxcalc.fluxlims, fluxcalc.fcen)
    return render(request, "radiosenseresults.html")


# Computes the observing time and make plots
def observtime(request):
    gain = request.POST['gain']
    SNR = request.POST['snr']
    Trec = request.POST['trec']
    bw = request.POST['bw']
    fcen = request.POST['fcen']
    fluxlim = request.POST['fluxlim']
    tscatter = request.POST['tscatter']
    galcon = request.POST["galcon"]

    fluxcalc = Sensitivity.Sensitivity(float(gain), float(bw), float(Trec), int(galcon), float(fcen), float(SNR))
    fluxcalc.getTobs(float(fluxlim), float(tscatter))

    # Make the plot and save it to the html file
    plotter = PlotParams.PlotParams()
    plotter.makeobsplots(fluxcalc.periods, fluxcalc.dcs, fluxcalc.Tobserves, fluxcalc.fcen)
    return render(request, "radiosenseresults.html")


