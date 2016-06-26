# Testing GitHub Branching
# Delta-V Calculator - GUI Version

from tkinter import *
from tkinter import ttk
import math

#Define Rocket Class - Starting as just a list of stages.
class rocket(object):
    def __init__(self):
        self.stages = []
    # Calculate and Return Total Delta-V
    def delta_v(self):
        total = 0
        # print(total)
        for stages in self.stages:
            # print(stages.delta_v())
            total = total + stages.delta_v()
            # print(total)
        return total
           
#Define Stage Class
class stage(object):
    def __init__(self, mass, fuel_type, fuel_vol, ox_vol, Isp, thrust=0):
        #self.name = name
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
    def TWR(self):
        twr = self.thrust / (self.mass_full*9.82)
        return twr


# Function for "New Rocket" button
def new():
    for i in range(0,numStages):
        stagelist[i].configure(state="disabled")
        dvlist[i].configure(text="")
        editlist[i].configure(state="disabled")
    # for child in results.winfo_children():
    #     child.configure(state="disabled")
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
	for child in entry.winfo_children():
		child.configure(state="normal")
			child.configure(state="normal")
    
# Function for "Done" button
def done(*args):
    newstage = stage(float(mass_var.get()),type_var.get(),int(fuel_var.get()),int(ox_var.get()),int(isp_var.get()))
    if len(newrocket.stages) >= stagenum:
        newrocket.stages[stagenum-1] = newstage
    else:
        newrocket.stages.append(newstage)
    try:
        stage_dv = int(newstage.delta_v())
        dvlist[stagenum-1].configure(text=str(stage_dv))
        rocket_dv = int(newrocket.delta_v())
        dv_sum.configure(text=str(rocket_dv))
        mass_ent.delete(0, 'end')
        fuel_ent.delete(0, 'end')
        ox_ent.delete(0, 'end')
        isp_ent.delete(0, 'end')
    except ValueError:
        pass
    stagelist[stagenum].config(state="normal")
    editlist[stagenum].config(state="normal")
    for child in entry.winfo_children():
        child.configure(state="disabled")
    # dvsum = int(newrocket.delta_v())
    # print(dvsum)
    # newrocket.delta_v()
        
root = Tk()
root.title("KSP Delta-V Calculator")

# Define Frame Components
content = ttk.Frame(root)
results = ttk.Frame(content, borderwidth=5, relief="sunken")
entry = ttk.Frame(content)

# Variable definitions and intial values
mass_var = StringVar()
type_var = IntVar()
fuel_var = StringVar()
ox_var = StringVar()
isp_var = StringVar()
newrocket = rocket()
stagenum = -1
stagelist = []
dvlist = []
editlist = []
numStages = 5


# Define Widgets
#
#
# Results Frame
dv_lbl = ttk.Label(results, text="Delta-V", font="helvetica 8 bold")

for i in range(1,numStages+1):
    stagename = "Stage " + str(i)
    newstage = ttk.Label(results, text=stagename, state="disabled")
    stagelist.append(newstage)
    dvlist.append(ttk.Label(results, text=""))
    editlist.append(ttk.Button(results, text="Edit", state="disabled", command= lambda i=i: edit(i)))
total_lbl = ttk.Label(results, text="Total DV:")
dv_sum = ttk.Label(results, text="")

# Entry Frame
StageNum_lbl = ttk.Label(entry, text="Stage:", state="disabled")
mass_lbl = ttk.Label(entry, text="Mass", state="disabled")
FuelType_lbl = ttk.Label(entry, text="Fuel Type", state="disabled")
FuelVol_lbl = ttk.Label(entry, text="Fuel Vol", state="disabled")
OxVol_lbl = ttk.Label(entry, text="Oxidizer", state="disabled")
isp_lbl = ttk.Label(entry, text="Isp", state="disabled")

mass_ent = ttk.Entry(entry, textvariable=mass_var, width=8, state="disabled")
typeL_ent = Radiobutton(entry, text="Liquid", variable=type_var, value=0, state="disabled")
typeS_ent = Radiobutton(entry, text="Solid", variable=type_var, value=1, state="disabled")
fuel_ent = ttk.Entry(entry, textvariable=fuel_var, width=8, state="disabled")
ox_ent = ttk.Entry(entry, textvariable=ox_var, width=8, state="disabled")
isp_ent = ttk.Entry(entry, textvariable=isp_var, width=8, state="disabled")

done_butt = ttk.Button(entry, text="Done", width=8, state="disabled", command=done)

#Content Frame New Rocket Button
new_butt = ttk.Button(content, text="New Rocket", command=new)


# Place Widgets on Grid
#
#
content.grid(column=0, row=0)
# Results Frame
results.grid(column=0, row=0, columnspan=4, rowspan=9, padx=10, pady=10)
dv_lbl.grid(column=1, row=0, padx=6)

for i in range(0,numStages):
    rownum = i + 1
    stagelist[i].grid(column=0, row=rownum, padx=6)
    dvlist[i].grid(column=1, row=rownum)
    editlist[i].grid(column=3, row=rownum, padx=6, pady=3)
total_lbl.grid(column=0)
dv_sum.grid(column=1, row=rownum+1)

# Entry Frame
entry.grid(column=4, row=0, pady=10)

StageNum_lbl.grid(column=0, row=0, padx=6, pady=3, sticky=E)
mass_lbl.grid(column=0, row=2, padx=6, pady=3, sticky=E)
FuelType_lbl.grid(column=0, row=3, padx=6, pady=3, sticky=E)
FuelVol_lbl.grid(column=0, row=5, padx=6, pady=3, sticky=E)
OxVol_lbl.grid(column=0, row=6, padx=6, pady=3, sticky=E)
isp_lbl.grid(column=0, row=7, padx=6, pady=3, sticky=E)

mass_ent.grid(column=1, row=2, padx=6, pady=3, sticky=EW)
typeL_ent.grid(column=1, row=3, sticky=W)
typeS_ent.grid(column=1, row=4, sticky=W)
fuel_ent.grid(column=1, row=5, padx=6, pady=3, sticky=EW)
ox_ent.grid(column=1, row=6, padx=6, pady=3, sticky=EW)
isp_ent.grid(column=1, row=7, padx=6, pady=3, sticky=EW)
done_butt.grid(column=1, row=8)

# Content Frame
new_butt.grid(column=0, row=9, pady=6)

# Mainloop
root.mainloop()
