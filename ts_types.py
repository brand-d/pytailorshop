from __future__ import annotations
def non_negative(value : float) -> float:
    return max(value, 0)

def clamp(value : float, min_val : float, max_val : float) -> float:
        return max(min(value, max_val), min_val)

def step_and_clamp(value : int, min_val : int, max_val : int, step : int, stepping : bool = True) -> int:
        result = clamp(value, min_val, max_val)
        if stepping:
            result = (result // step) * step
        return result

class Tailorshop_State:
    def __init__(self, bank_account=165775, shirt_sales=407, material_price=4, shirt_stock=81,
                 worker_satisfaction=0.98, production_idle=0, company_value=250691,
                 customer_interest=767, material_stock=16, machine_capacity=47, turn=1) -> None:
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
    
    def __copy__(self) -> Tailorshop_State:
        return Tailorshop_State.from_ts_state(self)
    
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
        # Worker satisfaction and production idle are primarily used to calculate damage and satisfaction (%), and should not be rounded before that
        # In the next turn, they are completely calculated from scratch, so it is not necessary to round them at all

    def get_shown_damage(self) -> float:
        return 2 * (50 - self.machine_capacity)

    def get_shown_worker_satisfaction(self) -> float:
        return round(100 * self.worker_satisfaction / 1.7)

class Controllable_Variables:
    def __init__(self, workers50=8, workers100=0, workers_salary=1080, worker_benefits=50, 
                 shirt_price=52, outlets=1, location=1, material_order=0, machines50=10, 
                 machines100=0, machines_maintenance=1200, advertising=2800, consider_stepping=True) -> None:
        self.consider_stepping = consider_stepping
        self.set_workers50(workers50)
        self.set_workers100(workers100)
        w_salary_stepped = step_and_clamp(workers_salary, 0, 5000, 100, stepping=self.consider_stepping)
        self.worker_salary_offset = workers_salary - w_salary_stepped
        self.set_workers_salary(workers_salary)
        self.set_worker_benefits(worker_benefits)
        self.set_shirt_price(shirt_price)
        self.set_outlets(outlets)
        self.set_location(location)
        self.set_material_order(material_order)
        self.set_machines50(machines50)
        self.set_machines100(machines100)
        self.set_machines_maintenance(machines_maintenance)
        self.set_advertising(advertising)

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
            consider_stepping=self.consider_stepping
        )
        return cloned

    def __str__(self) -> str:
        text = "Actions\n"
        text += "    Workers 50:          {}\n".format(self.workers50)
        text += "    Workers 100:         {}\n".format(self.workers100)
        text += "    Worker Salary:       {}\n".format(self.workers_salary)
        text += "    Worker Benefits:     {}\n".format(self.worker_benefits)
        text += "    Shirt Price:         {}\n".format(self.shirt_price)
        text += "    Number of outlets:   {}\n".format(self.outlets)
        text += "    Location:            {}\n".format(["Suburb", "City", "Inner City"][self.location])
        text += "    Material Order:      {}\n".format(self.material_order)
        text += "    Machines 50:         {}\n".format(self.machines50)
        text += "    Machines 100:        {}\n".format(self.machines100)
        text += "    Machine Maintenance: {}\n".format(self.machines_maintenance)
        text += "    Advertising:         {}\n".format(self.advertising)
        return text

    def set_workers50(self, value : int):
        self.workers50 = step_and_clamp(value, 0, 20, 1, stepping=self.consider_stepping)
    
    def set_workers100(self, value : int):
        self.workers100 = step_and_clamp(value, 0, 20, 1, stepping=self.consider_stepping)
    
    def set_workers_salary(self, value : int):
        self.workers_salary = step_and_clamp(value, 0, 5000, 100, stepping=self.consider_stepping) + self.worker_salary_offset
    
    def set_worker_benefits(self, value : int):
        self.worker_benefits = step_and_clamp(value, 0, 500, 10, stepping=self.consider_stepping)
    
    def set_shirt_price(self, value : int):
        self.shirt_price = step_and_clamp(value, 10, 100, 2, stepping=self.consider_stepping)
    
    def set_outlets(self, value : int):
        self.outlets = step_and_clamp(value, 0, 10, 1, stepping=self.consider_stepping)

    def set_location(self, value : int):
        self.location = step_and_clamp(value, 0, 2, 1, stepping=self.consider_stepping)

    def set_material_order(self, value : int):
        self.material_order = step_and_clamp(value, 0, 5000, 50, stepping=self.consider_stepping)

    def set_machines50(self, value : int):
        self.machines50 = step_and_clamp(value, 0, 20, 1, stepping=self.consider_stepping)

    def set_machines100(self, value : int):
        self.machines100 = step_and_clamp(value, 0, 20, 1, stepping=self.consider_stepping)

    def set_machines_maintenance(self, value : int):
        self.machines_maintenance = step_and_clamp(value, 0, 5000, 100, stepping=self.consider_stepping)

    def set_advertising(self, value : int):
        self.advertising = step_and_clamp(value, 0, 10000, 100, stepping=self.consider_stepping)
