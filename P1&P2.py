import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


plt.style.use('fivethirtyeight')

file_path = r"C:\Users\Muhammed\Documents\GitHub\sumagka-msu-pi\GROUP 8 EXCEL FILE.xlsx"


df = pd.read_excel(file_path, sheet_name='#1 & #2', skiprows=2, header=None)
df.columns = [
    'Attempts', '1A_Raw_H', '1A_Raw_T', '1A_Cum_H', '1A_Cum_T',
    '10B_Raw_H', '10B_Raw_T', '10B_Cum_H', '10B_Cum_T', 'Combine_H', 'Combine_T'
]


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6), facecolor='#f4f4f4')
fig.suptitle('Coin Toss Experiment: Cumulative Results', fontsize=22, fontweight='bold', color='#333333')


COLOR_H = '#00b4d8' 
COLOR_T = '#ff4d6d'  


max_attempts = df['Attempts'].max() + 2
max_y1 = max(df['1A_Cum_H'].max(), df['1A_Cum_T'].max()) + 5
max_y2 = max(df['10B_Cum_H'].max(), df['10B_Cum_T'].max()) + 5
max_y3 = max(df['Combine_H'].max(), df['Combine_T'].max()) + 5


def setup_axis(ax, title, max_y):
    ax.set_xlim(0, max_attempts)
    ax.set_ylim(0, max_y)
    ax.set_title(title, fontsize=15, fontweight='bold', color='#444444')
    ax.set_xlabel('No. of Attempts', fontsize=12)
    ax.set_ylabel('Cumulative Count', fontsize=12)
    
    
    line_h, = ax.plot([], [], label='Heads', color=COLOR_H, linewidth=3)
    line_t, = ax.plot([], [], label='Tails', color=COLOR_T, linewidth=3)

    
    dot_h, = ax.plot([], [], 'o', color=COLOR_H, markersize=10, markeredgecolor='white', markeredgewidth=1.5)
    dot_t, = ax.plot([], [], 'o', color=COLOR_T, markersize=10, markeredgecolor='white', markeredgewidth=1.5)
    
    
    ax.legend(loc='upper left', frameon=True, fontsize=11, facecolor='white', edgecolor='none')
    return line_h, line_t, dot_h, dot_t


l1_h, l1_t, d1_h, d1_t = setup_axis(ax1, 'Graph 1: 1A Coin Class', max_y1)
l2_h, l2_t, d2_h, d2_t = setup_axis(ax2, 'Graph 2: 10B Coin Class', max_y2)
l3_h, l3_t, d3_h, d3_t = setup_axis(ax3, 'Combined (1A + 10B)', max_y3)


plt.tight_layout(rect=[0, 0.03, 1, 0.92])



def update(frame):
    if frame == 0: return l1_h, l1_t, d1_h, d1_t, l2_h, l2_t, d2_h, d2_t, l3_h, l3_t, d3_h, d3_t
    
    x_data = df['Attempts'].iloc[:frame]
    current_x = [df['Attempts'].iloc[frame-1]] 

    l1_h.set_data(x_data, df['1A_Cum_H'].iloc[:frame])
    l1_t.set_data(x_data, df['1A_Cum_T'].iloc[:frame])
    d1_h.set_data(current_x, [df['1A_Cum_H'].iloc[frame-1]])
    d1_t.set_data(current_x, [df['1A_Cum_T'].iloc[frame-1]])
    

    l2_h.set_data(x_data, df['10B_Cum_H'].iloc[:frame])
    l2_t.set_data(x_data, df['10B_Cum_T'].iloc[:frame])
    d2_h.set_data(current_x, [df['10B_Cum_H'].iloc[frame-1]])
    d2_t.set_data(current_x, [df['10B_Cum_T'].iloc[frame-1]])
    
  
    l3_h.set_data(x_data, df['Combine_H'].iloc[:frame])
    l3_t.set_data(x_data, df['Combine_T'].iloc[:frame])
    d3_h.set_data(current_x, [df['Combine_H'].iloc[frame-1]])
    d3_t.set_data(current_x, [df['Combine_T'].iloc[frame-1]])
    
    return l1_h, l1_t, d1_h, d1_t, l2_h, l2_t, d2_h, d2_t, l3_h, l3_t, d3_h, d3_t


ani = animation.FuncAnimation(
    fig, update, 
    frames=len(df)+1, 
    interval=60,      
    blit=True, 
    repeat=False
)

plt.show()