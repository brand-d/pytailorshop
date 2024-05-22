from tkinter import Label, LabelFrame, StringVar, Button, Tk
from functools import partial
from typing import Callable
from tailorshop import Tailorshop
from ts_types import Controllable_Variables

action_variables : dict[str,StringVar] = {}
state_variables : dict[str,StringVar] = {}

""" Changes the number of workers (w50) and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_w50(inc : int) -> None:
    actions.set_workers50(actions.workers50 + inc)
    action_variables["workers50"].set(str(actions.workers50))

""" Changes the number of workers (w100) and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_w100(inc : int) -> None:
    actions.set_workers100(actions.workers100 + inc)
    action_variables["workers100"].set(str(actions.workers100))

""" Changes the number of machines (m50) and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_m50(inc : int) -> None:
    actions.set_machines50(actions.machines50 + inc)
    action_variables["machines50"].set(str(actions.machines50))

""" Changes the number of machines (m100) and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_m100(inc : int) -> None:
    actions.set_machines100(actions.machines100 + inc)
    action_variables["machines100"].set(str(actions.machines100))

""" Changes the worker salary and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_w_sal(inc : int) -> None:
    actions.set_workers_salary(actions.workers_salary + inc * 100)
    action_variables["workers_salary"].set(str(actions.workers_salary))

""" Changes the worker benefits and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_w_ben(inc : int) -> None:
    actions.set_worker_benefits(actions.worker_benefits + inc * 10)
    action_variables["workers_benefits"].set(str(actions.worker_benefits))

""" Changes the shirt price and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_shirt_price(inc : int) -> None:
    actions.set_shirt_price(actions.shirt_price + inc * 2)
    action_variables["shirt_price"].set(str(actions.shirt_price))

""" Changes the number of outlets and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_outlets(inc : int) -> None:
    actions.set_outlets(actions.outlets + inc)
    action_variables["outlets"].set(str(actions.outlets))

""" Changes the material order and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_material_order(inc : int) -> None:
    actions.set_material_order(actions.material_order + inc * 50)
    action_variables["material_order"].set(str(actions.material_order))

""" Changes the spending for maintenance and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_maintenance(inc : int) -> None:
    actions.set_machines_maintenance(actions.machines_maintenance + inc * 100)
    action_variables["maintenance"].set(str(actions.machines_maintenance))

