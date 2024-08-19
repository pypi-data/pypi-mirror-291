from pathlib import Path
import polars as pl
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import torch


def data_loading(frac: float = .5):
    # input
    file = Path.home() / 'Downloads/credit_card_transactions-ibm_v2.csv'
    dict_label = {'Yes': 1}
    df = (
        pl.read_csv(file)
        .sample(fraction=frac, seed=42)
        .lazy()
        .with_columns(pl.concat_str([pl.col('User'), pl.col('Card')], separator='_').alias('card_id'))
        .with_columns(
            pl.col('Amount').str.replace_all(r'\$', '').cast(pl.Float32),
            pl.col('Time').str.strptime(pl.Time, format='%H:%M').dt.hour().alias('hour'),
            pl.col('Time').str.strptime(pl.Time, format='%H:%M').dt.minute().alias('minute'),
            pl.col('Errors?').fill_null('No Errors'),
            pl.col('Is Fraud?').replace(dict_label, default=0),
        )

        .drop(['Time', 'User', 'Card', 'Merchant State', 'Zip'])
        .collect()

    )
    df = df.with_columns(
        pl.Series(values=LabelEncoder().fit_transform(df[i]), name=i)
        for i in ['Merchant City', 'Use Chip', 'Errors?']
    )
    print(df.shape)

    # split
    train, test = train_test_split(df, test_size=0.33, random_state=42)

    return train, test


def data_loading_to_model(G, data):
    edge_list = list(G.edges(data=True))
    x = []
    for edge in tqdm(edge_list):
        edge_values = list(edge[2].values())
        edge_values = [float(i[0]) if type(i) == tuple and type(i[0]) == str else i[0] if type(i) == tuple else i for i
                       in edge_values]
        x.append(edge_values)
    x = torch.tensor(x, dtype=torch.float)
    target = torch.tensor(data['Is Fraud?'].to_list(), dtype=torch.float)
    return x, target
