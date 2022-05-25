import numpy as np

# returns function that calcualtes cost based on tier
def tier_costs(tier):
    if (tier == 1):
        return tier1_cost
    elif (tier == 2):
        return tier2_cost
    else:
        return tier3_cost

# returns cost of a practitioner or concierge
def worker_cost(cost, travel_dist, travel_rate):
    return cost + travel_dist*travel_rate

# returns cost for tier 1 events
def tier1_cost(prac_cost=65, conc_cost=25, travel_dist=0, travel_rate=0.585):
    travel_rate = 0.585
    prac_cost = worker_cost(prac_cost, travel_dist, travel_rate) 
    conc_cost =  worker_cost(conc_cost, travel_dist, travel_rate)
    
    return prac_cost + conc_cost 

# returns cost for tier 2 events
def tier2_cost(kit, num_participants, prac_cost=65, conc_cost=25, travel_dist=0, travel_rate=0.585):
    kits = kits_cost(kit, num_participants)
    prac_cost = worker_cost(prac_cost, travel_dist, travel_rate)
    conc_cost = worker_cost(conc_cost, travel_dist, travel_rate)

    return kits + prac_cost + conc_cost

# returns total cost of all kits given type of kit and num people
def kits_cost(kit, num_participants):
    """
    kits are encoded as numbers in the same order as on the corporate pricing 
    breakdown sheet.
    """
    kit_prices = {
        0 : 30,
        1 : 42,
        2 : 31, 
        3 : 40,
        4 : 38,
        5 : 57,
        6 : 70
    }

    return kit_prices[kit] * num_participants

# returns cost for tier 3 events: 2 practitioners, 1 concierge, med consumables
def tier3_cost(consum_lst, num_participants, prac_cost1=65, prac_cost2=65, conc_cost=25, travel_dist=0, travel_rate=0.585):
    """
    consum_lst: number of medical consumables of each type
    """
    prac1 = worker_cost(prac_cost1, travel_dist, travel_rate) 
    prac2 = worker_cost(prac_cost2, travel_dist, travel_rate) 
    conc = worker_cost(prac_cost2, travel_dist, travel_rate) 

    return prac1 + prac2 + med_consum(consum_lst)

# returns total cost of medical consumables
def med_consum(consum_lst):
    """
    both arrays must have the consumables listed in the same order
    """
    consum_array = np.array(consum_lst)
    consum_costs = np.array([5, 6, 12, 25, 1, 2, 3.5])

    return consum_array * consum_costs