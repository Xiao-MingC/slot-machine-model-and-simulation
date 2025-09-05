import configs

def main():
    result = configs.spin_reels_from_config(config=configs.REELS_CONFIG_MAIN)
    configs.display(result)
    result_coin = configs.evaluate_paylines_linegame2(result = result,prt=True)
    print(f"\n🏆 Win Coins: {result_coin}\n")
    return result_coin

if __name__ == "__main__":
    main()  
