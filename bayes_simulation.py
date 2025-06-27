import numpy as np
import matplotlib.pyplot as plt

def bayesian_update(current_priors, evidence, likelihood_table, hypotheses):
    """
    Performs a single Bayesian update.

    Args:
        current_priors (np.array): The prior probabilities for each hypothesis.
        evidence (str): The new piece of evidence observed (e.g., 'H' or 'T').
        likelihood_table (dict): A dictionary defining P(Evidence|Hypothesis).
        hypotheses (list): A list of hypothesis names.

    Returns:
        np.array: The posterior probabilities for each hypothesis.
    """
    likelihood_values = np.array([likelihood_table[h][evidence] for h in hypotheses])
    
    # P(E|H) * P(H)
    unnormalized_posterior = likelihood_values * current_priors
    
    
    # P(E) = sum(P(E|H) * P(H))
    p_evidence = np.sum(unnormalized_posterior)
    
    # P(H|E) = [P(E|H) * P(H)] / P(E)
    posterior = unnormalized_posterior / p_evidence
    
    
    return posterior

def run_simulation(initial_priors, evidence_sequence, likelihood_table, hypotheses):
    """
    Runs the full simulation over a sequence of evidence.

    Args:
        initial_priors (np.array): The starting probabilities for the hypotheses.
        evidence_sequence (list): The list of observed evidence.
        likelihood_table (dict): The likelihoods for the simulation.
        hypotheses (list): A list of hypothesis names.

    Returns:
        np.array: A 2D array where each row is the belief state after an evidence piece.
    """
    belief_history = [initial_priors]
    current_beliefs = initial_priors.copy()

    for evidence in evidence_sequence:
        posterior = bayesian_update(current_beliefs, evidence, likelihood_table, hypotheses)
        belief_history.append(posterior)
        current_beliefs = posterior
        
    return np.array(belief_history)

def plot_belief_history(belief_history, hypotheses):
    """
    Visualizes the change in beliefs over time.

    Args:
        belief_history (np.array): The history of belief states from the simulation.
        hypotheses (list): The names of the hypotheses for the plot legend.
    """
    num_flips = np.arange(belief_history.shape[0])

    plt.figure(figsize=(10, 6))
    
    for i, hypothesis in enumerate(hypotheses):
        plt.plot(num_flips, belief_history[:, i], marker='o', linestyle='-', label=f'P({hypothesis})')

    plt.title("Bayesian Belief Updating: Coin Bias Estimation")
    plt.xlabel("Number of Flips (Evidence)")
    plt.ylabel("Probability of Hypothesis")
    plt.xticks(num_flips)
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

def main():
    """
    Main function to set up and run the project.
    """
    # 1. Define the scenario
    hypotheses = ['Fair Coin','Slightly Biased Coin', 'Biased Coin']
    initial_priors = np.array([0.5, 0.5,0.5])
    
    likelihood_table = {
        'Fair Coin': {'H': 0.5, 'T': 0.5},
        'Slightly Biased Coin': {'H': 0.6, 'T': 0.4},
        'Biased Coin': {'H': 0.75, 'T': 0.25}
    }
    
    evidence_sequence = []
    while True:
        evidence= input("Enter the next piece of evidence (H/T) or 'QUIT' to finish: ").strip().upper()
        if evidence == 'QUIT':
            break
        elif evidence in ['H', 'T']:
            evidence_sequence.append(evidence)
        else:
            print("Invalid input. Please enter 'H', 'T', or 'QUIT'.")
        

    # 2. Run the simulation
    belief_history = run_simulation(initial_priors, evidence_sequence, likelihood_table, hypotheses)

    # 3. Visualize the results
    plot_belief_history(belief_history, hypotheses)

    # 4. Print the final summary
    final_beliefs = belief_history[-1]
    print("\nFinal Beliefs after {} flips:".format(len(evidence_sequence)))
    for i, h in enumerate(hypotheses):
        print(f"P({h}): {final_beliefs[i]:.4f}")



if __name__ == "__main__":
    main()