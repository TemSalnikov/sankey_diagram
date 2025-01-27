import plotly.graph_objects as go
import pandas as pd
import numpy as np
import yandex as yndx
import vtb
import sber
import urllib.request
from json import loads

if __name__ == '__main__':
    yndx_data = yndx.get_transactions()
    vtb_data = vtb.get_transactions()
    sber_data = sber.get_transactions()

    yndx_df = pd.DataFrame.from_dict(yndx_data)
    vtb_df = pd.DataFrame.from_dict(vtb_data)
    sber_df = pd.DataFrame.from_dict(sber_data)

    df = pd.concat([yndx_df,vtb_df,sber_df])
    df_correct = df.loc[df['category'].str.contains('Прочие|Входящий|Исходящий|Перевод|перевод|сбп', regex=True)]
    df_correct_src = df_correct.loc[df_correct['debit'] > 0]
    df_correct_src = df_correct_src.reset_index()
    df_correct_tgt = df_correct.loc[df_correct['credit'] > 0]
    df_correct_tgt = df_correct_tgt.reset_index()
    df_correct = df_correct_src.merge(df_correct_tgt, left_on = ['debit', 'transfer_datetime'], right_on = ['credit', 'transfer_datetime'])
    df_correct_src = df_correct[['index_x','category_x']]
    df_correct_src = df_correct_src.rename(columns = {'index_x':'index', 'category_x':'category'})
    df_correct_tgt =  df_correct[['index_y','category_y']]
    df_correct_tgt = df_correct_tgt.rename(columns={'index_y': 'index', 'category_y': 'category'})
    df_correct = pd.concat([df_correct_src, df_correct_tgt])
    # df_correct = df_correct.rename(columns={0: 'index'})
    df_correct = df_correct.set_index('index')
    df = df.join(df_correct, how='left', rsuffix= '_x')
    df = df.drop(columns= 'auth_code')
    df = df.loc[df.isnull().any(axis=1)]
    # df_correct = df.loc(df['category'] )

    df_source = df.loc[df['debit']>0]
    df_source['target'] = 'Доход'
    df_source_dict = df_source.drop(['bank', 'text', 'trans_datetime', 'transfer_datetime','credit', 'debit', 'target'], axis = 1)
    df_source_dict = df_source_dict.drop_duplicates()
    df_source_dict['source'] = df_source_dict['category']
    df_source_dict.loc[df_source_dict['category'].str.contains(r"перевод|сбп", case=False, regex=True), 'source'] = 'Входящий преевод'
    df_source_dict.loc[df_source_dict['category'].str.contains(r"товар|отмена|возврат", case=False, regex=True), 'source'] = 'Возврат, отмена операции'
    df_source_dict.loc[df_source_dict['category'].str.contains(r"прочие", case=False, regex=True), 'source'] = 'Прочие зачислени'
    df_source = df_source.merge(df_source_dict, left_on = 'category', right_on = 'category')
    df_source = df_source.rename({'debit': 'value'}, axis = 1)

    df_target = df.loc[df['credit']>0]
    df_target = df_target.rename({'category':'target', 'credit':'value'}, axis = 1)
    df_target['source'] = 'Доход'
    fin_df = pd.concat([df_source,df_target])

    df_fin_group = fin_df[['value','source','target']]
    df_fin_group = df_fin_group.groupby(['source','target']).sum('value')
    df_fin_group = df_fin_group.reset_index()
    df_lable_src = df_fin_group[['value', 'source']]
    df_lable_src = df_lable_src.rename({'source': 'lable'}, axis=1)

    df_lable_tgt = df_fin_group[['value','target']]
    df_lable_tgt = df_lable_tgt.rename({'target': 'lable'}, axis = 1)

    df_lable_list = pd.concat([df_lable_src, df_lable_tgt])
    df_lable_list = df_lable_list.rename(columns={0: 'lable'})
    df_lable_inex = df_lable_list['lable'].drop_duplicates()
    df_lable_inex = df_lable_inex.reset_index()
    df_lable_inex['id'] = df_lable_inex.index
    df_lable_inex = df_lable_inex.drop(['index'], axis=1)

    df_lable_src = df_lable_src.merge(df_lable_inex)
    df_list_lable_src = df_lable_src['id']
    list_src = df_list_lable_src.values.tolist()
    df_lable_tgt = df_lable_tgt.merge(df_lable_inex)
    df_list_lable_tgt = df_lable_tgt['id']
    list_tgt = df_list_lable_tgt.values.tolist()

    # дропаем Доход в дф src т.к. в src он счиается по credit полю, а в tgt по debit,  что является правильным
    df_lable_src.drop( df_lable_src[df_lable_src['lable'] == 'Доход'].index, inplace= True)
    df_src_tgt = pd.concat([df_lable_src,df_lable_tgt])
    df_src_tgt = df_src_tgt.sort_values(by = ['id'])
    # df_lable = df_lable_inex['lable']
    df_src_tgt_lab = df_src_tgt[['lable', 'id']]
    df_src_tgt_lab = df_src_tgt_lab.drop_duplicates()
    list_lable = df_src_tgt_lab['lable'].tolist()

    df_lable_value = df_fin_group['value']
    list_value = df_lable_value.values.tolist()

    # fin_dict = fin_df.to_dict('tight')
    # color_node_list = []
    # color_link_list = []
    # for row in fin_df:
    #     color_node = list(np.random.choice(range(100, 256), size=3))
    #     color = ','.join([str(x) for x in color_node])
    #     color_node_list.append(f'rgba({color}, 1)')
    #     color_link_list.append(f'rgba({color}, 0.4)')
    #
    #
    # url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    # response = urllib.request.urlopen(url)
    # data = loads(response.read())

    # override gray link colors with 'source' colors
    opacity = 0.4
    # change 'magenta' to its 'rgba' value to add opacity
    config = {"node":{"color": [
     "rgba(31, 119, 180, 0.8)",
     "rgba(255, 127, 14, 0.8)",
     "rgba(44, 160, 44, 0.8)",
     "rgba(214, 39, 40, 0.8)",
     "rgba(148, 103, 189, 0.8)",
     "rgba(140, 86, 75, 0.8)",
     "rgba(227, 119, 194, 0.8)",
     "rgba(127, 127, 127, 0.8)",
     "rgba(188, 189, 34, 0.8)",
     "rgba(23, 190, 207, 0.8)",
     "rgba(31, 119, 180, 0.8)",
     "rgba(255, 127, 14, 0.8)",
     "rgba(44, 160, 44, 0.8)",
     "rgba(214, 39, 40, 0.8)",
     "rgba(148, 103, 189, 0.8)",
     "rgba(140, 86, 75, 0.8)",
     "rgba(227, 119, 194, 0.8)",
     "rgba(127, 127, 127, 0.8)",
     "rgba(188, 189, 34, 0.8)",
     "rgba(23, 190, 207, 0.8)",
     "rgba(31, 119, 180, 0.8)",
     "rgba(255, 127, 14, 0.8)",
     "rgba(44, 160, 44, 0.8)",
     "rgba(214, 39, 40, 0.8)",
     "rgba(148, 103, 189, 0.8)",
     "rgba(140, 86, 75, 0.8)",
     "rgba(227, 119, 194, 0.8)",
     "rgba(127, 127, 127, 0.8)",
     "rgba(188, 189, 34, 0.8)",
     "rgba(23, 190, 207, 0.8)",
     "rgba(31, 119, 180, 0.8)",
     "rgba(255, 127, 14, 0.8)",
     "rgba(44, 160, 44, 0.8)",
     "rgba(214, 39, 40, 0.8)",
     "rgba(148, 103, 189, 0.8)",
     "magenta",
     "rgba(227, 119, 194, 0.8)",
     "rgba(127, 127, 127, 0.8)",
     "rgba(188, 189, 34, 0.8)",
     "rgba(23, 190, 207, 0.8)",
     "rgba(31, 119, 180, 0.8)",
     "rgba(255, 127, 14, 0.8)",
     "rgba(44, 160, 44, 0.8)",
     "rgba(214, 39, 40, 0.8)",
     "rgba(148, 103, 189, 0.8)",
     "rgba(140, 86, 75, 0.8)",
     "rgba(227, 119, 194, 0.8)",
     "rgba(127, 127, 127, 0.8)"
    ]},
    "link":{"color": [
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(33,102,172,0.35)",
     "rgba(178,24,43,0.35)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "rgba(0,0,96,0.2)",
     "lightgreen",
     "goldenrod"
    ]}}
    config['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in
                               config['node']['color']]
    config['link']['color'] = [config['node']['color'][src].replace("0.8", str(opacity))
                                        for src in list_src]

    fig = go.Figure(data=[go.Sankey(
        valueformat=".0f",
        valuesuffix="₽",
        # Define nodes
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=list_lable,
            color=config['node']['color']
        ),
        # Add links
        link=dict(
            source=list_src,
            target=list_tgt,
            value=list_value,
            label=list_lable,
            color =  config['link']['color']
        ))])

    fig.update_layout(
        title_text="Sankey diagram движения денежных средств",
        font_size=10)
    fig.show()