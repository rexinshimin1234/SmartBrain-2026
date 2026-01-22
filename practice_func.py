def calculate_kda(kills,deaths,assists):
    if deaths == 0:
        return float(kills+assists)
    kda_score = (kills + assists) / deaths
    return round(kda_score,1)
player_data = [
    {"k": 5, "d": 2, "a": 10},
    {"k": 8, "d": 0, "a": 5},
    {"k": 0, "d": 5, "a": 0}
]
print("--- 本局战报 ---")

for player in player_data:
    score = calculate_kda(player['k'],player['d'], player['a'])
    print(f"战绩{player['k']}/{player['d']}/{player['a']} -> KDA :{score}")