import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import warnings

warnings.filterwarnings('ignore') 
plt.style.use('fivethirtyeight')

file_path = r"C:\Users\Muhammed\Documents\GitHub\sumagka-msu-pi\GROUP 8 EXCEL FILE.xlsx"
df = pd.read_excel(file_path, sheet_name='#5 TABLE', header=None)

classes_row = df.iloc[1].fillna('').astype(str).str.strip()
sub_headers = df.iloc[2].fillna('').astype(str).str.strip().str.upper()

attempt_cols = [i for i, v in enumerate(sub_headers) if 'ATTEMPT' in str(v)]
extracted_data = {}
valid_classes = ['1A', '1B', '2', '5A', '5B', '10A', '10B', '20']

for i, a_idx in enumerate(attempt_cols):
    cls = ''
    for offset in range(5):
        if a_idx + offset < len(classes_row) and classes_row[a_idx + offset] in valid_classes:
            cls = classes_row[a_idx + offset]
            break
        if a_idx - offset >= 0 and classes_row[a_idx - offset] in valid_classes:
            cls = classes_row[a_idx - offset]
            break
            
    if not cls: continue
    
    end_idx = attempt_cols[i+1] if i + 1 < len(attempt_cols) else len(sub_headers)
    target_idx = -1
    
    for j in range(a_idx, end_idx):
        if 'COMBINE' in str(sub_headers[j]):
            target_idx = j
            break
            
    if target_idx == -1:
        for j in range(end_idx - 1, a_idx - 1, -1):
            if 'GROUP' in str(sub_headers[j]):
                target_idx = j
                break
                
    if target_idx != -1:
        attempts = pd.to_numeric(df.iloc[4:, a_idx], errors='coerce')
        h_data = pd.to_numeric(df.iloc[4:, target_idx], errors='coerce')
        t_data = pd.to_numeric(df.iloc[4:, target_idx + 1], errors='coerce')
        
        valid = attempts.notna() & h_data.notna() & t_data.notna()
        if valid.sum() > 0:
            extracted_data[cls] = {
                'attempts': list(attempts[valid].values),
                'H': list(h_data[valid].values),
                'T': list(t_data[valid].values)
            }

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10), facecolor='#f4f4f4')
fig.suptitle('Requirement #5: TABLE Surface - All Coin Classes', fontsize=24, fontweight='bold', color='#333333')
axes = axes.flatten()

COLOR_H = '#00b4d8'
COLOR_T = '#ff4d6d'

lines_h, lines_t, dots_h, dots_t = [], [], [], []
classes_list = list(extracted_data.keys())
max_frames = 0

for i, cls in enumerate(classes_list):
    ax = axes[i]
    data = extracted_data[cls]
    
    max_x = len(data['attempts'])
    max_y = max(max(data['H']), max(data['T']))
    if max_x > max_frames: 
        max_frames = max_x
    
    ax.set_xlim(0, max_x + (max_x * 0.05))
    ax.set_ylim(0, max_y + (max_y * 0.1))
    ax.set_title(f'Class {cls}', fontsize=16, fontweight='bold')
    ax.set_xlabel('No. of Attempts', fontsize=11)
    ax.set_ylabel('Cumulative Count', fontsize=11)
    
    lh, = ax.plot([], [], color=COLOR_H, linewidth=2.5, label='Heads')
    lt, = ax.plot([], [], color=COLOR_T, linewidth=2.5, label='Tails')
    dh, = ax.plot([], [], 'o', color=COLOR_H, markersize=8, markeredgecolor='white')
    dt, = ax.plot([], [], 'o', color=COLOR_T, markersize=8, markeredgecolor='white')
    
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True)
    
    lines_h.append(lh)
    lines_t.append(lt)
    dots_h.append(dh)
    dots_t.append(dt)

for j in range(len(classes_list), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

def update(frame):
    if frame == 0:
        return lines_h + lines_t + dots_h + dots_t
        
    for idx, cls in enumerate(classes_list):
        d = extracted_data[cls]
        cf = min(frame, len(d['attempts']))
        if cf == 0: continue
        
        x = d['attempts'][:cf]
        yh = d['H'][:cf]
        yt = d['T'][:cf]
        
        lines_h[idx].set_data(x, yh)
        lines_t[idx].set_data(x, yt)
        dots_h[idx].set_data([x[-1]], [yh[-1]])
        dots_t[idx].set_data([x[-1]], [yt[-1]])
        
    return lines_h + lines_t + dots_h + dots_t

ani = animation.FuncAnimation(
    fig, update, 
    frames=max_frames + 1, 
    interval=60, 
    blit=True, 
    repeat=False
)

plt.show()