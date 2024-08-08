import sys
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

print("Python exe")
print(sys.executable)

sns.set_context("poster")
sns.set_style("ticks")
plt.rc("axes.spines", top=False, right=False)
fig_path = '../figs/'
golden_ratio = (5**.5 - 1) / 2
width = 12
height = width / golden_ratio

matplotlib.rcParams['figure.figsize'] = [width, height]
matplotlib.rcParams['lines.markersize'] = 5
matplotlib.rcParams["lines.linewidth"] = 0.7
matplotlib.rcParams["lines.markersize"] = 1
matplotlib.rcParams["font.size"] = 7
matplotlib.rcParams["axes.spines.right"] = False
matplotlib.rcParams["axes.spines.top"] = False
