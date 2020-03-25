import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os
import tweepy


FIG_SIZE = (7, 4.5)


def new_fig_ax():
    f = plt.figure(figsize=FIG_SIZE)
    a = f.add_subplot(111)
    return f, a

def do_plots(stats):
	f1, ax1 = new_fig_ax()
	f2, ax2 = new_fig_ax()
	f3, ax3 = new_fig_ax()
	f4, ax4 = new_fig_ax()
	f5, ax5 = new_fig_ax()
	f6, ax6 = new_fig_ax()
	f7, ax7 = new_fig_ax()

	ax1.legend(bbox_to_anchor=(1.01, 1))
	ax1.set_yscale('log')
	ax1.set_ylim(10, )
	ax1.set_title('Confirmed cases')
	plt.sca(ax1)
	ax1.grid(which='both', axis='both')
	plt.xticks(rotation=90)
	f1.tight_layout()

	ax2.legend(bbox_to_anchor=(1.01, 1))
	ax2.set_ylim(0, 15)
	ax2.set_title('Confirmed cases doubling times / days')
	plt.sca(ax2)
	#ax2.set_yscale('log')
	ax2.set_ylim(1, 15)
	ax2.grid(which='both', axis='both')
	plt.xticks(rotation=90)
	f2.tight_layout()

	ax3.legend(bbox_to_anchor=(1.01, 1))
	ax3.set_title('Days to get to n cases')
	ax3.set_xlabel('Number of cases')
	ax3.set_xscale('log')
	ax3.set_ylim(1, 100)
	ax3.set_yscale('log')
	ax3.grid(which='both', axis='both')
	f3.tight_layout()

	ax4.legend(bbox_to_anchor=(1.01, 1))
	ax4.set_title('Death rates / %')
	ax4.set_ylim(.1, 20)
	ax4.set_yscale('log')
	ax4.grid(which='both', axis='both')
	plt.sca(ax4)
	plt.xticks(rotation=90)
	f4.tight_layout()

	ax5.legend(bbox_to_anchor=(1.01, 1))
	ax5.set_yscale('log')
	ax5.set_ylim(MIN_DEATHS, )
	ax5.set_title('Deaths')
	ax5.grid(which='both', axis='both')
	plt.sca(ax5)
	plt.xticks(rotation=90)
	f5.tight_layout()

	ax6.legend(bbox_to_anchor=(1.01, 1))
	ax6.set_ylim(0, 15)
	ax6.set_title('Deaths doubling times / days')
	plt.sca(ax6)
	#ax2.set_yscale('log')
	ax6.set_ylim(1, 15)
	ax6.grid(which='both', axis='both')
	plt.xticks(rotation=90)
	f6.tight_layout()

	ax7.legend(bbox_to_anchor=(1.01, 1))
	ax7.set_title('Days to get to n deaths')
	ax7.set_xlabel('Number of deaths')
	ax7.set_xscale('log')
	ax7.set_ylim(1, 100)
	ax7.set_yscale('log')
	ax7.grid(which='both', axis='both')
	f7.tight_layout()
	
	f1.savefig('confirmed.png')
	f2.savefig('confirmed_doubling_times.png')
	f3.savefig('confirmed_days_to_n.png')
	f4.savefig('death_rate.png')
	f5.savefig('deaths.png')
	f6.savefig('deaths_doubling_times.png')
	f7.savefig('deaths_days_to_n.png')
