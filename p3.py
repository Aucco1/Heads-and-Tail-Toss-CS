import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


plt.style.use('fivethirtyeight')

file_path = r"C:\Users\Muhammed\Documents\GitHub\sumagka-msu-pi\GROUP 8 EXCEL FILE.xlsx"
coin_classes = ['1A', '1B', '2', '5A', '5B', '10A', '10B', '20']

data_dict = {}
max_frames = 0

for cls in coin_classes:
    df = pd.read_excel(file_path, sheet_name=cls, header=[0, 1], index_col=0)
    
    if 'COMBINED' in df.columns.levels[0]:
        target_col = 'COMBINED'
    else:
        target_col = [c for c in df.columns.levels[0] if 'Unnamed' not in str(c)][0]
        
    attempts = df.index.values
    h_data = df[target_col]['H'].values
    t_data = df[target_col]['T'].values
    
    data_dict[cls] = {
        'attempts': attempts,
        'h_data': h_data,
        't_data': t_data,
        'length': len(attempts)
    }
    if len(attempts) > max_frames:
        max_frames = len(attempts)

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10), facecolor='#f4f4f4')
fig.suptitle('Requirement #3: All Coin Classes Animated Race', fontsize=24, fontweight='bold', color='#333333')
axes = axes.flatten()

COLOR_H = '#00b4d8'  
COLOR_T = '#ff4d6d'  


lines_h, lines_t, dots_h, dots_t = [], [], [], []


for i, cls in enumerate(coin_classes):
    ax = axes[i]
    max_x = data_dict[cls]['attempts'].max() if data_dict[cls]['length'] > 0 else 100
    max_y = max(data_dict[cls]['h_data'].max(), data_dict[cls]['t_data'].max()) if data_dict[cls]['length'] > 0 else 100
    
    ax.set_xlim(0, max_x + (max_x * 0.05))
    ax.set_ylim(0, max_y + (max_y * 0.1)) 
    
    ax.set_title(f'Class {cls}', fontsize=16, fontweight='bold', color='#444444')
    ax.set_xlabel('No. of Attempts', fontsize=11)
    ax.set_ylabel('Cumulative Count', fontsize=11)
    
    
    lh, = ax.plot([], [], label='Heads', color=COLOR_H, linewidth=2.5)
    lt, = ax.plot([], [], label='Tails', color=COLOR_T, linewidth=2.5)
    dh, = ax.plot([], [], 'o', color=COLOR_H, markersize=8, markeredgecolor='white', markeredgewidth=1.5)
    dt, = ax.plot([], [], 'o', color=COLOR_T, markersize=8, markeredgecolor='white', markeredgewidth=1.5)
    
    ax.legend(loc='upper left', fontsize=10, facecolor='white', edgecolor='none')
    ax.grid(True)
    
    lines_h.append(lh)
    lines_t.append(lt)
    dots_h.append(dh)
    dots_t.append(dt)


plt.tight_layout(rect=[0, 0.03, 1, 0.95])


def update(frame):
    
    if frame == 0:
        return lines_h + lines_t + dots_h + dots_t
        
    for i, cls in enumerate(coin_classes):
   
        current_frame = min(frame, data_dict[cls]['length'])
        
        if current_frame == 0:
            continue
            
        x_data = data_dict[cls]['attempts'][:current_frame]
        y_h = data_dict[cls]['h_data'][:current_frame]
        y_t = data_dict[cls]['t_data'][:current_frame]
        
       
        lines_h[i].set_data(x_data, y_h)
        lines_t[i].set_data(x_data, y_t)
        
        
        current_x = [x_data[-1]]
        dots_h[i].set_data(current_x, [y_h[-1]])
        dots_t[i].set_data(current_x, [y_t[-1]])
        
    return lines_h + lines_t + dots_h + dots_t


ani = animation.FuncAnimation(
    fig, update, 
    frames=max_frames + 1, 
    interval=60,       
    blit=True, 
    repeat=False
)


plt.show()