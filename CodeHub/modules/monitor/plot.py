import pandas as pd
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from bokeh.embed import components

def table(data:dict):
    df = pd.DataFrame(data)
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]
    data_table = DataTable(source=ColumnDataSource(df), columns=columns, autosize_mode="fit_viewport", width=1000, height=300)
    script, div = components(data_table)
    return script, div
