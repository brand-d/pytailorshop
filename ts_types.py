from __future__ import annotations
from typing import Union

""" Helper function to prevent values from becoming negative.

    Parameters
    ----------

    value : float
        Any input number.

    Returns
    -------
    float
        The input number or zero if the input was negative.

    """
def non_negative(value : float) -> float:
    return max(value, 0)

""" Helper function to clamp numbers between a minimum and maximum.

    Parameters
    ----------

    value : float
        Any input number.
    
    min_val : float
        The minimum number allowed.

    max_val : float
        The maximum number allowed.

    Returns
    -------
    float
        min_val, iff value < min_val, 
        max_val, iff value > max_val,
        otherwise the value is returned.

    """
def clamp(value : float, min_val : float, max_val : float) -> float:
        return max(min(value, max_val), min_val)

""" Extended version of clamp that also ensures that it is in line with a given stepsize.
Values will be set to the lower step when not in line with the stepsize.
Examples:

>>> step_and_clamp(7, 0, 10, 3)
6
>>> step_and_clamp(25, 0, 15, 10)
10

    Parameters
    ----------

    value : int
        Any input number.
    
    min_val : int
        The minimum number allowed.

    max_val : int
        The maximum number allowed.
    
    stepsize : int
        The stepsize to use.
    
    use_steps : bool
        Indicates if the stepsize should be considered.

    Returns
    -------
    float
        Value within the range [minval, max_val] that is a multiple of the stepsize.

    """
