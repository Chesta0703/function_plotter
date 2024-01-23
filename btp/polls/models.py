from django.db import models

# Create your models here.
# models.py (or a separate Python file if you prefer)

import numpy as np

class NetworkedEpi:
    def __init__(self, n):
        # Initialization of parameters
        self.n = n  # Number of nodes
        self.beta = np.ones((n, n)) * 0.1  # Default βij matrix
        self.gamma = np.ones(n) * 0.05     # Default γi vector
        self.h = 0.1                       # Default time step
        self.data = {'S': [], 'I': [], 'R': [], 'T': []}

        # Initialize state variables
        self.reset_states()

    def reset_states(self):
        # Initialize the state variables (S, I, R)
        self.S = np.ones(self.n) * 0.99  # Default Susceptible
        self.I = np.zeros(self.n)        # Default Infected
        self.I[0] = 0.01                 # Initial infected node
        self.R = np.zeros(self.n)        # Default Recovered

    def update_params(self, beta=None, gamma=None, h=None):
        # Update the parameters β, γ, and h
        if beta is not None:
            self.beta = beta
        if gamma is not None:
            self.gamma = gamma
        if h is not None:
            self.h = h

    def update(self):
        # Update the state variables for one time step
        new_S = self.S - self.h * self.S * np.sum(self.beta * self.I, axis=1)
        new_I = self.I + self.h * (self.S * np.sum(self.beta * self.I, axis=1) - self.gamma * self.I)
        new_R = self.R + self.h * self.gamma * self.I

        # Normalization to ensure the sum of S, I, R is 1 for each node
        total = new_S + new_I + new_R
        self.S, self.I, self.R = new_S / total, new_I / total, new_R / total

    def generate(self, t0, tf):
        # Generate the epidemic curve from time t0 to tf
        self.reset_states()
        self.data['T'] = [t0]
        self.data['S'].append(self.S.copy())
        self.data['I'].append(self.I.copy())
        self.data['R'].append(self.R.copy())

        while self.data['T'][-1] < tf:
            self.update()
            self.data['T'].append(self.data['T'][-1] + self.h)
            self.data['S'].append(self.S.copy())
            self.data['I'].append(self.I.copy())
            self.data['R'].append(self.R.copy())

        return np.array(self.data['T']), np.array(self.data['S']), np.array(self.data['I']), np.array(self.data['R'])

    def clear(self):
        # Clear the stored data
        self.data = {'S': [], 'I': [], 'R': [], 'T': []}
