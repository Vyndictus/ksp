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
	def __init__(self, mass, fuel_type, fuel_vol, ox_vol, Isp, thrust=0):
		self.mass_full = mass
		self.fuel_type = fuel_type
		self.fuel_vol = fuel_vol
		self.ox_vol = ox_vol
		self.Isp = Isp
		self.thrust = thrust
	#Returns Mass of the Fuel
	def mass_fuel(self):
		if self.fuel_type == 1:
			mass = self.fuel_vol * .0075
		else:
			mass = (self.fuel_vol+self.ox_vol) * .005
		return mass
	#Returns Delta-V for the stage
	def delta_v(self):
		self.dv = math.log(self.mass_full/(self.mass_full-self.mass_fuel()))*self.Isp*9.81
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

# Function for "New Rocket" button
def new():
	clear_stage()
	for i in range(0,NUM_STAGES):
		stagelist[i].configure(state="disabled")
		dvlist[i].configure(text="")
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
			child.configure(state="normal")
	clear_stage()
	if len(newrocket.stages) >= stagenum: #If Stage exists, populate with existing values
		mass_var.set(newrocket.stages[stagenum-1].mass_full)
		type_var.set(newrocket.stages[stagenum-1].fuel_type)
		fuel_var.set(newrocket.stages[stagenum-1].fuel_vol)
		ox_var.set(newrocket.stages[stagenum-1].ox_vol)
		isp_var.set(newrocket.stages[stagenum-1].Isp)
	
	StageNum_lbl.configure(state="normal")
	mass_lbl.configure(state="normal")
	
# Function for "Done" button
def done(*args):
	newstage = Stage(float(mass_var.get()),type_var.get(),int(fuel_var.get()),int(ox_var.get()),int(isp_var.get()))
	if len(newrocket.stages) >= stagenum:
		newrocket.stages[stagenum-1] = newstage
	else:
		newrocket.stages.append(newstage)
	try:
		stage_dv = int(newstage.delta_v())
		dvlist[stagenum-1].configure(text=str(stage_dv))
		rocket_dv = int(newrocket.delta_v())
		dv_sum.configure(text=str(rocket_dv))
		clear_stage()
	except ValueError:
		pass
	stagelist[stagenum].config(state="normal")
	editlist[stagenum].config(state="normal")
	for child in entry.winfo_children():
		child.configure(state="disabled")


# Tkinter Layout Element Definitions
# Set up root and master frames to hold the notebook			
root = Tk()
root.title("KSP Delta-V Calculator")
# Define notebook object
nb = ttk.Notebook(root)
nb.pack(fill=BOTH, padx=2, pady=3)
# Define content frames and add as tabs in the notebook "nb"
dv_content = ttk.Frame(nb)
twr_content = ttk.Frame(nb)
nb.add(dv_content, underline=0, text='Delta-V')
nb.add(twr_content, underline=0, text='Thrust')
# Enable keyboard traversal of tabs
nb.enable_traversal()

# Define Frame Components on the Delta-V Tab
results = ttk.Frame(dv_content, borderwidth=5, relief="sunken")
entry = ttk.Frame(dv_content)
# Define Frame components on the Thrust tab
thrust_main = ttk.Frame(twr_content)
ascent_frame = ttk.Frame(twr_content)
orbit_frame = ttk.Frame(twr_content)

# Variable definitions and intial values
# Tkinter entry variables
mass_var = StringVar()
type_var = IntVar()
fuel_var = StringVar()
ox_var = StringVar()
isp_var = StringVar()
thrust_var = StringVar()
use_var = IntVar()
thrust_condition_var = IntVar()
ascent_mass_var = StringVar()
#instatiate rocket object
newrocket = Rocket()
#initial value settings for global variables and lists/dictionaries
stagenum = -1
stagelist = []
dvlist = []
editlist = []
twr_accel_list = []
#setting global constants
NUM_STAGES = 5


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
	editlist.append(ttk.Button(results, text="Edit", state="disabled", command= lambda i=i: edit(i)))
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
# Entry fields/Radio Buttons/Button
mass_ent = ttk.Entry(entry, textvariable=mass_var, width=8, state="disabled")
typeL_ent = ttk.Radiobutton(entry, text="Liquid", variable=type_var, value=0, state="disabled")
typeS_ent = ttk.Radiobutton(entry, text="Solid", variable=type_var, value=1, state="disabled")
fuel_ent = ttk.Entry(entry, textvariable=fuel_var, width=8, state="disabled")
ox_ent = ttk.Entry(entry, textvariable=ox_var, width=8, state="disabled")
isp_ent = ttk.Entry(entry, textvariable=isp_var, width=8, state="disabled")
thrust_ent = ttk.Entry(entry, textvariable=thrust_var, width=8, state="disabled")
done_butt = ttk.Button(entry, text="Done", width=8, state="disabled", command=done)
#dv_content Frame New Rocket Button on Delta-V Tab
new_butt = ttk.Button(dv_content, text="New Rocket", command=new)
#
# Widgets for Thrust tab
# Labels
condition_lbl = ttk.Label(thrust_main, text="Stage Engine Use:")
thrust_mass_lbl = ttk.Label(thrust_main, text="Mass")
# Entry widgets 
cond_ascent_ent = ttk.Radiobutton(thrust_main, text="Ascent", variable=thrust_condition_var, value=0)
cond_orbit_ent = ttk.Radiobutton(thrust_main, text="Orbital", variable=thrust_condition_var, value=1)
thrust_mass_ent = ttk.Entry(thrust_main, textvariable=ascent_mass_var, width=8)
#

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
# Grid the entry widgets in entry frame
mass_ent.grid(column=1, row=2, padx=6, pady=3, sticky=EW)
typeL_ent.grid(column=1, row=3, sticky=W)
typeS_ent.grid(column=1, row=4, sticky=W)
fuel_ent.grid(column=1, row=5, padx=6, pady=3, sticky=EW)
ox_ent.grid(column=1, row=6, padx=6, pady=3, sticky=EW)
isp_ent.grid(column=1, row=7, padx=6, pady=3, sticky=EW)
thrust_ent.grid(column=3, row=2, padx=6, pady=3, sticky=EW)
done_butt.grid(column=1, row=8)
# Gris New Rocket button in dv_content frame
new_butt.grid(column=0, row=9, pady=6)
#
# Thrust Tab
thrust_main.grid(column=0, row=0) # Grids the thrust_main frame within twr_content 
# Grid label and entry widgets in thrust_main frame
condition_lbl.grid(column=0, row=0, columnspan=2, padx=6, pady=3, sticky=EW)
cond_ascent_ent.grid(column=0, row=1, columnspan=2, padx=6)
cond_orbit_ent.grid(column=0, row=2, columnspan=2, padx=6)
thrust_mass_lbl.grid(column=0, row=3, padx=6, pady=3, sticky=E)
thrust_mass_ent.grid(column=1, row=3, padx=6, pady=3)
# Ascent Entry Frame
# ascent_frame.grid(column=3, row=0, pady=3) # Grids the ascent entry frame to the righ of the condition choice
# thrust_mass_lbl.grid(column=0, row=0, padx=6, pady=3)
# thrust_mass_ent.grid(column=1, row=0, padx=6, pady=3)

# Mainloop
root.mainloop()