""" Changes the money spent on advertising and updates the shown variable. 

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_advertising(inc : int) -> None:
    actions.set_advertising(actions.advertising + inc * 100)
    action_variables["advertising"].set(str(actions.advertising))

""" Changes the location and updates the shown variable. 
    In this case, the numeric value is used to find the correct string:
    0: Suburb, 1: City, 2: Inner City

    Parameters
    ----------

    inc : int
        Sign of the increment (1 for increment, -1 for decrement, 0 for update only).

    """
def change_location(inc : int) -> None:
    actions.set_location(actions.location + inc)
    action_variables["location"].set(["Suburb", "City", "Inner City"][actions.location])

""" Helper function to add widgets to the action frame.

    Parameters
    ----------

    action_frame : LabelFrame
        The LabelFrame instance to add widgets to.

    text : str
        Main text of the widget (i.e., name of the variable)
    
    key : str
        Key for retrieving the respective StringVar for updating values.

    init_val : {int, str}
        Initial value to show.
    
    command  : Callable
        Callback for the plus/minus buttons.
    
    row : int
        Row to place the widgets.

    """
def add_action_widgets(action_frame : LabelFrame, text : str, key : str, 
                       init_val : {int, str}, command : Callable, row : int) -> None:
    action_variables[key] = StringVar()
    action_variables[key].set(init_val)
    label = Label(action_frame, text=text)
    value = Label(action_frame, textvariable=action_variables[key], width=10)
    plus_btn = Button(action_frame, text="+", command=partial(command, 1), width=5)
    minus_btn = Button(action_frame, text="-", command=partial(command, -1), width=5)
    
    label.grid(row=row, column=0, sticky="w")
    value.grid(row=row, column=1, sticky="w")
    minus_btn.grid(row=row, column=2, sticky="w")
    plus_btn.grid(row=row, column=3, sticky="w")

""" Creates the content for the action LabelFrame.

    Parameters
    ----------

    action_frame : LabelFrame
        The LabelFrame instance to add widgets to.

    """
def create_action_frame(action_frame : LabelFrame) -> None:
    add_action_widgets(action_frame, "Workers (50):", "workers50", 
                       actions.workers50, change_w50, 0)
    add_action_widgets(action_frame, "Workers (100):", "workers100", 
                       actions.workers100, change_w100, 1)

    add_action_widgets(action_frame, "Worker Salary:", "workers_salary", 
                       actions.workers_salary, change_w_sal, 2)
    add_action_widgets(action_frame, "Worker Benefits:", "workers_benefits", 
                       actions.worker_benefits, change_w_ben, 3)
    
    add_action_widgets(action_frame, "Machines (50):", "machines50", 
                       actions.machines50, change_m50, 4)
    add_action_widgets(action_frame, "Machines (100):", "machines100", 
                       actions.machines100, change_m100, 5)
    add_action_widgets(action_frame, "Machines Maintenance:", "maintenance", 
                       actions.machines_maintenance, change_maintenance, 6)

    add_action_widgets(action_frame, "Material Order:", "material_order", 
                       actions.material_order, change_material_order, 7)

    add_action_widgets(action_frame, "Outlet Stores:", "outlets", 
                       actions.outlets, change_outlets, 8)
    add_action_widgets(action_frame, "Store Locations:", "location", 
                       actions.location, change_location, 9)
    change_location(0) # Used to convert the numeric into a text in the GUI

    add_action_widgets(action_frame, "Shirt Price:", "shirt_price", 
                       actions.shirt_price, change_shirt_price, 10)
    add_action_widgets(action_frame, "Advertising:", "advertising", 
                       actions.advertising, change_advertising, 11)

    action_frame.grid_columnconfigure(0, weight=10)
    action_frame.grid_columnconfigure(1, weight=3)
    action_frame.grid_columnconfigure(2, weight=1)
    action_frame.grid_columnconfigure(3, weight=1)

""" Helper function to add widgets to the observation frame.

    Parameters
    ----------

    observation_frame : LabelFrame
        The LabelFrame instance to add widgets to.

    text : str
        Main text of the widget (i.e., name of the variable)
    
    key : str
        Key for retrieving the respective StringVar for updating values.

    value : float
        Initial value to show.
    
    row : int
        Row to place the widgets.

    """
def add_observation_var_widget(observation_frame : LabelFrame, 
                               text : str, key : str, 
                               value : float, row : int) -> None:
    state_variables[key] = StringVar()
    state_variables[key].set(str(round(value)))
    label = Label(observation_frame, text=text)
    value = Label(observation_frame, textvariable=state_variables[key], width=10)
    label.grid(row=row, column=0, sticky="w")
    value.grid(row=row, column=1, sticky="w")

""" Creates the observation (stats) frame, where the derived variables are shown.

    Parameters
    ----------

    observation_frame : LabelFrame
        The LabelFrame instance to add widgets to.

    """
def create_observation_frame(observation_frame : LabelFrame) -> None:
    add_observation_var_widget(observation_frame, "Bank Account:", "bank_account", 
                               tailorshop.current_state.bank_account, 0)
    add_observation_var_widget(observation_frame, "Company Value:", "company_value", 
                               tailorshop.current_state.company_value, 1)
    add_observation_var_widget(observation_frame, "Shirt Sales:", "shirt_sales", 
                               tailorshop.current_state.shirt_sales, 2)
    add_observation_var_widget(observation_frame, "Shirt Stock:", "shirt_stock", 
                               tailorshop.current_state.shirt_stock, 3)
    add_observation_var_widget(observation_frame, "Material Price:", "material_price", 
                               tailorshop.current_state.material_price, 4)
    add_observation_var_widget(observation_frame, "Material Stock:", "material_stock", 
                               tailorshop.current_state.material_stock, 5)
    add_observation_var_widget(observation_frame, "Customer Interest:", "customer_interest", 
                               tailorshop.current_state.customer_interest, 6)
    add_observation_var_widget(observation_frame, "Production Idle:", "production_idle", 
                               tailorshop.current_state.production_idle, 7)
    add_observation_var_widget(observation_frame, "Machine Damage:", "damage", 
                               tailorshop.current_state.damage, 8)
    add_observation_var_widget(observation_frame, "Worker Satisfaction:", "worker_satisfaction", 
                               tailorshop.current_state.percent_worker_satisfaction, 9)

    observation_frame.grid_columnconfigure(0, weight=8)
    observation_frame.grid_columnconfigure(1, weight=3)

""" Updates the stats segments of the GUI.
    """
def update_information() -> None:
    state_variables["turn"].set(
        "Turn: {}".format(round(tailorshop.current_state.turn)))
    state_variables["bank_account"].set(
        str(round(tailorshop.current_state.bank_account)))
    state_variables["company_value"].set(
        str(round(tailorshop.current_state.company_value)))
    state_variables["shirt_sales"].set(
        str(round(tailorshop.current_state.shirt_sales)))
    state_variables["shirt_stock"].set(
        str(round(tailorshop.current_state.shirt_stock)))
    state_variables["material_price"].set(
        str(round(tailorshop.current_state.material_price)))
    state_variables["material_stock"].set(
        str(round(tailorshop.current_state.material_stock)))
    state_variables["customer_interest"].set(
        str(round(tailorshop.current_state.customer_interest)))
    state_variables["production_idle"].set(
        str(round(tailorshop.current_state.production_idle)))
    state_variables["damage"].set(
        str(round(tailorshop.current_state.damage)))
    state_variables["worker_satisfaction"].set(
        str(round(tailorshop.current_state.percent_worker_satisfaction)))
    if tailorshop.is_finished():
        state_variables["finished"].set("Finished!")
    else:
        state_variables["finished"].set("")

""" Resets the simulation and updates the GUI.

    """
def reset_simulation() -> None:
    tailorshop.reset()
    global actions
    actions = tailorshop.get_last_actions()

    # Since each variable in the GUI is updated when changed,
    # we use this to update the GUI when resetting.
    change_w50(0)
    change_w100(0)
    change_w_sal(0)
    change_w_ben(0)
    change_m100(0)
    change_m50(0)
    change_maintenance(0)
    change_material_order(0)
    change_outlets(0)
    change_location(0)
    change_advertising(0)
    change_shirt_price(0)

    # Update the stats segements
    update_information()

""" Advances the simulation by one step and updates the GUI..

    """
def next_step() -> None:
    tailorshop.do_next_step(actions)
    update_information()

""" Creates the simulation frame (footer), where controls and turn indicator is located.

    Parameters
    ----------

    simulation_footer : LabelFrame
        The LabelFrame instance to add widgets to.

    """
def create_simulation_bar(simulation_footer : LabelFrame) -> None:
    state_variables["turn"] = StringVar()
    state_variables["turn"].set(
        "Turn: {}".format(round(tailorshop.current_state.turn)))
    status_label = Label(simulation_footer, 
                         textvariable=state_variables["turn"], 
                         width=10)
    status_label.grid(row=0, column=0)

    state_variables["finished"] = StringVar()
    finished_label = Label(simulation_footer, 
                           textvariable=state_variables["finished"], 
                           width=10)
    finished_label.grid(row=0, column=1)

    next = Button(simulation_footer, text="Next Step", command=next_step, width=15)
    next.grid(row=1, column=0)

    reset = Button(simulation_footer, text="Reset", command=reset_simulation, width=15)
    reset.grid(row=1, column=1)

    simulation_footer.grid_rowconfigure(0, weight=2)
    simulation_footer.grid_rowconfigure(1, weight=1)

if __name__ == "__main__":
    # Instantiate tailorshop simulation
    tailorshop : Tailorshop = Tailorshop()
    actions : Controllable_Variables = tailorshop.get_last_actions()

    # Create window
    window = Tk()
    window.title("Tailorshop")
    window.geometry('500x450')

    # Create label frames for the sections
    action_frame = LabelFrame(window, text="Actions")
    observations_frame = LabelFrame(window, text="Stats")
    information_footer = LabelFrame(window, text="Simulation", height=50)

    # Place sections in grid
    action_frame.grid(row=0, column=0, sticky="nsew")
    observations_frame.grid(row=0, column=1, sticky="nsew")
    information_footer.grid(row=1, columnspan=2, sticky="nsew")

    # Balance grid
    window.grid_rowconfigure(0, weight=2)
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # Add content to frames
    create_action_frame(action_frame)
    create_observation_frame(observations_frame)
    create_simulation_bar(information_footer)

    # Enter window main loop
    window.mainloop()