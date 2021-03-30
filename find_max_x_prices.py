def find_x_max_prices(filepath, x=5):
  with open(filepath, 'r') as csv_file:
    lines = csv_file.readlines()
    lines.pop(0)
    prices = []
    for line in lines:
      prices.append(float(line.split(',')[2]))
    prices.sort(reverse=True)
    print("The " + str(x) + " highest values for " + filepath + ": " + str(prices[0:5]))

find_x_max_prices('magic_card_csv_files_by_color/W.csv')
find_x_max_prices('magic_card_csv_files_by_color/U.csv')
find_x_max_prices('magic_card_csv_files_by_color/B.csv')
find_x_max_prices('magic_card_csv_files_by_color/R.csv')
find_x_max_prices('magic_card_csv_files_by_color/G.csv')
