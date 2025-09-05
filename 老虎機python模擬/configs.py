import numpy
import random
import pandas
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt


WILD = "W" #賴子
SCATTER = "S"
HEIGTH = 3 #輪盤高度
BETTING_COST = {"linegame1" : 1 , "linegame2" : 1 ,"waygame": 50} #單次注額
STARTING_COIN = 30000 #初始資金
FREE_GAMES_TABLE = {3: 10 , 4: 15 , 5 : 20} #免費遊戲次數

PAYTABLE = { 
    "K": {3: 5, 4: 30, 5: 100},
    "Q": {3: 5, 4: 25, 5: 100},
    "J": {3: 5, 4: 20, 5: 75},
    "10": {3: 5, 4: 20, 5: 75},
    "9": {3: 5, 4: 10, 5: 50},
    "S": {3: 50, 4: 0, 5: 0}
} #賠付表(linegame1 , waygame)

PAYTABLE_L2 = {
    "K": {3: 5, 4: 30, 5: 100},
    "Q": {3: 5, 4: 25, 5: 100},
    "J": {3: 5, 4: 20, 5: 75},
    "10": {3: 5, 4: 20, 5: 75},
    "9": {3: 5, 4: 10, 5: 50},
    "S": {3: 2, 4: 2, 5: 2}
} #賠付表(linegame2)

PAYLINES = [
      [0, 0, 0, 0, 0],      # 上橫
    # [1, 1, 1, 1, 1],      # 中橫
    # [2, 2, 2, 2, 2],      # 下橫
    # [0, 1, 2, 1, 0],     # V
    # [2, 1, 0, 1, 2]   # 倒 V
] #下注line

