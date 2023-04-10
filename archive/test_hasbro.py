from card_analyzer import CardAnalyzer

analyzer = CardAnalyzer()
analyzer.address_missing_data()
analyzer.fix_types()
analyzer.check_hasbro_claim()
