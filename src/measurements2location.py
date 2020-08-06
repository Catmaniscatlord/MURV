#! /usr/bin/env python3

"""This program calculates an emitter position based on access point
locations and an approximate measurement of the distance from each
access point.
"""

import os
import sys
import csv
import random
import numpy as np
import scipy
import scipy.optimize

verbose = True
method = 'hillclimbing'
# method = 'simplex'

def main():
    """Procedure: read AP positions and distance measurements from a .csv
    file, then chose a starting point, then invoke an optimization function"""
    
    prog_dir = os.path.dirname(sys.argv[0]) # get this program's directory
    fpath = os.path.join(prog_dir, '..', 'data', 'emitter-sim.csv')
    print('# prog_dir, fpath:', prog_dir, fpath)
    ap_positions, measured_distances  = read_emitter_file(fpath)
    print('# AP_positions:', ap_positions)
    print('# measured_distances', measured_distances)
    assert(len(ap_positions) == len(measured_distances)) # minimal sanity check
    e_guess = np.array([1.0, 7.0, -21.0])   # starting point, could be close or quite far away
    print('# START:', e_guess, '   ', calc_cost(e_guess, ap_positions, measured_distances))
    # now do some simple hill-climbing or simplex method, starting
    # from this position.  we should also investigate simulated
    # annealing:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.dual_annealing.html
    if method == 'hillclimbing':
        emitter_pos = optimize_hillclimbing(calc_cost, e_guess, ap_positions, measured_distances)
    elif method == 'simplex':
        opt_result = optimize_simplex(calc_cost, e_guess, ap_positions, measured_distances)
        emitter_pos = opt_result.x
    else:
        sys.stderr.write('*error* we have no method %s at this time' % method)
    print('RESULT:  ', emitter_pos)

def optimize_hillclimbing(calc_cost, e_guess, ap_positions, measured_distances):
    """An embarrassingly simple hillclimbing optimization"""
    e_guess_old = e_guess
    cost_old = calc_cost(e_guess, ap_positions, measured_distances)
    for i in range(1000):
        e_guess = mutate(e_guess) # take the tentative step
        cost = calc_cost(e_guess, ap_positions, measured_distances)
        if verbose:
            print('  ', e_guess_old, '   ', cost_old, ' -> ', e_guess, '   ', cost)
        if cost <= cost_old:     # did cost get lower or stay put?
            e_guess_old = e_guess
            cost_old = cost
            if verbose:
                print('      NEW:', e_guess)
        else:                   # or did it get higher?
            e_guess = e_guess_old
            cost = cost_old
            pass
    return e_guess

def calc_cost_embedded(x, *args):
    """This is a repackaging of the calc_cost() function so that it can be
    passed to the scipy optimization functions
    """
    ap_positions = args[0]
    measured_distances = args[1]
    return calc_cost(x, ap_positions, measured_distances)

def optimize_simplex(calc_cost, e_guess, ap_positions, measured_distances):
    """use the simplex method to opitmize our cost function. this mostly
    just packages it up for the scipy.optimize method for Nelder-Mead
    """
    emitter_pos = scipy.optimize.minimize(calc_cost, e_guess, method='Nelder-Mead', 
                                          args=(ap_positions, measured_distances))
    return emitter_pos

def mutate(pt):
    """Take a small step, drawing from a random distribution."""
    sigma = 0.1                 # sigma for our step size
    mu = 0                      # step centered at zero
    # choose between a lognormal distribution (long tail) and a
    # gaussian (short tail, never jumps too far)
    shift = np.array([random.lognormvariate(mu, sigma)*(random.randint(0, 1)*2-1) for i in range(3)])
    # shift = np.array([random.gauss(mu, sigma) for i in range(3)])
    pt = pt + shift
    if verbose:
        print('SHIFT:', shift)
    return pt


def calc_cost(e_guess, ap_positions, measured_distances):
    """This is one possible cost calculation for geolocation:
    cost(e_guess) = Sum_i(||e_guess - ap_i||^2 - measuredDistance_i^2)^2

    """
    sum = 0
    for (apos, md) in zip(ap_positions, measured_distances):
        d2 = distance_sq(apos, e_guess)
        # print(apos, '   ', e_guess, ':   ', d2)
        sum += (d2 - md**2)**2
    return sum


def distance_sq(p1, p2):
    """Simple 3-D Euclidean distance."""
    assert(len(p1) == len(p2) and len(p1) == 3)
    return (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2

def read_emitter_file(fpath):
    """Reads and returns the AP positions and the measured distances to
    each AP from a csv-formatted file."""
    positions = []
    distances = []
    with open(fpath) as csvfile:
        reader = csv.reader(csvfile)
        print(reader.__next__())
        for row in reader:
            positions.append([float(word) for word in row[1:4]])
            distances.append(float(row[4]))
    return positions, distances
    



if __name__ == '__main__':
    main()
