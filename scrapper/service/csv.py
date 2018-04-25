import csv


def dict_to_csv(d: dict, file: str):
    """
    saves two dimensional dict to csv table
    outer dictionary key is rows name
    inner dictionary key is columns name
    :param d: dictionary
    :param file: file path
    """
    columns = set()
    for d_inner in d.values():
        for k in d_inner.keys():
            columns.add(k)
    columns = list(columns)

    with open(file, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([''] + columns)

        for seg_name, seg in d.items():
            counts = []
            for column in columns:
                counts.append(seg.get(column, 0))
            writer.writerow([seg_name] + counts)
