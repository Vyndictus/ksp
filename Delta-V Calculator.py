# Delta-V Calculator - GUI Version

from tkinter import *
from tkinter import ttk
import math

#Define Rocket Class - Starting as just a list of stages.
class Rocket(object):
	def __init__(self):
		self.stages = []
	# Calculate and Return Total Delta-V
	def delta_v(self):
		total = 0
		for stages in self.stages:
			total = total + stages.delta_v()
		return total
		   
#Define Stage Class
class Stage(object):
	def __init__(self, mass, fuel_type, fuel_vol, ox_vol, Isp, purpose, 
				thrust, gravity=1):
		self.mass_full = mass
		self.fuel_type = fuel_type
		self.fuel_vol = fuel_vol
		self.ox_vol = ox_vol
		self.Isp = Isp
		self.thrust = thrust
		self.purpose = purpose
		self.gravity = gravity
	#Returns Mass of the Fuel
	def mass_fuel(self):
		if self.fuel_type == 1:
			mass = self.fuel_vol * .0075
		else:
			mass = (self.fuel_vol+self.ox_vol) * .005
		return mass
	#Returns Delta-V for the stage
	def delta_v(self):
		self.dv = math.log(self.mass_full/(self.mass_full
							-self.mass_fuel()))*self.Isp*9.81
		return self.dv
	#Returns the Trust to Weight Ratio for the stage
	def twr(self, const):
		twr = self.thrust / (self.mass_full*const)
		return twr

# Function for clearing stage entry value variable
def clear_stage():
	mass_ent.delete(0, 'end')
	fuel_ent.delete(0, 'end')
	ox_ent.delete(0, 'end')
	isp_ent.delete(0, 'end')
	thrust_ent.delete(0, 'end')
	type_var.set(0)
	purpose_var.set(0)
	planet_var.set("Choose...")

# Function for "New Rocket" button
def new():
	clear_stage()
	for i in range(0,NUM_STAGES):
		stagelist[i].configure(state="disabled")
		dvlist[i].configure(text="")
		twr_accel_list[i].configure(text="")
		editlist[i].configure(state="disabled")
	for child in entry.winfo_children():
		child.configure(state="disabled")
	stagelist[0].config(state="normal")
	editlist[0].config(state="normal")
	dv_sum.configure(text="")
	del newrocket.stages[:]

# Function for "Edit" button
def edit(stage):
	global stagenum
	stagenum=int(stage)
	for child in entry.winfo_children(): #If new stage - just enable all widgets
			if child not in [planet_lbl, planet_ent]:
				child.configure(state="normal")
	clear_stage()
	if len(newrocket.stages) >= stagenum: #If Stage exists, populate with existing values
		mass_var.set(newrocket.stages[stagenum-1].mass_full)
		type_var.set(newrocket.stages[stagenum-1].fuel_type)
		fuel_var.set(newrocket.stages[stagenum-1].fuel_vol)
		ox_var.set(newrocket.stages[stagenum-1].ox_vol)
		isp_var.set(newrocket.stages[stagenum-1].Isp)
		thrust_var.set(newrocket.stages[stagenum-1].thrust)
		purpose_var.set(newrocket.stages[stagenum-1].purpose)
	StageNum_lbl.configure(state="normal")
	mass_lbl.configure(state="normal")
	
# Function for "Done" button
def done(*args):
	newstage = Stage(float(mass_var.get()),type_var.get(),int(fuel_var.get()),
					int(ox_var.get()),int(isp_var.get()), purpose_var.get(),
					int(thrust_var.get()), float(GRAV_DICT[planet_var.get()]))
	if len(newrocket.stages) >= stagenum:
		newrocket.stages[stagenum-1] = newstage
	else:
		newrocket.stages.append(newstage)
	try:
		stage_dv = int(newstage.delta_v())
		dvlist[stagenum-1].configure(text=str(stage_dv))
		stage_twr = float(newstage.twr(newstage.gravity))
		if newstage.gravity == 1:
			twr_accel_list[stagenum-1].configure(text=str(int(stage_twr))+"m/s")
		else:
			twr_accel_list[stagenum-1].configure(text=str(round(stage_twr, 2)))
		rocket_dv = int(newrocket.delta_v())
		dv_sum.configure(text=str(rocket_dv))
		clear_stage()
	except ValueError:
		pass
	stagelist[stagenum].config(state="normal")
	editlist[stagenum].config(state="normal")
	for child in entry.winfo_children():
		child.configure(state="disabled")

