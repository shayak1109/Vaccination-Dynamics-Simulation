# 🧬 Vaccination Dynamics Simulation  
*A Behavioral Epidemiological Model with Application to Meningitis Spread in Nigeria*

---

## 📖 Overview  
This project extends an **epidemiological vaccination model** to study the impact of **social influence**, **healthcare accessibility**, and **misinformation** on vaccination dynamics.  
The simulation combines concepts from behavioral epidemiology and disease modeling to analyze how these factors affect disease spread, vaccination rates, and public health outcomes.

The model is implemented in **Python** and visualized using a **Streamlit web application**, allowing users to interactively explore how different social and healthcare parameters influence epidemic dynamics.

---

## 🧩 Model Summary  
Traditional vaccination models often focus purely on biological and demographic factors.  
Our model introduces three new behavioral and societal indices to bridge that gap:

- **Healthcare Access Index (γ):**  
  Represents the variability in access to healthcare services. Better access increases vaccination and recovery rates.

- **Social Influence Index (η):**  
  Captures how social pressure, peer behavior, and community sentiment impact individuals’ decisions to vaccinate.

- **Misinformation Index (ξ):**  
  Models the negative influence of misinformation and distrust in healthcare on vaccination campaigns.

These indices are integrated into a **modified SIRVC model** (Susceptible, Infected, Recovered, Vaccinated, Carriers).

---

## ⚙️ Implementation Details  

**Tech Stack:**
- Python 🐍  
- Streamlit 🌐  
- NumPy, SciPy, Matplotlib for computation and visualization  

**Key Components:**
- `odeint()` solver from SciPy to compute the system of coupled differential equations.  
- Streamlit dashboard for parameter tuning and live graph updates.  
- MATLAB used for validating earlier simulations and reference comparisons.

---

## 🧮 Model Parameters  
You can adjust the following parameters in the Streamlit sidebar:
- Transmission Rate (`β`)
- Vaccine Effectiveness (`ψ`)
- Waning Immunity Rates (`θ`, `ϕ`)
- Social Influence Coefficients (`αη`, `βη`)
- Healthcare Access Coefficients (`αγ`, `βγ`)
- Misinformation Spread Rates (`αξ`, `βξ`)
- Memory Length (`a`) and Information Coverage (`k`)

---

## 🚀 Running the Simulation  

### 1️⃣ Install dependencies  
```bash
pip install -r requirements.txt
```

### 2️⃣ Run the Streamlit app
```bash
streamlit run main.py
```

### 3️⃣ Adjust parameters
Use the sidebar to modify inputs such as infection rate, vaccination rate, or social influence parameters.
The plots update automatically in real time to show how the disease dynamics change.


## 📊 Outputs and Visualization

The Streamlit dashboard displays:

Population Dynamics:

- Susceptible (S)

- Vaccinated (V)

- Carriers (C)

- Infected (I)

- Recovered (R)

Behavioral Indices:

- Healthcare Access (γ)

- Social Influence (η)

- Misinformation (ξ)

## 🧩 Key Observations:

- Improved healthcare access and positive social influence enhance vaccination success.

- Misinformation significantly hampers vaccination rates and prolongs outbreaks.

- Integrated public health efforts addressing these three factors yield better epidemic control.

## 🧠 Key Takeaways

- Healthcare Access Matters: Better access leads to faster vaccination and recovery rates.

- Social Influence Can Help or Hurt: Communities with strong positive social influence show higher vaccine uptake.

- Misinformation is a Major Threat: Countering misinformation is critical for maintaining public trust in vaccines.

- Integrated Strategies Work Best: A mix of improved healthcare infrastructure, social awareness, and accurate information is essential for epidemic control.

## 🖥️ Project Structure
```bash
📁 Vaccination-Dynamics-Simulation
 ├── main.py              # Streamlit application
 ├── requirements.txt      # Dependencies
 ├── Math_Report.pdf       # Contains project report
 ├── Math_paper.pdf        # Graph outputs
 └── README.md             # This documentation file

```

## 👥 Contributors

- **Supervisor:** Dr. Nivya Muchikel, Asst. Professor, RVCE, Bangalore

- Pranav Kumar

- Shayak Bose

- Siddharth Ranganatha

- Suneel Nayak

## 🧾 References  
Key literature referenced in this work:

1. B. Buonomo and R. Della Marca, *A Behavioural Vaccination Model with Application to Meningitis Spread in Nigeria*, Applied Mathematical Modelling, 2023.  
2. N. E. Basta et al., *Meningococcal Carriage within Households in the African Meningitis Belt*, J. Infect., 2018.  
3. T. J. Irving et al., *Modelling Meningococcal Meningitis in the African Meningitis Belt*, Epidemiol. Infect., 2012.  
4. F. Agusto and M. Leite, *Optimal Control and Cost–Effective Analysis of the 2017 Meningitis Outbreak in Nigeria*, Infect. Dis. Model., 2019.  
5. L. Perra et al., *Behaviour–Disease Models*, PLoS ONE, 2011.  

For the **complete reference list**, please refer to the [`Math_paper.pdf`](Math_paper.pdf) file.

