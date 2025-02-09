import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator
import styles
from importdata import getValues

runNo = 423433#427885

def main():
    # Import and clean data
    cpmEta, cpmPhi, cpmVal, efxEta, efxPhi, efxVal, r2 = getValues(runNo)
    # Categorise events
    central = []
    margins = []
    for i in range(len(cpmEta)):
        if cpmEta[i] < -6 or cpmEta[i] > 5:
            margins.append(i)
        else:
            central.append(i)
    # Convert energy units
    finalCpmVal = cpmVal*.025
    finalEfxVal = efxVal*.025
    # Set up figure and axes
    f = plt.figure()
    ax = f.add_axes([0.09, .1, .92, .85])
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    #  Define binning
    xmax=65
    div=1
    x_bins = np.linspace(0, xmax, div*xmax+1)
    y_bins = np.linspace(0, xmax, div*xmax+1)
    #  Plot 2D histogram and colour bar
    plt.hist2d(matched(finalCpmVal,r2), matched(finalEfxVal,r2), bins=[x_bins, y_bins], norm=colors.LogNorm(), cmap=plt.cm.gnuplot2, snap=True, edgecolors=None)
    cbar = plt.colorbar(pad=0.01)
    # Adjust labels, limits, padding, tick marks
    ax.set_xlim(0,xmax)
    ax.set_ylim(0,xmax)
    ax.plot([0, xmax],[0, xmax],'--',color='lime')
    ax.set_xlabel(r"CPM Energy [GeV]", ha='right', x=1.00)
    ax.set_ylabel(r"eFEX Energy [GeV]", ha='right', y=1.00)
    cbar.ax.set_ylabel(r"TOB/RoI matches / GeV$^2$", ha='left', y=1.00, rotation=270, labelpad=16)
    # Annotate plot
    plt.text(0.06, 0.950, f'Run {runNo}, '+r'$\mathsf{\sqrt{s} =} 13.6$ TeV', transform=ax.transAxes, horizontalalignment='left', verticalalignment='top')
    plt.text(0.06, 0.895, r"$\mathsf{\eta}$-$\mathsf{\phi}$ matched TOBs/RoIs", transform=ax.transAxes, horizontalalignment='left', verticalalignment='top')
    # Save to file
    plt.savefig(f'plots/matcheshist_{runNo}.pdf')
    plt.savefig(f'plots/matcheshist_{runNo}.png',dpi=200) #alternate format

def matched( inputList, r2 ):
    return [ inputList[i] for i in range(len(inputList)) if r2[i] < 3]

if __name__ == "__main__":
    main()
