#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 13:45:33 2020

@author: howardwetsman
I don't think I have it well done yet. I don't think i'm right in the
treatment of the tested population. What I'm trying to do is take the
population tested that day, multiply by the current infection rate and then
by the sensitivity of the test and then subtract those from the infected
population. But it doesn't seem to make a difference whether it's 90 or 99%
sensitive.
"""

import plotly.graph_objects as go
from plotly.offline import plot
import numpy as np
from datetime import date as dt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Beta = rate of mew exposure of susceptable
# Gamma = recovery rate
# Sigma = infection rate of those exposed
# Mu = background mortality rate unrelated to this illness
# dS = Mu*(N-S) - Beta(S*I/N) - Nu*S
# dE = Beta * (S*I/N) - (Mu+Sigma)*E
# dI = Sigma*E - (Mu + Gamma)*I
# dR = Gamma *I - Mu * R + Nu * S
# N = S + E + I + R
# R0 = Beta/Gamma

# ds/dt = -B*s*i
#ds = -B*s*i*dt
# ds/s = -B*i*dt
# -ds/s = B*i*dt
# B = -ds/s*i*dt

# create streamlit sidebar inputs
R0 = st.sidebar.slider('R0', min_value=1.0, max_value=18.0, step=.5, value=2.0)
days_to_run = st.sidebar.slider('Days to run', min_value=100, max_value=365, step=5, value=200)
CFR = st.sidebar.slider('Case Fatality Rate in %', min_value=.1,
                        max_value=4.0, step=.1, value=.2)/100
days_to_recovery = st.sidebar.slider(
    'Days to recovery', min_value=10, max_value=30, step=1, value=16)
gamma = 1/days_to_recovery
beta = R0*gamma
N = st.sidebar.slider('Population in MM', min_value=100, max_value=7000, step=100, value=300)
# Will be inputs
# beta =
d0 = dt(2022, 1, 1)
test_perday = 1000
sens = .9
# End Inputs
d1 = dt.today()
delta = d1-d0
days = delta.days

# I=infected
#S= susceptable
#R = recovered
# N = total population
S_list = []  # initializing lists
I_list = []
R_list = []
D_list = []
Q_list = []

# set day zero
I = 1
R = 0
S = N-I-R
D = 0
Q = 0
S_list.append(S)
I_list.append(I)
R_list.append(R)
D_list.append(D)
Q_list.append(Q)

for day in range(1, days_to_run):
    baserate = I/S
    dQ = test_perday*baserate*sens
    dD = I*CFR*gamma
    dS = -beta*I*S/N
    dR = gamma*I
    dI = beta*I*S/N - dR - dD
    # dI = beta*I*S/N - dR - dD - dQ
    S = S+dS
    R = R+dR
    I = I+dI
    D = D+dD
    # Q = Q+dQ
    S_list.append(S)
    I_list.append(I)
    R_list.append(R)
    D_list.append(D)
    # Q_list.append(Q)

dates = np.arange(1, days_to_run+1)
fig, ax = plt.subplots()
# fig = go.Figure()
print(len(dates), len(S_list))
ax.scatter(dates, S_list, label='Susceptible')
# fig.add_trace(
#     go.Scatter(x=dates, y=S_list,
#                name="Susceptible", line=dict(color='goldenrod')))
ax.scatter(dates, I_list, label='Infected')
# fig.add_trace(
#     go.Scatter(x=dates, y=I_list,
#                name="Infected", line=dict(color='red')))
ax.scatter(dates, R_list, label='Recovered')
# fig.add_trace(
#     go.Scatter(x=dates, y=R_list,
#                name="Recovered", line=dict(color='green')))
ax.scatter(dates, D_list, label='Dead')
fig.legend(loc='center left')
# fig.add_trace(
#     go.Scatter(x=dates, y=D_list,
#                name="Dead", line=dict(color='violet')))
# ax.scatter(dates, Q_list, label='Quarantined')
# fig.add_trace(
#      go.Scatter(x=dates, y=Q_list,
#                 name="Quarantined",line=dict(color='black')))

# fig.update_layout(
#     title={
#         'text': f'America with R0 = {R0} and CFR of {CFR*100}%',
#         'y': 0.9,
#         'x': 0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'},
#     annotations=[
#         dict(
#             x=dates[days],
#             y=5,
#             xref="x",
#             yref="y",
#             text=f'We are here: day {dates[days]}',
#             showarrow=True,
#             arrowhead=1,
#             ax=0,
#             ay=-40)
#     ]
# )

st.pyplot(fig)
