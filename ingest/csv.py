from ingest.transform import clean
from datetime import datetime
import csv

def process(filepath, filename, filters=[], transforms={}, alltransforms=[], max=1000000, writefile=False, returnRows=False, uploadS3=None):
    with open(f'{filepath}/{filename}') as csvFile:
        csvReader = csv.reader(csvFile, delimiter=';')
        catalog = {}
        count = 0
        rows = []

        # Treat Header
        header = next(csvReader)
        header[0] = clean(header[0], '\ufeff')
        print(f'Column names are {", ".join(header)}')
        # rows.append(header)
        count += 1

        # A catalog with ColumnName -> Position in the row array.
        catalog = _buildCatalog(header)

        for row in csvReader:
            filtered = True
            for ft in filters:
                filtered = filtered and ft(catalog, row)
            if not filtered:
                continue

            print(f'\t BEFORE {row}')

            # Clean columns
            for col, pos in catalog.items():
                for transf in alltransforms:
                    row[pos] = transf(row[pos])
                if transforms.get(col) is None:
                    continue
                for transf in transforms[col]:
                    row[pos] = transf(row[pos])

            print(f'\t AFTER {row}')

            rows.append(row)
            count += 1
            if count == max:
                break
        print(f'Processed {count} lines.')
        if writefile:
            nfilename = _write(filepath, filename, rows)
            if uploadS3 is not None:
                uploadS3(nfilename)

        if returnRows:
            return rows

def _buildCatalog(row):
    """Builds a dict of ColumnName to position"""
    cat = {}
    for pos, col in enumerate(row):
        cat[col] = pos
    return cat

def _write(filepath, filename, rows):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    nfile = f"{filename[:-4]}-{timestamp}{filename[len(filename)-4:]}"
    csvfile = open(f'{filepath}/{nfile}', 'w', newline='\n')
    csvwriter = csv.writer(csvfile, delimiter=';')
    csvwriter.writerows(rows)
    csvfile.close()
    return nfile