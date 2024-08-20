# Project Description for drug-repurposing-extract

This is a Python package for drug repurposing data extraction. You can use it to retrieve and analyze data related to specific compound IDs (CIDs) for potential drug repurposing.

## Installation

You can install the package using `pip`:

```bash
pip install drug-repurposing-extract
```
# Usage

## Import the package

```bash
import drug_repurposing
from drug_repurposing import get_data
```

## Generate CSV File from CID List

### To generate a CSV file from a list of CIDs (Compound IDs), you can use the generate_data_from_list function:

```bash
get_data.generate_data_from_list([942, 1070])
```

## Generate CSV List from Uploading a CSV File of CID List

### You can also generate a CSV file from a list of CIDs by uploading a CSV file containing the CID list. Here's how you can do it in a Google Colab environment:

```bash
from google.colab import files
import io
import pandas as pd

uploaded = files.upload()
uploaded_file = list(uploaded.values())[0]
df = pd.read_csv(io.BytesIO(uploaded_file))
data = df["cid"].values

get_data.generate_data_from_list(data)
```

## Predicting the CIDs Data

### To predict data based on CIDs, you can follow these steps:

Make sure you have a CSV file (e.g., complete_data.csv) generated from the previous steps.

Read the CSV file using pandas:

```bash
import pandas as pd
df = pd.read_csv("complete_data.csv")
```

Use the predict_data function to perform predictions:

```bash
get_data.predict_data(df)
```

