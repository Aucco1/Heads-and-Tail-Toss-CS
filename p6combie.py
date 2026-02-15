import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import warnings

warnings.filterwarnings('ignore') 
plt.style.use('fivethirtyeight')

file_path = r"C:\Users\Muhammed\Documents\GitHub\sumagka-msu-pi\GROUP 8 EXCEL FILE.xlsx"
coin_classes = ['1A', '1B', '2', '5A', '5B', '10A', '10B', '20']

def get_grand_totals(sheet_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    classes_row = df.iloc[1].fillna('').astype(str).str.strip()
    sub_headers = df.iloc[2].fillna('').astype(str).str.strip().str.upper()
    attempt_cols = [i for i, v in enumerate(sub_headers) if 'ATTEMPT' in str(v)]
    
    extracted_data = []
    max_attempts = 0
    
    for i, a_idx in enumerate(attempt_cols):
        cls = ''
        for offset in range(5):
            if a_idx + offset < len(classes_row) and classes_row[a_idx + offset] in coin_classes:
                cls = classes_row[a_idx + offset]
                break
            if a_idx - offset >= 0 and classes_row[a_idx - offset] in coin_classes:
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
                temp_df = pd.DataFrame({'H': h_data[valid].values, 'T': t_data[valid].values}, index=attempts[valid].values.astype(int))
                max_attempts = max(max_attempts, int(temp_df.index.max()))
                extracted_data.append(temp_df)
    
    common_index = range(1, max_attempts + 1)
    grand_h = pd.Series(0.0, index=common_index)
    grand_t = pd.Series(0.0, index=common_index)
    for temp_df in extracted_data:
        temp_df = temp_df.reindex(common_index, method='ffill').fillna(0)
        grand_h += temp_df['H']
        grand_t += temp_df['T']
    return grand_h, grand_t, max_attempts

table_h, table_t, table_max = get_grand_totals('#5 TABLE')
tiles_h, tiles_t, tiles_max = get_grand_totals('#5 TILES')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7), facecolor='#f4f4f4')
fig.suptitle('Requirement #5: Grand Totals (Table vs. Tiles)', fontsize=22, fontweight='bold', color='#333333')

COLOR_H = '#00b4d8'
COLOR_T = '#ff4d6d'
max_frames = max(table_max, tiles_max)

ax1.set_xlim(0, table_max + 5)
ax1.set_ylim(0, max(table_h.max(), table_t.max()) + 10)
ax1.set_title('TABLE Surface (Grand Total)', fontsize=16)
line_table_h, = ax1.plot([], [], label='Heads', color=COLOR_H, linewidth=3.5)
line_table_t, = ax1.plot([], [], label='Tails', color=COLOR_T, linewidth=3.5)
dot_table_h, = ax1.plot([], [], 'o', color=COLOR_H, markersize=10, markeredgecolor='white')
dot_table_t, = ax1.plot([], [], 'o', color=COLOR_T, markersize=10, markeredgecolor='white')
ax1.legend(loc='upper left')

ax2.set_xlim(0, tiles_max + 5)
ax2.set_ylim(0, max(tiles_h.max(), tiles_t.max()) + 10)
ax2.set_title('TILES Surface (Grand Total)', fontsize=16)
line_tiles_h, = ax2.plot([], [], label='Heads', color=COLOR_H, linewidth=3.5)
line_tiles_t, = ax2.plot([], [], label='Tails', color=COLOR_T, linewidth=3.5)
dot_tiles_h, = ax2.plot([], [], 'o', color=COLOR_H, markersize=10, markeredgecolor='white')
dot_tiles_t, = ax2.plot([], [], 'o', color=COLOR_T, markersize=10, markeredgecolor='white')
ax2.legend(loc='upper left')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

def update(frame):
    if frame == 0:
        return line_table_h, line_table_t, dot_table_h, dot_table_t, line_tiles_h, line_tiles_t, dot_tiles_h, dot_tiles_t
        
    f_table = min(frame, table_max)
    if f_table > 0:
        x, h, t = range(1, f_table+1), table_h.iloc[:f_table], table_t.iloc[:f_table]
        line_table_h.set_data(x, h)
        line_table_t.set_data(x, t)
        dot_table_h.set_data([x[-1]], [h.iloc[-1]])
        dot_table_t.set_data([x[-1]], [t.iloc[-1]])

    f_tiles = min(frame, tiles_max)
    if f_tiles > 0:
        x, h, t = range(1, f_tiles+1), tiles_h.iloc[:f_tiles], tiles_t.iloc[:f_tiles]
        line_tiles_h.set_data(x, h)
        line_tiles_t.set_data(x, t)
        dot_tiles_h.set_data([x[-1]], [h.iloc[-1]])
        dot_tiles_t.set_data([x[-1]], [t.iloc[-1]])
        
    return line_table_h, line_table_t, dot_table_h, dot_table_t, line_tiles_h, line_tiles_t, dot_tiles_h, dot_tiles_t

ani = animation.FuncAnimation(fig, update, frames=max_frames + 1, interval=50, blit=True, repeat=False)
plt.show()