REELS_CONFIG =numpy.array([
    ["K",   "W",    "W",    "W",    "W"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"],
    ["K",   "S",    "S",    "S",    "9"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["10",  "9",    "9",    "9",    "9"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"],
    ["J",   "J",    "J",    "J",    "J"],
    ["10",  "J",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"]
]) #滾輪設置(linegame1 , waygame)

REELS_CONFIG_MAIN =numpy.array([
    ["K",   "W",    "W",    "W",    "W"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"],
    ["S",   "S",    "S",    "S",    "S"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["10",  "9",    "9",    "9",    "9"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"],
    ["J",   "J",    "J",    "J",    "J"],
    ["10",  "J",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"]
]) #滾輪設置(linegame2)

REELS_CONFIG_FREE =numpy.array([
    ["K",   "W",    "W",    "W",    "W"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"],
    ["S",   "S",    "S",    "S",    "S"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "Q",    "Q",    "Q",    "Q"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["10",  "9",    "9",    "9",    "9"],
    ["Q",   "K",    "K",    "K",    "K"],
    ["J",   "W",    "W",    "W",    "W"],
    ["10",  "J",    "J",    "J",    "J"],
    ["9",  "10",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",    "9"],
    ["J",   "J",    "J",    "J",    "J"],
    ["10",  "J",   "10",   "10",   "10"],
    ["9",   "9",    "9",    "9",   None]
])#滾輪設置(freegame)


# ----------- 函數區 ----------- #

def spin_reels_from_config(config): #單次抽獎(config:滾輪設置)
    cols = len(config[0,:])
    rows = [numpy.count_nonzero(config[:,_]!= None) for _ in range(cols)]
    start_indices = [random.randint(0, rows[_] - 1) for _ in range(cols)]
    result = [[None for _ in range(cols)] for _ in range(HEIGTH) ]
    for col in range(cols):
        for row in range(HEIGTH):
            index = (start_indices[col] + row) % rows[col]
            result[row][col] = config[index][col]
    return result

def display(result): #打印結果
    print("🎰 Slot Machine Result :")
    for row in result:
        print(" ".join(row))

def matching(symbols): #單線符號連線計數
    base_symbol = None
    match_count = 0
    for s in symbols:
        if s == SCATTER:
                break  
        if s == WILD:
            match_count += 1
        elif base_symbol is None:
             base_symbol = s
             match_count += 1
        elif s == base_symbol:
                match_count += 1
        else:
            break
    return base_symbol,match_count

def free_game(ini,config,prt = False): #免費遊戲(ini:初始免費遊戲次數,config:滾輪設定,prt:是否打印結果)
    score = 0
    while ini != 0  :
        payout_free = 0
        ini -= 1
        result = spin_reels_from_config(config)
        if prt :
            display(result = result)
        symbols = []
        for idx,line in enumerate(PAYLINES) :
            for col in range(len(result[1])):
                row = line[col]
                symbols.append(result[row][col])
        symbols = numpy.array(symbols).reshape(len(PAYLINES),len(result[1]))
        for _ in range(len(symbols)):
            base_symbol,match_count = matching(symbols[_]) 
            if base_symbol and base_symbol in PAYTABLE_L2:
                payout_free = PAYTABLE_L2[base_symbol].get(match_count, 0)
            if payout_free > 0:
                if prt :
                    print(f"✅ Line {_+1}: {base_symbol} x {match_count} → coin +{payout_free}")
                score += payout_free
        scatter_count = sum(row.count(SCATTER) for row in result)
        if scatter_count >= 3:
            scatter_score = PAYTABLE_L2[SCATTER].get(scatter_count, 0)
            free_games_add = FREE_GAMES_TABLE.get(scatter_count,0)
            ini += free_games_add
            if prt :
                print(f"✨ Scatter Bonus: {scatter_count} scatters → +{scatter_score} game → +{free_games_add}")
            score += scatter_score
    if prt :
        print(f"✨ Scatter Bonus Total Win ✨: {score}")
    return score

def evaluate_paylines_test(result,prt = False): #linegame測試滾輪設定之rtp，可忽略
    coin = 0 
    symbols = []
    payout = 0
    for idx,line in enumerate(PAYLINES) :
        for col in range(len(result[1])):
            row = line[col]
            symbols.append(result[row][col])
    symbols = numpy.array(symbols).reshape(len(PAYLINES),len(result[1]))
    for _ in range(len(symbols)):
        base_symbol,match_count = matching(symbols[_]) 
        if base_symbol and base_symbol in PAYTABLE_L2:
            payout = PAYTABLE_L2[base_symbol].get(match_count, 0)
        if payout > 0:
            if prt :
                print(f"✅ Line {_+1}: {base_symbol} x {match_count} → coin +{payout}")
            coin += payout
    scatter_count = sum(row.count(SCATTER) for row in result)
    if scatter_count >= 3:
        scatter_score = PAYTABLE_L2[SCATTER].get(scatter_count, 0)
        if prt : 
            print(f"✨ Scatter Bonus: {scatter_count} scatters → +{scatter_score}")
        coin += scatter_score
    return coin



def evaluate_paylines_linegame1(result,prt=False): #linegame1 對獎 (prt:是否打印結果)
    coin = 0 
    symbols = []
    payout = 0
    for idx,line in enumerate(PAYLINES) :
        for col in range(len(result[1])):
            row = line[col]
            symbols.append(result[row][col])
    symbols = numpy.array(symbols).reshape(len(PAYLINES),len(result[1]))
    for _ in range(len(symbols)):
        base_symbol,match_count = matching(symbols[_]) 
        if base_symbol and base_symbol in PAYTABLE:
            payout = PAYTABLE[base_symbol].get(match_count, 0)
        if payout > 0:
            if prt :
                print(f"✅ Line {_+1}: {base_symbol} x {match_count} → coin +{payout}")
            coin += payout
    scatter_count = sum(row.count(SCATTER) for row in result)
    if scatter_count >= 3:
        scatter_score = PAYTABLE[SCATTER].get(scatter_count, 0)
        if prt :
            print(f"✨ Scatter Bonus: {scatter_count} scatters → +{scatter_score}")
        coin += scatter_score
    return coin

def evaluate_paylines_linegame2(result,prt = False): #linegame2 對獎 (prt:是否打印結果)
    coin = 0
    symbols = []
    payout = 0
    for idx,line in enumerate(PAYLINES) :
        for col in range(len(result[1])):
            row = line[col]
            symbols.append(result[row][col])
    symbols = numpy.array(symbols).reshape(len(PAYLINES),len(result[1]))
    for _ in range(len(symbols)):
        base_symbol,match_count = matching(symbols[_]) 
        if base_symbol and base_symbol in PAYTABLE_L2:
            payout = PAYTABLE_L2[base_symbol].get(match_count, 0)
        else: payout = 0
        if payout > 0:
            if prt :
                print(f"✅ Line {_+1}: {base_symbol} x {match_count} → coin +{payout}")
            coin += payout
    scatter_count = sum(row.count(SCATTER) for row in result)
    if scatter_count >= 3:
        scatter_score = PAYTABLE_L2[SCATTER].get(scatter_count, 0)
        if prt :
            print(f"✨ Scatter Bonus: {scatter_count} scatters → +{scatter_score}")
            print(f"✨ Scatter Bonus Free Game ✨")
            print()
        coin += scatter_score
        free_game_score = free_game(ini = FREE_GAMES_TABLE.get(scatter_count) ,config = REELS_CONFIG_FREE,prt=prt)
        coin += free_game_score
    return coin

     


def evaluate_paylines_waygame(result,prt = False): #waygame 對獎 (prt:是否打印結果)
    coin = 0
    symbols_all = numpy.unique(REELS_CONFIG)
    symbols = symbols_all[~numpy.isin(symbols_all,[WILD,SCATTER])]
    count = pandas.DataFrame(index=symbols,columns=[ i for i in range(len(result[1]))])
    for _ in symbols_all :
        for __ in range(len(result[1])):
            count.loc[_, __] = (numpy.array(result)[:,__]== _).sum()
    count.loc[symbols] += count.loc[WILD]
    Scoreboard = {}
    for _ in symbols:
        ini = 1 ; t = 0
        while t<5 and count.loc[_].iloc[t] != 0 :
            ini *= count.loc[_].iloc[t]
            t += 1
        Scoreboard[_] = [t,ini]
        if _ and _ in PAYTABLE:
             payout = PAYTABLE[_].get(Scoreboard[_][0], 0)
        else: payout = 0
        if payout > 0:
            if prt :
                print(f"✅ {Scoreboard[_][1]} Line : {Scoreboard[_][0]} x {_}  → coin +{payout*Scoreboard[_][1]}")
            coin += payout*Scoreboard[_][1]
    scatter_count = sum(row.count(SCATTER) for row in result)

    if scatter_count >= 3:
        scatter_score = PAYTABLE[SCATTER].get(scatter_count, 0)
        if prt :
            print(f"✨ Scatter Bonus: {scatter_count} scatters → +{scatter_score} coin")
            print()
        coin += scatter_score
    return coin 

def simulate_advanced_with_graphs(game,n_spins=1000, n_simulations=1): #模擬試驗(gma:玩哪一種遊戲,spin:玩幾次,n_simulations:幾組)
    plt.rcParams['font.family'] = 'Heiti TC'
    plt.rcParams['axes.unicode_minus'] = False 
    total_returns = []
    total_rtp = []
    win_rates = []
    average_wins = []
    bankrupt_count = 0
    betting_cost = BETTING_COST.get(game,0)
    if game == "linegame1" :
        setting_config = REELS_CONFIG 
        evaluate_function = evaluate_paylines_linegame1
    elif game == "linegame2" :
        setting_config = REELS_CONFIG_MAIN
        evaluate_function = evaluate_paylines_linegame2
    elif game == "waygame" :
        setting_config = REELS_CONFIG
        evaluate_function = evaluate_paylines_waygame
    elif game == "test" :
        setting_config = REELS_CONFIG_FREE
        evaluate_function = evaluate_paylines_test

    # 用來畫圖（只用第一組）
    coin_history = []
    profit_history = []
    rtp_history = []
    for sim in range(n_simulations):
        current_coin = STARTING_COIN
        win_count = 0
        total_win_amount = 0
        spins_done = 0

        for i in range(n_spins):
            spins_done += 1
            result = spin_reels_from_config(config=setting_config)
            win_coin = evaluate_function(result=result)
            #win_coin = configs.evaluate_paylines_linegame1(result=result)
            delta = win_coin - betting_cost
            current_coin += delta

            # 只紀錄第一組的圖表資料
            if sim == 0:
                coin_history.append(current_coin)
                if delta != -betting_cost:
                    profit_history.append(delta+betting_cost)
                rtp = (current_coin - STARTING_COIN + spins_done*betting_cost) / (spins_done*betting_cost) * 100
                rtp_history.append(rtp)

            # 判斷贏／輸
            if delta > 0:
                win_count += 1
                total_win_amount += delta
        
            # 若破產
            if current_coin <= 0:
                bankrupt_count += 1
                break
        total_return = current_coin - STARTING_COIN
        rtp = (total_return + (spins_done*betting_cost)) / (spins_done*betting_cost) * 100
        total_returns.append(total_return)
        total_rtp.append(rtp)
        win_rates.append(win_count / spins_done)
        average_wins.append((total_win_amount / win_count) if win_count > 0 else 0)

    # 📊 統計輸出
    print(f"\n📊 模擬報告 (共 {n_simulations} 次模擬，每次 {n_spins} Spins)")
    print(f"💰 初始資金: {STARTING_COIN}")
    print(f"📈 平均 RTP: {numpy.mean(total_rtp):.2f}%")
    print(f"🎯 平均中獎率: {numpy.mean(win_rates)*100:.2f}%")
    print(f"💸 平均贏得金額: {numpy.mean(average_wins):.2f} coin")
    print(f"☠️ 破產次數: {bankrupt_count} / {n_simulations} → 破產率: {(bankrupt_count/n_simulations)*100:.2f}%")

    # # 📈 畫圖區

    # ===== 圖1：資金變化曲線 =====
    plt.figure(figsize=(10, 6))
    plt.plot(coin_history, label="資金")
    plt.title("資金曲線")
    plt.xlabel("Spin 次數")
    plt.ylabel("Coin")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # ===== 圖2：回報直方圖 =====
    if game in ["linegame1"] :
        # 計算每個獲利值出現的次數
        profit_counter = Counter(profit_history)

        # 按照獲利值排序
        profit_values = sorted(profit_counter.keys())
        counts = [profit_counter[val] for val in profit_values]

        # 繪製長條圖
        x_vals = [str(x) for x in sorted(profit_counter.keys())]
        y_vals = [profit_counter[int(x)] for x in x_vals]

        # 畫計次圖
        plt.figure(figsize=(10, 6))
        plt.bar(x_vals, y_vals, color="skyblue", edgecolor="black")
        plt.title("單次獲利計次圖（僅顯示樣本空間）")
        plt.xlabel("單次獲利 (coin)")
        plt.ylabel("出現次數")
        plt.xticks(rotation=45)  # 可選：讓 x 軸標籤傾斜，避免擠在一起
        plt.tight_layout()
        plt.show()

        values, counts = numpy.unique(profit_history, return_counts=True)
        percentages = counts / counts.sum() * 100

        table_data = []
        for v, c, p in zip(values, counts, percentages):
            table_data.append([v, c, f"{p:.1f}%"])

        fig, ax = plt.subplots(figsize=(6, len(values)*0.4 + 1))  # 高度隨資料行數調整
        ax.axis('off')  # 不顯示軸線

        table = ax.table(cellText=table_data,
                        colLabels=["獲利值", "次數", "百分比"],
                        cellLoc='center',
                        colLoc='center',
                        loc='center')

        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1, 1.5)  # 調整表格大小

        plt.title("單次獲利分布表")
        plt.tight_layout()
        plt.show()
    
    elif game in ["waygame" ,"linegame2"] :
        plt.figure(figsize=(10, 6))
        # 畫直方圖和 KDE（曲線分開畫）
        sns.histplot(profit_history, bins=40, color='darkblue', edgecolor='black', stat='count', kde=False)

        plt.title("單次獲利分布")
        plt.xlabel("單次獲利 (coin)")
        plt.ylabel("次數")
        plt.tight_layout()
        plt.show()

    # ===== 圖3：RTP變化圖 =====
    #print(numpy.mean(rtp_history))
    plt.figure(figsize=(10, 6))
    plt.plot(rtp_history, color="orange")
    plt.title("RTP 隨 Spin 次數變化")
    plt.xlabel("Spin 次數")
    plt.ylabel("RTP (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
