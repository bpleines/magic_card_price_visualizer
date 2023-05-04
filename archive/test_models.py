from sklearn.preprocessing import MinMaxScaler

from card_analyzer import CardAnalyzer


def all_card_data():
    analyzer = CardAnalyzer()
    analyzer.address_missing_data()
    analyzer.fix_types()
    # This halts program execution, so don't include by default
    # analyzer.pairplot()
    # StandardScaler
    analyzer.make_pipeline()
    analyzer.make_pipeline(drop_columns=["name", "image", "type_line", "artist"])
    analyzer.make_pipeline(drop_columns=["name", "image", "type_line", "artist", "cmc"])
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color"]
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color", "cmc"]
    )
    # MinMaxScaler
    analyzer.make_pipeline(scaler=MinMaxScaler())
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist"], scaler=MinMaxScaler()
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "cmc"],
        scaler=MinMaxScaler(),
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color"],
        scaler=MinMaxScaler(),
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color", "cmc"],
        scaler=MinMaxScaler(),
    )


def before_hasbro_card_data():
    analyzer = CardAnalyzer()
    analyzer.address_missing_data()
    analyzer.fix_types()
    analyzer.set_before_hasbro()
    # StandardScaler
    analyzer.make_pipeline()
    analyzer.make_pipeline(drop_columns=["name", "image", "type_line", "artist"])
    analyzer.make_pipeline(drop_columns=["name", "image", "type_line", "artist", "cmc"])
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color"]
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color", "cmc"]
    )
    # MinMaxScaler
    analyzer.make_pipeline(scaler=MinMaxScaler())
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist"], scaler=MinMaxScaler()
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "cmc"],
        scaler=MinMaxScaler(),
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color"],
        scaler=MinMaxScaler(),
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color", "cmc"],
        scaler=MinMaxScaler(),
    )


def after_hasbro_card_data():
    analyzer = CardAnalyzer()
    analyzer.address_missing_data()
    analyzer.fix_types()
    analyzer.set_after_hasbro()
    # StandardScaler
    analyzer.make_pipeline()
    analyzer.make_pipeline(drop_columns=["name", "image", "type_line", "artist"])
    analyzer.make_pipeline(drop_columns=["name", "image", "type_line", "artist", "cmc"])
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color"]
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color", "cmc"]
    )
    # MinMaxScaler
    analyzer.make_pipeline(scaler=MinMaxScaler())
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist"], scaler=MinMaxScaler()
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "cmc"],
        scaler=MinMaxScaler(),
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color"],
        scaler=MinMaxScaler(),
    )
    analyzer.make_pipeline(
        drop_columns=["name", "image", "type_line", "artist", "color", "cmc"],
        scaler=MinMaxScaler(),
    )


print(
    "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
)
print("ALL CARD DATA")
all_card_data()
print(
    "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
)
print("CARDS BEFORE HASBRO")
before_hasbro_card_data()
print(
    "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
)
print("CARDS AFTER HASBRO")
after_hasbro_card_data()
