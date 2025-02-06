#  ---1
import pandas as pd
import neurokit2 as nk
import matplotlib.pyplot as plt

# df = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\Shokung_all\rawData\VDO1-1 UnderTheSea\2024-12-14_19-30-39-281346_EA.csv")
#
# data_clean = nk.eda_clean(df["EA"])
# data = nk.eda_phasic(data_clean, sampling_rate=15, method="cvxeda")
# data.plot()
# plt.show()
# print(data)
# #
# ---break


# df = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\20Dec\2\2024-12-20_16-29-44-179315_EA.csv")
# df = pd.read_csv(rf"path")

time = int(input("How Many data paths those you want to plot GRAPH? : "))
i = 1
while i <= time:
    print("No. ", i)
    path = input("EDA file path: ").strip('"')
    df = pd.read_csv(path)

    data_clean = nk.eda_clean(df["EA"])
    data = nk.eda_phasic(data_clean, sampling_rate=15, method="cvxeda")
    data.plot()
    plt.show()
    print(data)
    print("------")

    i = i + 1



# ---2

# df = pd.read_csv(rf"D:\1-BukAILab\EmotiBit\Shokung_all\rawData\VDO2-OOP\2024-12-14_20-04-37-140956_EA.csv")
#
# data_clean = nk.eda_clean(df["EA"])
# data = nk.eda_phasic(data_clean, sampling_rate=15, method="cvxeda")
# data.plot()
# plt.show()
# print(data)