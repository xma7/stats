import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import binom_test

def simulate_coin_flips(n_flips, n_trials, prob_heads):
    trials = np.random.rand(n_trials, n_flips) < prob_heads
    return trials.mean(axis=1)

def main():
    st.title('Coin Flip Simulation')

    # Input parameters
    prob_heads = st.sidebar.slider('Probability of Heads', min_value=0.0, max_value=1.0, value=0.5)
    n_trials = int(st.sidebar.text_input('Number of Trials', value='1000'))
    n_flips = int(st.sidebar.text_input('Number of Coin Flips per Trial', value='1000'))
    alpha = float(st.sidebar.text_input('Alpha (Significance Level)', value='0.05'))

    # Button to run simulation
    run_simulation = st.button('Run Simulation')

    if run_simulation:
        # Perform simulation and store results in session state
        expected_values = simulate_coin_flips(n_flips, n_trials, prob_heads)
        st.session_state['results'] = expected_values
        st.session_state['last_run'] = {'n_flips': n_flips, 'n_trials': n_trials, 'prob_heads': prob_heads, 'alpha': alpha}

    if 'results' in st.session_state:
        # Display results from the latest simulation
        results = st.session_state['results']
        last_run = st.session_state['last_run']
        
        # Plotting
        fig, ax = plt.subplots()
        
        mean_value = results.mean()
        ax.axvline(mean_value, color="#FF6F61", linestyle='--', label=f'Mean: {mean_value:.4f}')

        sns.histplot(results, kde=True, color="teal", stat="density", ax=ax)
        ax.set_title(f'Distribution of Expected Value of Heads\n{last_run["n_flips"]} Flips, {last_run["n_trials"]} Trials')
        ax.set_xlabel('Expected Value of Heads')
        ax.set_ylabel('Density')
        ax.legend()
        st.pyplot(fig)

        # Correct p-value calculation: x is the count of heads, not the mean proportion
        p_values = [binom_test(x, n=last_run['n_flips'], p=0.5) for x in (results * last_run['n_flips'])]

        # Calculate the average p-value from all trials as a summary statistic
        average_p_value = np.mean(p_values)

        # Decide if the coin is fair or unfair based on the average p-value
        fair_unfair = "unfair" if average_p_value < last_run['alpha'] else "fair"

        # Display the alpha level, average p-value, and conclusion using Markdown for formatting
        st.markdown(f"**Significance Level (Alpha): {last_run['alpha']}**")
        st.markdown(f"**Average P-Value from Simulation: {average_p_value:.4f}**")
        st.markdown(f"**Conclusion: The coin is {fair_unfair}.**")

    else:
        st.info("Adjust parameters if needed and click 'Run Simulation' to see results.")

if __name__ == '__main__':
    main()