def step_and_clamp(value : int, min_val : int, max_val : int, 
                   stepsize : int, use_steps : bool = True) -> int:
        result = clamp(value, min_val, max_val)
        if use_steps:
            result = (result // stepsize) * stepsize
        return result

class Tailorshop_State:
    """ Class for managing the state variables of the Tailorshop simulation.
    These consist of all variables not directly controllable by the user/player.
    For worker satisfaction and machine capacity, two additional variables for 
    easier interpretation are added:
    - percent_worker_satisfaction (satisfaction in percent)
    - damage (Percentage of damage to the machines)
    Note that, although counter-intuitive, most values are floats. This is because
    they can be non-integer in intermediate steps, but are rounded at the end.

    """

    """ Creates an instance of the Tailorshop state.

    Parameters
    ----------

    bank_account : float
        The current amount of money in the bank account.

    shirt_sales : float
        The shirt sales from the previous state to this state.
    
    material_price : float
        The current price for raw materials.
    
    shirt_stock : float
        The number of shirts in stock.
    
    worker_satisfaction : float
        The current worker satisfaction. This variable is not
        meant to be interpreted directly, but an interpretable
        version (percent_worker_satisfaction) will be derived.
    
    production_idle : float
        The current loss of production 
        (i.e., unused capacity).
    
    company_value : float
        The current company value.
    
    customer_interest : float
        The current customer interest.
    
    material_stock : float
        The amount of raw materials in stock.
    
    machine_capacity : float
        The current machine capacity.
    
    turn : int
        The current turn.

    """
    def __init__(self, bank_account : float = 165775, shirt_sales : float = 407, 
                 material_price : float = 4, shirt_stock : float = 81,
                 worker_satisfaction : float = 0.98, production_idle : float = 0,
                 company_value : float = 250691, customer_interest : float = 767, 
                 material_stock : float = 16, machine_capacity : float = 47, 
                 turn : int = 1) -> None:
        self.bank_account = bank_account
        self.shirt_sales = non_negative(shirt_sales)
        self.material_price = non_negative(material_price)
        self.shirt_stock = non_negative(shirt_stock)
        self.worker_satisfaction = non_negative(worker_satisfaction)
        self.production_idle = clamp(production_idle, 0, 100)
        self.company_value = company_value
        self.customer_interest = non_negative(customer_interest)
        self.material_stock = non_negative(material_stock)
        self.machine_capacity = clamp(machine_capacity, 0, 50)
        self.turn = non_negative(turn)
        self.damage = self.get_shown_damage()
        self.percent_worker_satisfaction = self.get_shown_worker_satisfaction()
    
    """ Clones a given Tailorshop State.

    Parameters
    ----------

    ts_state : Tailorshop_State
        State to clone.

    Returns
    -------
    Tailorshop_State
        Cloned state.

    """
    @staticmethod
    def from_ts_state(ts_state : Tailorshop_State) -> Tailorshop_State:
        return Tailorshop_State(
            bank_account=ts_state.bank_account, 
            shirt_sales=ts_state.shirt_sales, 
            material_price=ts_state.material_price, 
            shirt_stock=ts_state.shirt_stock,
            worker_satisfaction=ts_state.worker_satisfaction, 
            production_idle=ts_state.production_idle, 
            company_value=ts_state.company_value,
            customer_interest=ts_state.customer_interest, 
            material_stock=ts_state.material_stock, 
            machine_capacity=ts_state.machine_capacity, 
            turn=ts_state.turn
        )
    
    """ Implementation of copy.

    Returns
    -------
    Tailorshop_State
        Copy of the current state.

    """
    def __copy__(self) -> Tailorshop_State:
        return Tailorshop_State.from_ts_state(self)
    
    """ Rounds the variables and derives the values for 
    damage and percent_worker_satisfaction.

    """
    def round_and_update(self) -> None:
        self.bank_account = round(self.bank_account)
        self.shirt_sales = round(self.shirt_sales)
        self.material_price = round(self.material_price)
        self.shirt_stock = round(self.shirt_stock)
        self.company_value = round(self.company_value)
        self.customer_interest = round(self.customer_interest)
        self.material_stock = round(self.material_stock)
        self.machine_capacity = round(self.machine_capacity)
        self.damage = self.get_shown_damage()
        self.percent_worker_satisfaction = self.get_shown_worker_satisfaction()
        # Worker satisfaction and production idle are primarily used to 
        #calculate damage and satisfaction (%), and should not be rounded before that
        # In the next turn, they are completely calculated from scratch, 
        # so it is not necessary to round them at all

    """ Returns the value for the damage based on
    machine capacity.

    Returns
    -------
    float
        Interpretable machine damage.

    """
    def get_shown_damage(self) -> float:
        return 2 * (50 - self.machine_capacity)

    """ Returns the percentage of worker satisfaction.

    Returns
    -------
    float
        Worker satisfaction in percent.

    """
    def get_shown_worker_satisfaction(self) -> float:
        return round(100 * self.worker_satisfaction / 1.7)
    
    """ Returns a readable string representation of the state.

    Returns
    -------
    str
        Readable string representation of the state.

    """
    def __str__(self) -> str:
        text = "State \n"
        text += "    Turn:                    {}\n".format(self.turn)
        text += "    Bank Account:            {}\n".format(self.bank_account)
        text += "    Company Value:           {}\n".format(self.company_value)
        text += "    Shirt Sales:             {}\n".format(self.shirt_sales)
        text += "    Shirt Stock:             {}\n".format(self.shirt_stock)
        text += "    Material Price:          {}\n".format(self.material_price)
        text += "    Material Stock:          {}\n".format(self.material_stock)
        text += "    Customer Interest:       {}\n".format(self.customer_interest)
        text += "    Production Idle:         {}\n".format(self.production_idle)
        text += "    Machine Capacity:        {}\n".format(self.machine_capacity)
        text += "    Machine Damage:          {}\n".format(self.damage)
        text += "    Worker Satisfaction:     {}\n".format(self.worker_satisfaction)
        text += "    Worker Satisfaction (%): {}\n".format(self.percent_worker_satisfaction)
        return text

class Controllable_Variables:
    """ Class for managing the controllable variables (actions).
    Provides setter-functions that consider the stepsizes and limits for the values.

    """

    """ Constructor for the Controllable Variable Object.

    Parameters
    ----------

    workers50 : int
        Number of workers for machine50 (machines that can produce 50 shirts).
    
    workers100 : int
        Number of workers for machine100 (machines that can produce 100 shirts).
    
    workers_salary : int
        Worker salary per turn per worker.
    
    worker_benefits : int
        Worker benefits per turn per worker.
    
    shirt_price : int
        Price for a shirt.
    
    outlets : int
        Number of outlets.
    
    location : int
        Location (0 = suburb, 1 = city, 2 = inner city).
    
    material_order : int
        The amount of raw material to order.
    
    machines50 : int
        The number of machine50 (machines that can produce 50 shirts).
    
    machines100 : int
        The number of machine100 (machines that can produce 100 shirts).
    
    machines_maintenance : int
        Money spent for maintenance.
    
    advertising : int
        Money spent on advertisements.
    
    use_steps : bool
        If true, stepsizes are considered. Otherwise, all values within
        limits are allowed.

    """
    def __init__(self, workers50 : int = 8, workers100 : int = 0, workers_salary : int = 1080, 
                 worker_benefits: int = 50, shirt_price: int = 52, outlets: int = 1, 
                 location: int = 1, material_order: int = 0, machines50: int = 10, 
                 machines100: int = 0, machines_maintenance: int = 1200, 
                 advertising: int = 2800, use_steps : bool = True) -> None:
        self.use_steps = use_steps
        self.set_workers50(workers50)
        self.set_workers100(workers100)
        self.set_outlets(outlets)
        self.set_location(location)
        self.set_machines50(machines50)
        self.set_machines100(machines100)
        
        w_salary_stepped = step_and_clamp(workers_salary, 0, 5000, 100, use_steps=self.use_steps)
        self.worker_salary_offset = workers_salary - w_salary_stepped
        self.set_workers_salary(workers_salary)

        w_benefits_stepped = step_and_clamp(worker_benefits, 0, 500, 10, use_steps=self.use_steps)
        self.worker_benefits_offset = worker_benefits - w_benefits_stepped
        self.set_worker_benefits(worker_benefits)

        shirt_price_stepped = step_and_clamp(shirt_price, 0, 100, 2, use_steps=self.use_steps)
        self.shirt_price_offset = shirt_price - shirt_price_stepped
        self.set_shirt_price(shirt_price)
        
        material_order_stepped = step_and_clamp(material_order, 0, 5000, 50, use_steps=self.use_steps)
        self.material_order_offset = material_order - material_order_stepped
        self.set_material_order(material_order)
        
        machines_maintenance_stepped = step_and_clamp(machines_maintenance, 0, 5000, 100, use_steps=self.use_steps)
        self.machines_maintenance_offset = machines_maintenance - machines_maintenance_stepped
        self.set_machines_maintenance(machines_maintenance)

        advertising_stepped = step_and_clamp(advertising, 0, 10000, 100, use_steps=self.use_steps)
        self.advertising_offset = advertising - advertising_stepped
        self.set_advertising(advertising)

    """ Implementation of copy.

    Returns
    -------
    Controllable_Variables
        Copy of the current object.

    """
    def __copy__(self) -> Controllable_Variables:
        cloned = Controllable_Variables(
            workers50=self.workers50,
            workers100=self.workers100,
            workers_salary=self.workers_salary,
            worker_benefits=self.worker_benefits,
            shirt_price=self.shirt_price,
            outlets=self.outlets,
            location=self.location,
            material_order=self.material_order,
            machines50=self.machines50,
            machines100=self.machines100,
            machines_maintenance=self.machines_maintenance,
            advertising=self.advertising,
            use_steps=self.use_steps
        )
        return cloned

    """ Returns a readable string representation of the actions.

    Returns
    -------
    str
        Readable string representation of the actions.

    """
    def __str__(self) -> str:
        text = "Actions\n"
        text += "    Workers 50:              {}\n".format(self.workers50)
        text += "    Workers 100:             {}\n".format(self.workers100)
        text += "    Worker Salary:           {}\n".format(self.workers_salary)
        text += "    Worker Benefits:         {}\n".format(self.worker_benefits)
        text += "    Shirt Price:             {}\n".format(self.shirt_price)
        text += "    Number of outlets:       {}\n".format(self.outlets)
        text += "    Location:                {}\n".format(["Suburb", "City", "Inner City"][self.location])
        text += "    Material Order:          {}\n".format(self.material_order)
        text += "    Machines 50:             {}\n".format(self.machines50)
        text += "    Machines 100:            {}\n".format(self.machines100)
        text += "    Machine Maintenance:     {}\n".format(self.machines_maintenance)
        text += "    Advertising:             {}\n".format(self.advertising)
        return text

    """ Changes the number of workers50.
    The new value will be clamped to ensure it is within the limits.

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_workers50(self, value : int):
        self.workers50 = step_and_clamp(value, 0, 20, 1, use_steps=self.use_steps)
    
    """ Changes the number of workers100.
    The new value will be clamped to ensure it is within the limits.

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_workers100(self, value : int):
        self.workers100 = step_and_clamp(value, 0, 20, 1, use_steps=self.use_steps)
    
    """ Changes the worker salary.
    The new value will be clamped to ensure it is within the limits.
    Additionally, it can only be altered in steps of 100 relative to the starting value
    (if stepsize is considered).

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_workers_salary(self, value : int):
        self.workers_salary = step_and_clamp(value, 0, 5000, 100, use_steps=self.use_steps) + self.worker_salary_offset
    
    """ Changes the worker benefits.
    The new value will be clamped to ensure it is within the limits.
    Additionally, it can only be altered in steps of 10 relative to the starting value
    (if stepsize is considered).

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_worker_benefits(self, value : int):
        self.worker_benefits = step_and_clamp(value, 0, 500, 10, use_steps=self.use_steps) + self.worker_benefits_offset
    
    """ Changes the shirt price.
    The new value will be clamped to ensure it is within the limits.
    Additionally, it can only be altered in steps of 2 relative to the starting value
    (if stepsize is considered).

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_shirt_price(self, value : int):
        self.shirt_price = step_and_clamp(value, 10, 100, 2, use_steps=self.use_steps) + self.shirt_price_offset
    
    """ Changes the number of outlets.
    The new value will be clamped to ensure it is within the limits.

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_outlets(self, value : int):
        self.outlets = step_and_clamp(value, 0, 10, 1, use_steps=self.use_steps)

    """ Changes the location.
    The new value will be clamped to ensure it is within the limits.

    Parameters
    ----------

    location : {int, str}
        The new location. If it is a string, it has to be one of
        ["Suburb", "City", "Inner City"]. If it is an integer,
        it is interpreted to be the index of the respective locations list.

    """
    def set_location(self, location : Union[str, int]):
        if isinstance(location, int):
            self.location = step_and_clamp(location, 0, 2, 1, use_steps=self.use_steps)
        else:
            idx = ["suburb", "city", "inner city"].index(location.lower())
            self.location = step_and_clamp(idx, 0, 2, 1, use_steps=self.use_steps)

    """ Changes the amount of raw material to order.
    The new value will be clamped to ensure it is within the limits.
    Additionally, it can only be altered in steps of 50 relative to the starting value
    (if stepsize is considered).

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_material_order(self, value : int):
        self.material_order = step_and_clamp(value, 0, 5000, 50, use_steps=self.use_steps) + self.material_order_offset

    """ Changes the number of machines50.
    The new value will be clamped to ensure it is within the limits.

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_machines50(self, value : int):
        self.machines50 = step_and_clamp(value, 0, 20, 1, use_steps=self.use_steps)

    """ Changes the number of machines100.
    The new value will be clamped to ensure it is within the limits.

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_machines100(self, value : int):
        self.machines100 = step_and_clamp(value, 0, 20, 1, use_steps=self.use_steps)

    """ Changes the amount of money spent on maintenance.
    The new value will be clamped to ensure it is within the limits.
    Additionally, it can only be altered in steps of 100 relative to the starting value
    (if stepsize is considered).

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_machines_maintenance(self, value : int):
        self.machines_maintenance = step_and_clamp(value, 0, 5000, 100, use_steps=self.use_steps) + self.machines_maintenance_offset

    """ Changes the amount of money spent on advertisements.
    The new value will be clamped to ensure it is within the limits.
    Additionally, it can only be altered in steps of 100 relative to the starting value
    (if stepsize is considered).

    Parameters
    ----------

    value : int
        The new value.

    """
    def set_advertising(self, value : int):
        self.advertising = step_and_clamp(value, 0, 10000, 100, use_steps=self.use_steps) + self.advertising_offset
