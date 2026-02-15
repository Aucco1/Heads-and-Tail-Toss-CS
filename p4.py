import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('fivethirtyeight')

file_path = r"C:\Users\Muhammed\Documents\GitHub\sumagka-msu-pi\GROUP 8 EXCEL FILE.xlsx"
coin_classes = ['1A', '1B', '2', '5A', '5B', '10A', '10B', '20']

max_attempts = 0
extracted_data = []

for cls in coin_classes:
    df = pd.read_excel(file_path, sheet_name=cls, header=[0, 1], index_col=0)
    
    if 'COMBINED' in df.columns.levels[0]:
        target_col = 'COMBINED'
    else:
        target_col = [c for c in df.columns.levels[0] if 'Unnamed' not in str(c)][0]
        
    temp_df = df[target_col][['H', 'T']].copy()
    max_attempts = max(max_attempts, int(temp_df.index.max()))
    extracted_data.append(temp_df)

common_index = range(1, max_attempts + 1)
grand_h = pd.Series(0.0, index=common_index)
grand_t = pd.Series(0.0, index=common_index)

for temp_df in extracted_data:
    temp_df = temp_df.reindex(common_index, method='ffill').fillna(0)
    grand_h += temp_df['H']
    grand_t += temp_df['T']

fig, ax = plt.subplots(figsize=(12, 7), facecolor='#f4f4f4')
fig.suptitle('Requirement #4: Grand Total (All Coin Classes Combined)', fontsize=22, fontweight='bold', color='#333333')

COLOR_H = '#00b4d8'
COLOR_T = '#ff4d6d'

max_y = max(grand_h.max(), grand_t.max())

ax.set_xlim(0, max_attempts + (max_attempts * 0.05))
ax.set_ylim(0, max_y + (max_y * 0.1))
ax.set_xlabel('No. of Attempts', fontsize=14)
ax.set_ylabel('Grand Total Cumulative Count', fontsize=14)

line_h, = ax.plot([], [], label='Grand Total Heads', color=COLOR_H, linewidth=3.5)
line_t, = ax.plot([], [], label='Grand Total Tails', color=COLOR_T, linewidth=3.5)
dot_h, = ax.plot([], [], 'o', color=COLOR_H, markersize=12, markeredgecolor='white', markeredgewidth=2)
dot_t, = ax.plot([], [], 'o', color=COLOR_T, markersize=12, markeredgecolor='white', markeredgewidth=2)

ax.legend(loc='upper left', fontsize=13, facecolor='white', edgecolor='none')
ax.grid(True)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

x_data_full = list(common_index)
y_h_full = grand_h.values
y_t_full = grand_t.values

def update(frame):
    if frame == 0:
        return line_h, line_t, dot_h, dot_t
        
    x_data = x_data_full[:frame]
    y_h = y_h_full[:frame]
    y_t = y_t_full[:frame]
    
    line_h.set_data(x_data, y_h)
    line_t.set_data(x_data, y_t)
    
    current_x = [x_data[-1]]
    dot_h.set_data(current_x, [y_h[-1]])
    dot_t.set_data(current_x, [y_t[-1]])
    
    return line_h, line_t, dot_h, dot_t

ani = animation.FuncAnimation(
    fig, update, 
    frames=max_attempts + 1, 
    interval=50,
    blit=True, 
    repeat=False
)

plt.show()