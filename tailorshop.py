from __future__ import annotations
from ts_types import Tailorshop_State, Controllable_Variables
import numpy as np
from copy import copy

class Tailorshop:
    """ Main class for the Tailorshop simulation. 
    Instantiates the simulation and allows to update it with given actions.

    """
    positive_interest = 0.0025
    negative_interest = 0.0066
    max_machine_capacity = 50
    max_advertising_effect = 900
    max_worker_satisfaction = 1.7
    locations_rents = [500, 1000, 2000]
    outlet_rent = 500
    cash_injection = 0
    price_machine50 = 10000
    price_machine100 = 20000
    price_outlet = 10000

    """ Instantiates the Tailorshop simulation.

    Parameters
    ----------
    ts_state : Tailorshop_State
        The initial state or None. 
        When no state is given, default initialization values are used.

    initial_actions : Controllable_Variables
        The initial state of the controllable variables or None. 
        When no actions are given, default values are used.
    
    randomize : bool
        When set to true, the dynamic effects parameters are generated randomly.
        Otherwise, a fixed initialization is used.
    
    use_steps : bool
        If true, the controllable variables can only be changed using the default stepsize,
        and values not aligning with the stepsizes will be altered automatically.
        Otherwise, all values within min/max limits are allowed.

    """
    def __init__(self, ts_state : Tailorshop_State = None, 
                 initial_actions : Controllable_Variables = None, 
                 randomize : bool = False, use_steps : bool = True) -> None:
        # Initialize random variables
        self.rnd_machines_50 = [
            -1.6794734, 0.3962952, -1.2906776, -1.69717836, 
            0.6770368, 0.3517432, -1.5712524, 1.154388, 
            -0.5179668, 1.634584, -1.3330284, -0.9713408, 
            0.1261412, 0.8854424
        ]
        self.rnd_machines_100 = [
            -0.8060082, 1.3505922, -1.7557848, -2.44459788, 
            -1.0919448, -2.66181528, 0.2626608, -2.0520366, 
            1.4789304, -1.7724894, -1.1784876, 1.6133514, 
            0.6488046, 1.135758]
        self.rnd_customer_interest = [
            -23.04985, 19.2422, 34.44874, 19.7927,
            -24.671, 30.50709, -4.26652, 38.93418, 
            -12.88273, -47.064686, -13.75205, -49.315691, 
            25.20559, 30.6675
        ]
        self.rnd_material_price = [
            8.2671817, 4.8714296, 4.8530515, 5.9098319,
            5.18731075, 7.09909075, 6.772157, 7.6171843, 
            8.02385095, 2.6811532, 5.0227145, 6.29710125, 
            7.7631327, 2.51019404
        ]
        if randomize:
            # Adopted from Tobago by Holger Diedam, Michael Engelhart and Sebastian Sager
            # See https://sourceforge.net/projects/tobago/
            self.rnd_machines_50 = [
                4.0 * x - 2.0 for x in np.random.random(size=14)
            ]
            
            self.rnd_machines_100 = [
                6.0 * x - 3.0 for x in np.random.random(size=14)
            ]
            
            self.rnd_customer_interest = [
                100 * x - 50 for x in np.random.random(size=14)
            ]
            
            self.rnd_material_price = [
                2 + 6.5 * x for x in np.random.random(size=14)
            ]
        
        self.current_state = None
        if ts_state:
            self.current_state = Tailorshop_State.from_ts_state(ts_state)
        else:   
            self.current_state = Tailorshop_State()
        self.last_actions = None
        if initial_actions:
            self.last_actions = copy(initial_actions)
            self.last_actions.use_steps = use_steps
        else:
            self.last_actions = Controllable_Variables(use_steps=use_steps)
    
    """ Calculates the production capacity for 50-shirts-producing machines.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Capacity of the machines-50.

    """
    def _production_capacity_50(self, actions: Controllable_Variables, 
                                ts_state : Tailorshop_State) -> float:
        turn = ts_state.turn
        capacity_m50 = ts_state.machine_capacity + self.rnd_machines_50[turn -1]
        workers_m50 = min(actions.machines50, actions.workers50)
        satisfaction_effect = np.sqrt(np.abs(ts_state.worker_satisfaction))
        return workers_m50 * capacity_m50 * satisfaction_effect
    
    """ Calculates the production capacity for 100-shirts-producing machines.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Capacity of the machines-100.

    """
    def _production_capacity_100(self, actions: Controllable_Variables, 
                                 ts_state : Tailorshop_State) -> float:
        turn = ts_state.turn
        capacity_m100 = (2 * ts_state.machine_capacity) + self.rnd_machines_100[turn -1]
        workers_m100 = min(actions.machines100, actions.workers100)
        satisfaction_effect = np.sqrt(np.abs(ts_state.worker_satisfaction))
        return workers_m100 * capacity_m100 * satisfaction_effect

    """ Calculates the demand for shirts.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Demand for shirts.

    """
    def _shirts_demand(self, actions: Controllable_Variables, 
                       ts_state : Tailorshop_State) -> float:
        base_demand = (ts_state.customer_interest / 2) + 280
        demand_elasticity = (1.25 * np.power(2.7181, (-1 * (np.power(actions.shirt_price, 2)) / 4250)))
        return  base_demand * demand_elasticity

    """ Calculates the cost of investments for outlets and machines.
    If outlets or machines are sold, the value is negative (i.e., profit),
    but different weights are used for buying and selling are used.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    last_actions: Controllable_Variables
        The actions/state of the controllable variables performed in the previous turn.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Costs of investments or profits from buying/selling outlets/machines.

    """
    def _investments_machines_outlets(self, actions: Controllable_Variables, 
                                      last_actions : Controllable_Variables, 
                                      ts_state : Tailorshop_State) -> float:
        machineCondition = ts_state.machine_capacity / self.max_machine_capacity
        trade_outlets = self._trade(actions.outlets - last_actions.outlets,
                                    self.price_outlet, 
                                    0.8 * self.price_outlet - (100 * ts_state.turn))        
        trade_m50 = self._trade(actions.machines50 - last_actions.machines50,
                                    self.price_machine50, 
                                    0.8 * self.price_machine50 * machineCondition)
        trade_m100 = self._trade(actions.machines100 - last_actions.machines100,
                                    self.price_machine100, 
                                    0.8 * self.price_machine100 * machineCondition)
        return trade_outlets + trade_m50 + trade_m100

    """ Helper function for buying/selling assets.

    Parameters
    ----------

    number : float
        The number of assets to buy/sell.

    buying_price : float
        The value of the asset when buying it.
    
    selling_price:
        The value of the asset when selling it.

    Returns
    -------
    float
        Total cost/profit for the transaction.

    """
    @staticmethod
    def _trade(number : float, buying_price : float, selling_price : float) -> float:
        if number > 0:
            return number * buying_price
        else:
            return number * selling_price

    """ Calculates the regular expenses consisting of
    material orders, salaries and worker benefits, rent
    and storage costs.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Regular expenses

    """
    def _regular_expenses(self, actions: Controllable_Variables, 
                          ts_state : Tailorshop_State) -> float:        
        material = actions.material_order * ts_state.material_price
        num_workers = actions.workers50 + actions.workers100
        worker_salary = actions.workers_salary * num_workers
        worker_benefits = actions.worker_benefits * num_workers

        outlets = actions.outlets * self.outlet_rent
        location = self.locations_rents[actions.location]
        
        storage = ts_state.shirt_stock + (0.5 * ts_state.material_stock)
        
        expenses = material + worker_salary + worker_benefits + actions.advertising \
                    + outlets + location + actions.machines_maintenance + storage
        return expenses

    """ Calculates the customer interest.
    The interest is influenced by advertising as well as by
    the location and number of outlet stores.
    Note that this value is not the demand.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Customer interest.

    """
    def customer_interest(self, actions: Controllable_Variables, ts_state : Tailorshop_State) -> float:
        advertising_effect = min((actions.advertising / 5), Tailorshop.max_advertising_effect)
        outlet_effect = 100 * actions.outlets
        location_factor = 1 + (actions.location / 10)
        random_fluctuation = self.rnd_customer_interest[ts_state.turn - 1]

        result = ((advertising_effect + outlet_effect) * location_factor) + random_fluctuation
        return result

    """ Calculates the total company value.
    This value is usually the optimization goal for the task.

    Parameters
    ----------

    actions: Controllable_Variables
        The current actions/state of the controllable variables.

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    float
        Total company value.

    """
    def _company_value(self, actions: Controllable_Variables, ts_state : Tailorshop_State) -> float:
        turn = ts_state.turn
    
        bank = ts_state.bank_account
        machines_50 = actions.machines50 * (ts_state.machine_capacity / self.max_machine_capacity * self.price_machine50)
        machines_100 = actions.machines100 * (ts_state.machine_capacity / self.max_machine_capacity * self.price_machine100)
        outlets = (actions.outlets * self.price_outlet - (turn * 100))
        material = ts_state.material_stock * 2
        shirts = ts_state.shirt_stock * 20
        
        return bank + machines_50 + machines_100 + outlets + material + shirts

    """ Determines if the simulation is over.

    Returns
    -------
    bool
        True, if the simulation is over.

    """
    def is_finished(self) -> bool:
        return self._is_finished(self.current_state)

    """ Determines if the simulation is over for a given state.

    Parameters
    ----------

    ts_state: Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    bool
        True, if the simulation is over.

    """
    def _is_finished(self, ts_state : Tailorshop_State) -> bool:
        return (ts_state.turn >= len(self.rnd_material_price)) or (ts_state.turn >= len(self.rnd_customer_interest)) \
            or (ts_state.turn >= len(self.rnd_machines_100)) or (ts_state.turn >= len(self.rnd_machines_50))

    """ Calculates the successor state for a given state based on 
    given new actions.
    Note that this function does not alter the states in-place, so it can be used
    to test various outcomes on the same state.

    Parameters
    ----------

    actions: Controllable_Variables
        The actions/state of the controllable variables that should be applied to the state.

    last_actions: Controllable_Variables
        The previous actions/state of the controllable variables (that directly led to the state).

    ts_state : Tailorshop_State
        The state of the non-controllable tailorshop variables.

    Returns
    -------
    Tailorshop_State
        The successor state.

    """
    def calculate_step(self, actions : Controllable_Variables, 
                       last_actions : Controllable_Variables, 
                       ts_state : Tailorshop_State) -> Tailorshop_State:
        if self._is_finished(ts_state):
            print("Warning: Cannot perform step when the prepared random variables are depleted.")
            return None

        new_state = Tailorshop_State.from_ts_state(ts_state)

        # calculate the total available material
        material_before_production = ts_state.material_stock + actions.material_order
        
        # Calculate the machine capacity
        num_of_machines = actions.machines50 + actions.machines100
        machine_capacity = (0.9 * ts_state.machine_capacity) + ((actions.machines_maintenance / (num_of_machines + 0.00000001)) * 0.017)
        new_state.machine_capacity = machine_capacity
        
        # Calculate worker satisfaction
        satisfaction = (0.5 + ((actions.workers_salary - 850) / 550) + (actions.worker_benefits / 800))
        new_state.worker_satisfaction = satisfaction

         # Calculate production
        production_capacity = self._production_capacity_50(actions, new_state) + self._production_capacity_100(actions, new_state)
        actual_production = min(material_before_production, production_capacity)
        
        production_idle = 0
        if production_capacity != 0:
            production_idle = (production_capacity - actual_production) / production_capacity
        new_state.production_idle = production_idle
        new_state.material_stock = material_before_production - actual_production

        # Calculate shirt sales
        shirts_before_sales = ts_state.shirt_stock + actual_production
        current_demand = self._shirts_demand(actions, ts_state)
        
        shirt_sales = min(shirts_before_sales, current_demand)
        new_state.shirt_sales = shirt_sales

        sales_revenue = shirt_sales * actions.shirt_price
        new_state.shirt_stock = shirts_before_sales - shirt_sales

        # Calculate investments
        investments = self._investments_machines_outlets(actions, last_actions, ts_state)
        expenses = self._regular_expenses(actions, ts_state)

        # Calculate interest
        interest = 0
        if ts_state.bank_account > 0:
            interest = ts_state.bank_account * self.positive_interest
        else:
            interest = ts_state.bank_account * self.negative_interest

        bank_account = ts_state.bank_account + interest + sales_revenue - investments - expenses
        new_state.bank_account = bank_account

        # Calculate customer interest
        customer_interest = self.customer_interest(actions, ts_state)
        new_state.customer_interest = customer_interest
        
        # New material price
        material_price = round(self.rnd_material_price[ts_state.turn - 1])
        new_state.material_price = material_price

        new_state.turn = ts_state.turn + 1

        # New company value
        company_value = self._company_value(actions, new_state)
        new_state.company_value = company_value

        # round everything and update the shown variables
        new_state.round_and_update()

        return new_state
    
    """ Applies given actions and advances the simulation by one step.
    The function alters the internal state of the simulation and is the main 
    function to use for running the simulation.

    Parameters
    ----------

    actions: Controllable_Variables
        The actions/state of the controllable variables that should be applied.

    """
    def do_next_step(self, actions : Controllable_Variables) -> None:
        if self.is_finished():
            raise Exception("Cannot calculate next step once the simulation is finished.")

        last_actions = copy(self.last_actions)
        next_state = self.calculate_step(actions, last_actions, self.current_state)
        self.last_actions = copy(actions)
        self.current_state = next_state
    
    """ Returns a copy of the previous actions 
    (i.e., the actions that directly led to the current state). 

    Returns
    -------
    Controllable_Variables
        The previous actions/state of the controllable variables.

    """
    def get_last_actions(self) -> Controllable_Variables:
        return copy(self.last_actions)

    """ Returns a readable string representing the current state
    of the simulation. 

    Returns
    -------
    str
        String showing the state of the simulation.

    """
    def __str__(self) -> str:
        text = "Tailorshop Simulation: {}\n".format("finished" if self.is_finished() else "not finished")
        text += str(self.current_state)
        text += str(self.last_actions)
        return text