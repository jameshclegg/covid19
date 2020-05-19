import matplotlib.pyplot as plt
import numpy as np
import datetime
import os

FIG_SIZE = (7, 4.5)
MIN_DEATHS = 5

def new_fig_ax():
    f = plt.figure(figsize=FIG_SIZE)
    a = f.add_subplot(111)
    return f, a

def get_days_to_n(n_current, counts, doubling_time):
	# counts is a numpy array of numbers of cases you want to
	# project out to
	
	factor_to_go = counts / n_current 
	n_doublings = np.log(factor_to_go)/np.log(2)
	
	n_doublings[n_doublings<0] = 0

	days_to_go = n_doublings*doubling_time
	
	return days_to_go
        
def plot(data):
	
	n_cases_proj = np.logspace(3, np.log10(3e6), 45)
	n_deaths_proj = 0.05 * n_cases_proj
	
	def plot_triplet(dates, cases_or_deaths, window, n_proj, limit, axA, axB, axC):	
		axA.plot_date(dates, cases_or_deaths, '.', label=c)

		t_dbl = data.get_doubling_times(cases_or_deaths, limit)
		axB.plot_date(dates[window:], t_dbl, '-', label=c)
		
		d = get_days_to_n(cases_or_deaths[-1], n_proj, t_dbl[-1])
		axC.plot(n_proj, d, label=c)
	
	f1, ax1 = new_fig_ax()
	f2, ax2 = new_fig_ax()
	f3, ax3 = new_fig_ax()
	f4, ax4 = new_fig_ax()
	f5, ax5 = new_fig_ax()
	f6, ax6 = new_fig_ax()
	f7, ax7 = new_fig_ax()
		
	print('Starting to plot...')
	# loop over countries
	for c in data.confirmed_cases:
		plot_triplet(data.dates, data.confirmed_cases[c], 
					 data.window, n_cases_proj, 50,
					 ax1, ax2, ax3)
			
		plot_triplet(data.dates, data.deaths[c], 
					 data.window, n_deaths_proj, 5,
					 ax5, ax6, ax7)
		
		# plot the death rate
		ax4.plot_date(data.dates, data.get_death_rate(c)*100, '-', label=c)
	
	print('Formatting plots...')
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
	
	print('Saving to disk...')
	folder_name = datetime.datetime.now().strftime('%Y-%m-%d')
	
	if os.path.isdir(folder_name):
		files = os.listdir(folder_name)
		for f in files:
			os.remove(os.path.join(folder_name, f))
	else:
		os.mkdir(folder_name)
	
	def save_fig(f, name):
		f.savefig(os.path.join(folder_name, name))
	
	save_fig(f1, 'confirmed.png')
	save_fig(f2, 'confirmed_doubling_times.png')
	save_fig(f3, 'confirmed_days_to_n.png')
	save_fig(f4, 'death_rate.png')
	save_fig(f5, 'deaths.png')
	save_fig(f6, 'deaths_doubling_times.png')
	save_fig(f7, 'deaths_days_to_n.png')
	
	return folder_name
