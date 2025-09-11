import pandas as pd
import os
from datetime import timedelta
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Criar pasta de saída
path_output = 'outputs/graficos/'
os.makedirs(path_output, exist_ok=True)

# Ler dados
plantio_date = pd.to_datetime('2024-03-14')
data = pd.read_csv("utils/prec_mensal_SP.txt", sep='\t', parse_dates=['Ano-mes'], dayfirst=True)
data.set_index('Ano-mes', inplace=True)
data.index = pd.to_datetime(data.index)

# Selecionar séries
series = {
    'INMET': 'black',
    'ERA5-Land': 'tab:green',
    'ERA5': 'tab:orange',
    'NASA POWER': 'tab:blue',
    'CPC': 'tab:purple',
    'CHIRPS': 'gold'
}

# Configurações de fases e atividades
phases = [
    ('Germinação', plantio_date, plantio_date + timedelta(days=30), 'lime'),
    ('Estabelecimento \n vegetativo inicial', plantio_date + timedelta(days=30), plantio_date + timedelta(days=120), 'yellow'),
    ('Crescimento vegetativo \n Perfilhamento', plantio_date + timedelta(days=120), plantio_date + timedelta(days=210), 'orange'),
    ('Maturação inicial', plantio_date + timedelta(days=210), plantio_date + timedelta(days=300), 'magenta'),
    ('Maturação \n (acúmulo de sacarose)', plantio_date + timedelta(days=300), plantio_date + timedelta(days=390), 'skyblue')]

activity_dates = [
    ('2024-03-14', 'Plantio', 'red'),
    ('2024-06-21', 'Atividade 1', 'red'),
    ('2024-10-25', 'Atividade 2', 'red'),
    ('2025-02-28', 'Atividade 3', 'red'),
    ('2025-04-12', 'Atividade 4', 'red'),
    ('2025-03-31', 'Atividade 5 \n Corte - BRIX', 'red')]

# Definir largura das barras e posições
bar_width = 0.13
x = np.arange(len(data.index))  # posições para cada mês

fig, ax = plt.subplots(figsize=(15,4))

# Plotar cada série como barra deslocada
for i, (col, color) in enumerate(series.items()):
    ax.bar(x + i*bar_width, data[col], width=bar_width, color=color, label=col)

# Função para meses 
def mes_pt(dt):
    meses = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']
    return f"{meses[dt.month-1]}\n{dt.year}"

ax.set_xticks(x + bar_width*len(series)/2)  # centralizar rótulos
ax.set_xticklabels([mes_pt(d) for d in data.index], rotation=0, ha='center')

# Limites do eixo y
min_val = 0
max_val = data.max().max() + 50
ax.set_ylim(min_val, max_val)
ax.set_ylabel('Precipitação (mm)', fontsize=12)
ax.grid(True, axis='y', linestyle='--', alpha=0.6)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Atividades (linhas verticais)
for date_str, label, color in activity_dates:
    date_obj = pd.to_datetime(date_str)
    date_month = date_obj.replace(day=1)
    
    idx = np.where(data.index == date_month)[0]
    
    if len(idx) > 0:
        idx = idx[0]
        center_pos = x[idx] + (bar_width * len(series)) / 2
        
        # Linha vertical
        ax.axvline(x=center_pos, color=color, linestyle='--', linewidth=1.5, label='_nolegend_')
        
        # Ajuste do alinhamento baseado na atividade
        text_y = max_val + (max_val * 0.01)
        if label == 'Atividade 3':
            ax.text(center_pos, text_y, label, rotation=0,
                   va='bottom', ha='right', color=color,
                   fontsize=10, weight='bold',
                   bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
        elif label == 'Atividade 4':
            ax.text(center_pos, text_y, label, rotation=0,
                   va='bottom', ha='left', color=color,
                   fontsize=10, weight='bold',
                   bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
        else:
            ax.text(center_pos, text_y, label, rotation=0,
                   va='bottom', ha='center', color=color,
                   fontsize=10, weight='bold',
                   bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))
            
# Fases
for label, start_date, end_date, color in phases:
    # encontrar posições aproximadas de início e fim
    idx_start = np.argmin(np.abs(data.index - start_date))
    idx_end = np.argmin(np.abs(data.index - end_date))
    ax.axvspan(idx_start, idx_end, color=color, alpha=0.3, label='_nolegend_')
    center = (idx_start + idx_end)/2
    ax.text(center, max_val-20, label, ha='center', va='center', fontsize=12, alpha=0.85, bbox=dict(facecolor='white', alpha=0.15, boxstyle='round'))

# Legenda
handles, labels = ax.get_legend_handles_labels()
handles_series = [h for h, l in zip(handles, labels) if l not in ['_nolegend_']]
labels_series = [l for l in labels if l not in ['_nolegend_']]
ax.legend(handles_series, labels_series, loc='upper left', fontsize=12)

plt.tight_layout()
plt.savefig(path_output + 'prec_mensal_SP_barras.png', dpi=300, bbox_inches='tight')
plt.show()
