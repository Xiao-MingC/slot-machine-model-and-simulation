import configs

if __name__ == "__main__":
    configs.simulate_advanced_with_graphs(
        game= "waygame",
        n_spins=1000,         # 每組模擬幾次Spin
        n_simulations=1     # 模擬組數(用以統計破產機率)
    )
