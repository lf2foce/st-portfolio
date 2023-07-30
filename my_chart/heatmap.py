import numpy as np
import plotly.graph_objects as go
import json

def stock_heatmap(stocks_df_pivot):
    corr = stocks_df_pivot.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    df_mask = corr.mask(mask)
    X = df_mask.columns.tolist()
    z = df_mask.to_numpy()
    z_text = [[str(round(y, 1)) if str(y) != 'nan' else '' for y in x  ] for x in z]
    # hovertext = [[f'corr({X[i]}, {X[j]})= {corr[i][j]:.2f}' if i>j else '' for j in list(df_mask.columns)] for i in list(df_mask.columns)]
    sns_colorscale = [[0.0, '#3f7f93'], #cmap = sns.diverging_palette(220, 10, as_cmap = True)
    [0.071, '#5890a1'],
    [0.143, '#72a1b0'],
    [0.214, '#8cb3bf'],
    [0.286, '#a7c5cf'],
    [0.357, '#c0d6dd'],
    [0.429, '#dae8ec'],
    [0.5, '#f2f2f2'],
    [0.571, '#f7d7d9'],
    [0.643, '#f2bcc0'],
    [0.714, '#eda3a9'],
    [0.786, '#e8888f'],
    [0.857, '#e36e76'],
    [0.929, '#de535e'],
    [1.0, '#d93a46']]

    heat = go.Heatmap(z=df_mask,
                    x=X,
                    y=X,
                    xgap=1, ygap=1,
                    text= z_text,
                    texttemplate="%{text}",
                    textfont={"size":14},
                    colorscale='RdBu',#sns_colorscale,
                    colorbar_thickness=20,
                    colorbar_ticklen=3,
                    hovertext=z_text,
                    hoverinfo='text',
                    showscale=True,
                    zmid=0 #added
                    )


    title = 'Correlation Matrix'               

    layout = go.Layout(title_text=title, title_x=0.5, 
                    
                    width=700, height=700,
                    xaxis_showgrid=False,
                    yaxis_showgrid=False,
                    yaxis_autorange='reversed',
                    template='plotly_white'
                    )
    
    fig=go.Figure(data=[heat], layout=layout)    
    result = fig.to_json()
    return fig # json.loads(result)
    # fig.show() 