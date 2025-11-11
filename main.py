import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Set up the Streamlit app
st.title('Epidemiological Vaccination Model')
st.markdown("""
Welcome to the *Epidemiological Vaccination Model* app! This app allows you to simulate the spread
of a disease within a population and observe the effects of vaccination efforts over time.
You can adjust various parameters to explore different scenarios and understand the dynamics of
disease spread, vaccination, and recovery.
This model is inspired by real-world epidemiological studies
and is tailored to provide insights into managing infectious diseases.
Use the sidebar to input your desired parameters and observe how they affect the susceptible,
vaccinated, carrier, infected, recovered populations, and the misinformation index.
""")

# Sidebar for parameters
st.sidebar.header('Model Parameters')
st.sidebar.markdown("""
Adjust the parameters below to simulate different scenarios. These parameters influence the disease
dynamics, vaccination effectiveness, and public perception.
""")
Lambda = st.sidebar.number_input('Total Population (Lambda)', value=186121000, min_value=1000,
                                 help="Total population size.")
mu = st.sidebar.number_input('Natural Mortality Rate (mu)', value=1/70, min_value=0.0,
                             max_value=1.0, help="Rate at which individuals naturally die.")
beta = st.sidebar.number_input('Transmission Rate (beta)', value=0.3, min_value=0.0, max_value=1.0,
                               help="Rate at which the disease spreads.")
epsilon = st.sidebar.number_input('Modification Factor (epsilon)', value=1.0,
                                  min_value=0.0,  # Added min_value for completeness
                                  max_value=10.0, help="Factor modifying transmission rate due to carriers.")
p0 = st.sidebar.number_input('Base Vaccination Rate (p0)', value=0.01,
                             min_value=0.0,
                             max_value=1.0, help="Baseline rate of vaccination.")
pmax = st.sidebar.number_input('Max Vaccination Rate (pmax)', value=0.05,
                               min_value=0.0,
                               max_value=1.0, help="Maximum rate of vaccination based on public awareness.")
D = st.sidebar.number_input('Reactivity Factor (D)', value=5000, min_value=0, help="Factor determining public reactivity to the disease.")
psi = st.sidebar.number_input('Vaccine Effectiveness (psi)', value=0.9, min_value=0.0, max_value=1.0,
                              help="Effectiveness of the vaccine.")
theta = st.sidebar.number_input('Waning Rate of Vaccine-Induced Immunity (theta)', value=1/365,
                                min_value=0.0, max_value=1.0, help="Rate at which vaccine-induced immunity wanes.")
sigma = st.sidebar.number_input('Rate of Symptom Development (sigma)', value=0.01, min_value=0.0,
                                max_value=1.0, help="Rate at which carriers develop symptoms.")
delta = st.sidebar.number_input('Recovery Rate for Carriers (delta)', value=1/14, min_value=0.0,
                                max_value=1.0, help="Rate at which carriers recover.")
rho = st.sidebar.number_input('Recovery Rate for Ill (rho)', value=1/10, min_value=0.0,
                              max_value=1.0, help="Rate at which infected individuals recover.")
d = st.sidebar.number_input('Disease-Induced Mortality Rate (d)', value=1/1000, min_value=0.0,
                            max_value=1.0, help="Mortality rate due to the disease.")
phi = st.sidebar.number_input('Waning Rate of Natural Immunity (phi)', value=1/365, min_value=0.0,
                              max_value=1.0, help="Rate at which natural immunity wanes.")
k = st.sidebar.number_input('Information Coverage (k)', value=0.5, min_value=0.0, max_value=1.0,
                            help="Extent of information coverage about the disease.")
a = st.sidebar.number_input('Characteristic Memory Length (a)', value=1/30, min_value=0.0,
                            max_value=1.0, help="Memory length affecting public response to the disease.")
alpha_gamma = st.sidebar.number_input('Growth Rate for Healthcare Access (alpha_gamma)',
                                      value=0.01, min_value=0.0, max_value=1.0, help="Rate at which access to healthcare improves.")
beta_gamma = st.sidebar.number_input('Reduction Rate for Healthcare Access (beta_gamma)',
                                     value=0.005, min_value=0.0, max_value=1.0, help="Rate at which healthcare access is reduced.")
alpha_eta = st.sidebar.number_input('Growth Rate for Social Influence (alpha_eta)', value=0.02,
                                    min_value=0.0, max_value=1.0, help="Rate at which social influence grows.")
beta_eta = st.sidebar.number_input('Reduction Rate for Social Influence (beta_eta)', value=0.01,
                                   min_value=0.0, max_value=1.0, help="Rate at which social influence wanes.")
alpha_xi = st.sidebar.number_input('Growth Rate of Misinformation (alpha_xi)', value=0.005,
                                   min_value=0.0, max_value=1.0, help="Rate at which misinformation spreads.")
beta_xi = st.sidebar.number_input('Reduction Rate of Misinformation (beta_xi)', value=0.002,
                                  min_value=0.0, max_value=1.0, help="Rate at which misinformation is countered.")

# Initial conditions
st.sidebar.header('Initial Conditions')
st.sidebar.markdown("Set the initial population distribution among the different groups.")
initial_infected = st.sidebar.number_input('Initial Infected Population', value=1000, min_value=0,
                                           max_value=Lambda, help="Initial number of infected individuals.")
initial_vaccinated = st.sidebar.number_input('Initial Vaccinated Population', value=10000000,
                                             min_value=0, max_value=Lambda, help="Initial number of vaccinated individuals.")
initial_carriers = st.sidebar.number_input('Initial Carriers Population', value=5000, min_value=0,
                                           max_value=Lambda, help="Initial number of carriers.")