def enable_disable_planet():
	if purpose_var.get() == 1:
		planet_lbl.configure(state="normal")
		planet_ent.configure(state="normal")
	else:
		planet_lbl.configure(state="disabled")
		planet_ent.configure(state="disabled")
	
# Tkinter Layout Element Definitions
# Set up root and master frames to hold the notebook			
root = Tk()
root.title("KSP Toolkit")
dv_content = ttk.Frame(root)
dv_content.pack(fill=BOTH, padx=3, pady=3)
results = ttk.Frame(dv_content, borderwidth=5, relief="sunken")
entry = ttk.Frame(dv_content)

# Variable definitions and intial values
# Define Tkinter entry variables
mass_var = StringVar()
type_var = IntVar()
fuel_var = StringVar()
ox_var = StringVar()
isp_var = StringVar()
thrust_var = StringVar()
purpose_var = IntVar()
use_var = IntVar()
planet_var = StringVar()
thrust_condition_var = IntVar()
ascent_mass_var = StringVar()
# instatiate objects
newrocket = Rocket()
# initialize global variables and dynamic lists
stagenum = -1
stagelist = []
dvlist = []
editlist = []
twr_accel_list = []
# set global constants, tuples, and static dictionaries
NUM_STAGES = 5
PLANET_LIST = ('Choose...', 'Moho', 'Eve', 'Gilly', 'Kerbin', 'Mun', 'Minmus', 'Duna',
				'Ike', 'Dres', 'Jool', 'Laythe', 'Vall', 'Tylo', 'Bop',
				'Pol', 'Eeloo')
GRAV_DICT = {'Choose...':1, 'Moho':2.7, 'Eve':16.7, 'Gilly':0.049, 'Kerbin':9.81, 'Mun':1.63, 'Minmus':0.49, 'Duna':2.94,
				'Ike':1.1, 'Dres':1.13, 'Jool':7.85, 'Laythe':7.85, 'Vall':2.31, 'Tylo':7.85, 'Bop':0.589,
				'Pol':0.373, 'Eeloo':1.69}


# Define Widgets
#
# Widgets for Delta-V Tab
# Results Frame on Delta-V Tab
dv_lbl = ttk.Label(results, text="Delta-V", font="helvetica 8 bold")
twr_lbl = ttk.Label(results, text="TWR/Accel", font="helvetica 8 bold")
for i in range(1,NUM_STAGES+1):
	stagename = "Stage " + str(i)
	newstage = ttk.Label(results, text=stagename, state="disabled")
	stagelist.append(newstage)
	dvlist.append(ttk.Label(results, text=""))
	twr_accel_list.append(ttk.Label(results, text=""))
	editlist.append(ttk.Button(results, text="Edit", state="disabled", 
					command= lambda i=i: edit(i)))
total_lbl = ttk.Label(results, text="Total DV:")
dv_sum = ttk.Label(results, text="")
# Entry Frame on Delta-V Tab
# Labels
StageNum_lbl = ttk.Label(entry, text="Stage:", state="disabled")
mass_lbl = ttk.Label(entry, text="Mass", state="disabled")
FuelType_lbl = ttk.Label(entry, text="Fuel Type", state="disabled")
FuelVol_lbl = ttk.Label(entry, text="Fuel Vol", state="disabled")
OxVol_lbl = ttk.Label(entry, text="Oxidizer", state="disabled")
isp_lbl = ttk.Label(entry, text="Isp", state="disabled")
thrust_lbl = ttk.Label(entry, text="Thrust (kN)", state="disabled")
purpose_lbl = ttk.Label(entry, text="Purpose", state="disabled")
planet_lbl = ttk.Label(entry, text="Planet", state="disabled")
# Entry fields/Radio Buttons/Button
mass_ent = ttk.Entry(entry, textvariable=mass_var, width=8, state="disabled")
typeL_ent = ttk.Radiobutton(entry, text="Liquid", variable=type_var, value=0, state="disabled")
typeS_ent = ttk.Radiobutton(entry, text="Solid", variable=type_var, value=1, state="disabled")
fuel_ent = ttk.Entry(entry, textvariable=fuel_var, width=8, state="disabled")
ox_ent = ttk.Entry(entry, textvariable=ox_var, width=8, state="disabled")
isp_ent = ttk.Entry(entry, textvariable=isp_var, width=8, state="disabled")
thrust_ent = ttk.Entry(entry, textvariable=thrust_var, width=8, state="disabled")

