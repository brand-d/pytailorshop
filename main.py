from tailorshop import Tailorshop
if __name__ == "__main__":
    # Create Tailorshop instance
    ts = Tailorshop()
    print(ts)
    print()

    # Obtain initial actions
    actions = ts.get_last_actions()

    # Hire 2 workers and machines (100), increase material order to 500
    actions.set_workers100(2)
    actions.set_machines100(2)
    actions.set_material_order(500)
    print(actions)
    print()
    
    # Do a step with the previous actions
    ts.do_next_step(actions)
    print(ts)