# Derived initial conditions
S0 = Lambda - initial_infected - initial_vaccinated - initial_carriers
V0 = initial_vaccinated
C0 = initial_carriers
I0 = initial_infected
R0 = 0
M0 = k * initial_infected / Lambda
gamma0 = 0.8
eta0 = 0.2
xi0 = 0.05

# Time span
tspan = np.linspace(0, 365, 365)

# ODE function
def vaccination_model_dynamic(Y, t, params):
    S, V, C, I, R, M, gamma, eta, xi = Y
    Lambda, mu, beta, epsilon, p0, pmax, D, psi, theta, sigma, delta, rho, d, phi, k, a, alpha_gamma, \
    beta_gamma, alpha_eta, beta_eta, alpha_xi, beta_xi = params

    N = S + V + C + I + R
    p_effective = gamma * (p0 + (pmax - p0) * D * M / (1 + D * M))
    
    dSdt = Lambda - beta * S * (epsilon * C + I) / N - p_effective * S + theta * V + phi * R - mu * S
    dVdt = p_effective * S - (1 - psi) * beta * V * (epsilon * C + I) / N - (theta + mu) * V
    dCdt = beta * (S + (1 - psi) * V) * (epsilon * C + I) / N - (sigma + delta + mu) * C
    dIdt = sigma * C - (rho + mu + d) * I
    dRdt = delta * C + rho * I - (phi + mu) * R
    dMdt = a * (k * I / Lambda - M) + eta * M - xi * M
    dGammaDt = alpha_gamma * (S / N) - beta_gamma * (I / N)
    dEtaDt = alpha_eta * (V / N) - beta_eta * (M / N)
    dXiDt = alpha_xi * M - beta_xi * (V / N)
    
    return [dSdt, dVdt, dCdt, dIdt, dRdt, dMdt, dGammaDt, dEtaDt, dXiDt]

# Parameters tuple
params = (Lambda, mu, beta, epsilon, p0, pmax, D, psi, theta, sigma, delta, rho, d, phi, k, a,
          alpha_gamma, beta_gamma, alpha_eta, beta_eta, alpha_xi, beta_xi)

# Initial conditions vector
Y0 = [S0, V0, C0, I0, R0, M0, gamma0, eta0, xi0]

# Solving the ODEs
solution = odeint(vaccination_model_dynamic, Y0, tspan, args=(params,))

# Extract solutions
S, V, C, I, R, M, gamma, eta, xi = solution.T

# Plotting the results
st.subheader('Model Results')
st.markdown("""
The graphs below represent the population dynamics over time. Each graph shows the number of
individuals in a specific category as the disease spreads and the effects of vaccination take place.
""")

fig, axs = plt.subplots(3, 2, figsize=(12, 12))

axs[0, 0].plot(tspan, S, '-b', linewidth=1.5)
axs[0, 0].set_xlabel('Time (days)')
axs[0, 0].set_ylabel('Susceptible Population (S)')
axs[0, 0].set_title('Susceptible Population (S)')
axs[0, 0].grid(True)

axs[0, 1].plot(tspan, V, '-g', linewidth=1.5)
axs[0, 1].set_xlabel('Time (days)')
axs[0, 1].set_ylabel('Vaccinated Population (V)')
axs[0, 1].set_title('Vaccinated Population (V)')
axs[0, 1].grid(True)

axs[1, 0].plot(tspan, C, '-r', linewidth=1.5)
axs[1, 0].set_xlabel('Time (days)')
axs[1, 0].set_ylabel('Carriers Population (C)')
axs[1, 0].set_title('Carriers Population (C)')
axs[1, 0].grid(True)

axs[1, 1].plot(tspan, I, '-m', linewidth=1.5)
axs[1, 1].set_xlabel('Time (days)')
axs[1, 1].set_ylabel('Infected Population (I)')
axs[1, 1].set_title('Infected Population (I)')
axs[1, 1].grid(True)

axs[2, 0].plot(tspan, R, '-c', linewidth=1.5)
axs[2, 0].set_xlabel('Time (days)')
axs[2, 0].set_ylabel('Recovered Population (R)')
axs[2, 0].set_title('Recovered Population (R)')
axs[2, 0].grid(True)

# Remove the empty subplot
axs[2, 1].axis('off')

plt.tight_layout()
st.pyplot(fig)




st.subheader('Understanding the Outputs')
st.markdown("""
- *Susceptible Population $(S)$*: This represents individuals who are not infected but are at risk of
contracting the disease.
- *Vaccinated Population $(V)$*: Individuals who have received the vaccine. The effectiveness of the
vaccine is reflected in this graph.
- *Carriers Population $(C)$*: People who carry the disease without showing symptoms, contributing to
the disease's spread.
- *Infected Population $(I)$*: The number of individuals who are currently symptomatic and can spread
the disease.
- *Recovered Population $(R)$*: Individuals who have recovered from the disease and gained natural
immunity.
- *Misinformation Index $(M)$*: Reflects the impact of misinformation on public perception
and vaccination rates.
- This model allows you to visualize the intricate balance between disease spread, public health
interventions, and social factors.
Use this tool to gain insights into how different strategies could
influence disease outcomes in real-world scenarios.
""")
st.subheader('References and Further Reading')
st.markdown("""
*[Epidemiology: An Introduction](https://example.com/epidemiology-introduction)*: A
comprehensive resource to understand the basics of epidemiology.
*[The Role of Vaccination in Disease Control](https://example.com/vaccination-disease-control)*: An
article detailing how vaccination impacts disease dynamics.
*[Understanding Misinformation and Its Impact](https://example.com/misinformation-impact)*:
Learn more about how misinformation affects public health efforts.
""")
st.markdown("### Thank you for using the Epidemiological Vaccination Model app. Stay informed, stay safe!")
