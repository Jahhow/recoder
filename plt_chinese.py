# 讓 matplotlib 可以顯示中文
# how to use: from plt_chinese import plt

from matplotlib.font_manager import fontManager
import matplotlib.pyplot as plt
import matplotlib
plt.style.use('seaborn') # 有需要設定style則要在更新font之前設定
fontManager.addfont('D:/CSC-code/TaipeiSansTCBeta-Regular.ttf')
matplotlib.rc('font', family='Taipei Sans TC Beta')