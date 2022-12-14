from sklearn.preprocessing import MinMaxScaler

from card_analyzer import CardAnalyzer

analyzer = CardAnalyzer()
analyzer.address_missing_data()
analyzer.fix_types()
# Standard Scaler
analyzer.make_pipeline()
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist'])
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist', 'cmc'])
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist', 'color'])
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist', 'color', 'cmc'])
# Min-max scaler
analyzer.make_pipeline(scaler=MinMaxScaler())
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist'],
                       scaler=MinMaxScaler()
)
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist', 'cmc'],
                       scaler=MinMaxScaler()
)
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist', 'color'],
                       scaler=MinMaxScaler()
)
analyzer.make_pipeline(drop_columns=['name', 'image', 'type_line', 'artist', 'color', 'cmc'],
                       scaler=MinMaxScaler()
)
