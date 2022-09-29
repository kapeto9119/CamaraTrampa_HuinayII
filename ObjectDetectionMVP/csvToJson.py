def read(filepath):
  content = []
  with open(filepath) as csvfile:
    csv_reader = csv.reader(csvfile)
    headers = next(csv_reader)

    for row in csv_reader:
      row_data = {key: value for key, value in zip(headers, row)}
      content.append(row_data)

  return content