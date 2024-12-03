import pandas as pd
import random
import math
# Function to categorize rows into 3 buckets based on multiple columns

FINAL_BUCKET_SIZE = 4


def categorize_rows(df):
    buckets = {
        'Bucket 1': [],
        'Bucket 2': [],
    }

    # Loop through each row and categorize into buckets
    for _, row in df.iterrows():
        if row['Is Overseas'] == True and row['SP Status'] == 'In Program' and row['Gender'] == 'male':
            buckets['Bucket 1'].append(row)
        elif row['Is Overseas'] == False and row['SP Status'] == 'In Program' and row['Gender'] == 'male':
            buckets['Bucket 2'].append(row)
        elif row['Is Overseas'] == False and row['SP Status'] == 'In Program' and row['Gender'] == 'male':
            buckets['Bucket 3'].append(row)

    return buckets

# Function to select between 2 and 5 items from each bucket


def select_from_buckets(buckets, number_of_buckets):
    # Iterate number_of_buckets times
    new_buckets = {}
    some_bucket_name = random.choice(list(buckets.keys()))
    cols = buckets[some_bucket_name].columns
    counter = 1

    # for i in range(1, number_of_buckets):
    while len(list(buckets.keys())) > 0:
        print(f'{counter} started.')
        initial_df = pd.DataFrame(columns=cols)
        key_list = list(buckets.keys())
        new_buckets[counter] = []

        while len(initial_df) < FINAL_BUCKET_SIZE:
            num_items_to_select = 1
            if len(key_list) > 0:
                bucket_name = random.choice(key_list)
                key_list.remove(bucket_name)
                row_dfs = buckets[bucket_name]

                if len(row_dfs) == 0:
                    continue

                selected_rows = row_dfs.sample(num_items_to_select)
                initial_df = pd.concat(
                    [initial_df, selected_rows], ignore_index=True)

                idx = row_dfs.index[row_dfs['Person Id']
                                    == selected_rows.iloc[0]['Person Id']]
                cleaned_dfs = row_dfs.drop(idx)

                buckets[bucket_name] = cleaned_dfs
                if len(cleaned_dfs) == 0:
                    del buckets[bucket_name]

            else:
                break

        new_buckets[counter] = initial_df
        print(f'{counter} completed.')
        counter += 1

    for bucket_name in list(buckets.keys()):
        print(bucket_name, ": ", len(buckets[bucket_name]))

    return new_buckets


def categorize_by_column(df, column_name):
    buckets = {}

    # Get unique values in the specified column
    unique_values = df[column_name].unique()

    # Loop through the unique values and categorize rows into buckets
    for value in unique_values:
        buckets[value] = df[df[column_name] == value]

    return buckets


# Example usage
if __name__ == "__main__":
    # region Read the Excel file (make sure to replace 'data.xlsx' with your actual file path)
    file_path = 'data_sheet_for_python.xlsx'  # Update with your file path
    df = pd.read_excel(file_path)
    # endregion

    # Ensure the DataFrame contains the expected number of rows and columns
    print(f"Original DataFrame shape: {df.shape}")

    # region Categorization based on multiple column conditions

    # Categorize rows into 3 buckets based on the criteria
    # buckets = categorize_rows(df)
    # endregion

    # region Make buckets based on distinct values in a column

    # Specify the column name you want to categorize by
    column_name = 'Language'  # Replace with the column you want to use

    # Categorize rows into buckets based on unique values in the column
    buckets = categorize_by_column(df, column_name)
    # endregion

    # region Count the new number of bins

    row_count = df.shape[0]
    number_of_buckets = (math.floor(
        row_count/4)) + (0 if row_count % 4 == 0 else 1)
    # endregion

    new_bins = select_from_buckets(buckets, number_of_buckets)

    # region Convert dictionary of data frames into an excel file

    df = new_bins.values()

    data_frames_list = [
        df for df in new_bins.values() if isinstance(df, pd.DataFrame)]

    dfs = pd.concat(data_frames_list, ignore_index=True)
    print("Dataframe count after concatination: ", len(dfs))
    dfs.to_excel('dict1515.xlsx')
    # endregion