planet_ent = ttk.OptionMenu(entry, planet_var, *PLANET_LIST)

purpose_o_ent = ttk.Radiobutton(entry, text="Orbital Maneuver", 
								variable=purpose_var, value=0, state="disabled",
								command= lambda: enable_disable_planet())
purpose_a_ent = ttk.Radiobutton(entry, text="Ascent/Lander", 
								variable=purpose_var, value=1, state="disabled",
								command= lambda: enable_disable_planet())
planet_ent.configure(state="disabled")
done_butt = ttk.Button(entry, text="Done", width=8, state="disabled", command=done)
#dv_content Frame New Rocket Button on Delta-V Tab
new_butt = ttk.Button(dv_content, text="New Rocket", command=new)


# Place Widgets on Grid
#
# Delta-V Tab
# Results Frame
results.grid(column=0, row=0, columnspan=4, rowspan=9, padx=10, pady=10) #Grids the results frame within dv_content
dv_lbl.grid(column=1, row=0, padx=6)
twr_lbl.grid(column=2, row=0, padx=6)
for i in range(0,NUM_STAGES):
	rownum = i + 1
	stagelist[i].grid(column=0, row=rownum, padx=6)
	dvlist[i].grid(column=1, row=rownum)
	twr_accel_list[i].grid(column=2, row=rownum)
	editlist[i].grid(column=3, row=rownum, padx=6, pady=3)
total_lbl.grid(column=0)
dv_sum.grid(column=1, row=rownum+1)
# Entry Frame
entry.grid(column=4, row=0, pady=10) # Grids the entry fram within dv_content
# Grid the label widgets in entry frame
StageNum_lbl.grid(column=0, row=0, padx=6, pady=3, sticky=E)
mass_lbl.grid(column=0, row=2, padx=6, pady=3, sticky=E)
FuelType_lbl.grid(column=0, row=3, padx=6, pady=3, sticky=E)
FuelVol_lbl.grid(column=0, row=5, padx=6, pady=3, sticky=E)
OxVol_lbl.grid(column=0, row=6, padx=6, pady=3, sticky=E)
isp_lbl.grid(column=0, row=7, padx=6, pady=3, sticky=E)
thrust_lbl.grid(column=2, row=2, padx=6, pady=3, sticky=E)
purpose_lbl.grid(column=2, row=3, padx=6, pady=3, sticky=E)
planet_lbl.grid(column=2, row=5, padx=6, pady=3, sticky=E)
# Grid the entry widgets in entry frame
mass_ent.grid(column=1, row=2, padx=6, pady=3, sticky=EW)
typeL_ent.grid(column=1, row=3, sticky=W)
typeS_ent.grid(column=1, row=4, sticky=W)
fuel_ent.grid(column=1, row=5, padx=6, pady=3, sticky=EW)
ox_ent.grid(column=1, row=6, padx=6, pady=3, sticky=EW)
isp_ent.grid(column=1, row=7, padx=6, pady=3, sticky=EW)
thrust_ent.grid(column=3, row=2, padx=6, pady=3, sticky=W)
purpose_o_ent.grid(column=3, row=3, padx=6, pady=3, sticky=EW)
purpose_a_ent.grid(column=3, row=4, padx=6, pady=3, sticky=EW)
planet_ent.grid(column=3, row=5, padx=0, pady=3, sticky=W)
done_butt.grid(column=1, row=8)
# Grid New Rocket button in dv_content frame
new_butt.grid(column=0, row=9, pady=6)

# Mainloop
root.mainloop()
