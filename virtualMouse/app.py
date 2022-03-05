from os import stat
from flask import Flask
from math import pow, sqrt
import pyautogui as pg
from butterworth import Butter
import numpy, numba
import csv

pg.FAILSAFE = False

filter = Butter(
    btype="lowpass",
    cutoff = 1000,
    rolloff = 48,
    sampling = 44100 
)


class state():
    
    # Process noise varience (At rest)
    Q_ACC = 9.57629193670408e-05
    Q_VEL = 3.339386350278879e-05 * 0.2
    Q_DIS = 0.5 * 3.339386350278879e-05 * 0.04

    # Estimated error
    WEIGHT = 0.001
    p_MU_ACC = WEIGHT
    p_MU_VEL = WEIGHT
    p_MU_DIS = WEIGHT

    # Measured int acc and vel
    a_MU = 0
    v_MU = 0
    d_MU = 0

    # Measurement varience (At motion)
    R_ACC = 34.169150985200645
    R_VEL = 3.167365979974516 * 0.2
    R_DIS = 0.5 * 3.167365979974516 * 0.04

    # Int velocity
    u_ak = 0
    u_avk = 0
    u_avdk = 0

    # Initial displacement
    d_ak = 0
    d_avk = 0
    d_avdk = 0

# Time interval 200ms
with open('readings.csv', 'w', newline='') as readings:
    writer = csv.DictWriter(readings, fieldnames=['x', 'a_mu'])
    writer.writeheader()

# FLASK APP
app = Flask(__name__)

@app.route("/move/<float(signed=true):x>")
def index(x):
    """ Time update """
    # State extrapolation
    a_TU = state.a_MU
    v_TU = state.v_MU
    d_TU = state.d_MU
  
    # Covarience extrapolation
    p_TU_ACC = state.p_MU_ACC + state.Q_ACC
    p_TU_VEL = state.p_MU_VEL + state.Q_VEL
    p_TU_DIS = state.p_MU_DIS + state.Q_DIS

    """ Measurement Update """
    # Kalman Gain
    k_ACC = p_TU_ACC / (p_TU_ACC + state.R_ACC)
    k_VEL = p_TU_VEL / (p_TU_VEL + state.R_VEL)
    k_DIS = p_TU_DIS / (p_TU_DIS + state.R_DIS)

    # State update
    state.a_MU = a_TU + (k_ACC * (x - a_TU))
    v = state.u_avk + (state.a_MU * 0.2)
    state.v_MU = v_TU + (k_VEL * (v - v_TU))
    dis = (state.u_avk * 0.2) + (0.5 * state.a_MU * 0.04)
    state.d_MU = d_TU + (k_DIS * (dis - d_TU))

    # Covarience update
    state.p_MU_ACC = (1 - k_ACC) * p_TU_ACC
    state.p_MU_VEL = (1 - k_VEL) * p_TU_VEL
    state.p_MU_DIS = (1 - k_DIS) * p_TU_DIS

    # Displacement
    s_ak = (state.u_ak * 0.2) + (0.5 * state.a_MU * 0.04)
    s_avk = (state.u_avk * 0.2) + (0.5 * state.a_MU * 0.04)
    
    state.u_ak = state.u_ak + (state.a_MU * 0.2)
    state.u_avk = state.v_MU

    try:
        pg.moveRel(x, 0)
    except:
        print('Error pg move')

    # filter the data
    filtered_x = filter.send(x)

    with open('readings.csv', 'a', newline='') as readings:
        writer = csv.DictWriter(readings, fieldnames=['x', 'filtered_x'])
        writer.writerow({'x': x, 'filtered_x': filtered_x})

    state.d_ak = s_ak
    state.d_avk = s_avk
    state.d_avdk = state.d_MU

    return 'Hello'
