from tailorshop import Tailorshop
if __name__ == "__main__":
    # Create Tailorshop instance
    ts = Tailorshop(use_steps=True)
    print(ts)

    # Obtain initial actions
    actions = ts.get_last_actions()

    # Hire 2 workers and machines (100), increase material order to 500
    actions.set_workers100(2)
    actions.set_machines100(2)
    actions.set_material_order(500)

    # Do step
    ts.do_next_step(actions)
    print(ts)

    # Change locations
    actions.set_location("Inner City")

    # Do step
    ts.do_next_step(actions)
    print(ts)

    # Change advertising and worker salary/benefits
    actions.set_advertising(3000)
    actions.set_worker_benefits(100)
    actions.set_workers_salary(1180)

    # Do step
    ts.do_next_step(actions)
    print(ts)

    # Change shirt price
    actions.set_shirt_price(66)

    # Do step
    ts.do_next_step(actions)
    print(ts)
