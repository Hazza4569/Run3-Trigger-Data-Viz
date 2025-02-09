import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.patches import Patch
import styles
from importdata import getValues

runNo = 423433#427885
efxBase = True # else use cpm base
# Binning and ranges:
ymax = 150
nbins = 5
eMin = 0
eMax = 100 

def main():
    # Import and clean data
    cpmEta, cpmPhi, cpmVal, efxEta, efxPhi, efxVal, r2 = getValues(runNo)
    # Define binning
    binWidth = (eMax-eMin)/(nbins)
    bin_edges = np.linspace(eMin,eMax,nbins+1)
    bin_centres = [ (a+b)/2 for a,b in zip(bin_edges[:-1], bin_edges[1:]) ]
    reference_energy = (efxVal if efxBase else cpmVal)*0.025
    energy_indices = np.digitize(reference_energy, bin_edges)
    # ^ gives ROOT-like bin indices
    # ( 0 = underflow, 1 -> nbins = bins, nbins+1 = overflow )
    # Count matches and total events per bin
    matched = np.zeros(nbins)
    total = np.zeros(nbins)
    for i_r2, energy_bin in zip(r2, energy_indices):
        if energy_bin < 1: continue
        out_bin = energy_bin - (1 if energy_bin < nbins+1 else 2)
        # ^ subtract 1 to correct to 0-indexed.
        #   subtract 2 if overflow to include in last bin.
        # Add event to counters
        matched[out_bin] += i_r2 < 3
        total[out_bin] += 1
    # Calculate efficiencies and uncertainties
    percent, errors = 100*np.array([
        [match/tot, np.sqrt(match)/tot] if tot > 0 else [0,0]
        for match,tot in zip(matched,total)
    ]).transpose()
    # Set up figure and axes
    f = plt.figure()
    ax = f.add_axes([0.09, .1, .86, .85])
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    # Custom error bars
    x_fill = [ edge for edge in bin_edges for i in range(2) ][1:-1]
    y_fill = np.array([
        [p-e, p+e] for p,e in zip(percent, errors) for i in range(2)
    ]).transpose()
    # ^ `for i in range(2)` gives 2 of each value in the list.
    #   x values are then shifted, so that at each bin edge it steps
    #   between y values at the same x
    ax.fill_between(
        x_fill, y_fill[0], y_fill[1],
        zorder=1,# hatch='/////',
        alpha=0.7,
        facecolor='#2C74BC', linewidth=0
    )
    # Patches and legend
    error_patch = Patch(
        #hatch='/////',
        alpha=0.7,
        facecolor='#2C74BC', linewidth=0
        #facecolor='white',
        #edgecolor='#2C74BC', linewidth=0
    )
    bar_patch = ax.bar(
        bin_centres, percent, color='red',
        #yerr=errors, # < draw default error bars
        width=binWidth, zorder=0
    )
    plt.legend(
        [bar_patch, error_patch], ['Match rate', 'Stat. uncertainty'],
        framealpha=0, fontsize=13,
        bbox_to_anchor=(.78,.785, .2, .2),
        handleheight=2
    )
    # Axis labels
    ax.set_xlabel(
        ('eFEX' if efxBase else 'CPM') + r' Energy [GeV]',
        ha='right', x=.99
    )
    ax.set_ylabel(
        f"% matched with {'CPM RoIs' if efxBase else 'eFEX TOBs'}",
        ha='right', y=.99
    )
    ax.set_ylim(0,ymax)
    # Set last label to represent overflow
    labels = [ '100+' if l == 100 else f'{l:.0f}' for l in bin_edges ]
    ax.set_xticklabels(labels)
    # Annotate plot
    plt.text(
        0.04, 0.950, f'Run {runNo}, '+r'$\mathsf{\sqrt{s} =} 13.6$ TeV',
        transform=ax.transAxes, horizontalalignment='left', verticalalignment='top',
        fontsize=13
    )
    plt.text(
        0.04, 0.895, f"Match rate for {'eFEX TOBs' if efxBase else 'CPM RoIs'}",
        transform=ax.transAxes, horizontalalignment='left', verticalalignment='top',
        fontsize=13
    )
    # Save to file
    plt.savefig(f"plots/matchrate_{runNo}_{'eFEX' if efxBase else 'CPM'}.pdf")
    plt.savefig(f"plots/matchrate_{runNo}_{'eFEX' if efxBase else 'CPM'}.png",dpi=200)

if __name__ == "__main__":
    main()
