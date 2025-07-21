from tabulate import tabulate
import pandas as pd

# DATA VALIDATION

def check_table_requirements(actual_table, requirement_table):
    actual_table_name = [table for table in actual_table]
    requirement_table_name = list(requirement_table.keys())
    table_checking = []

    for table_name in actual_table_name:
        if table_name in requirement_table_name:
            table_checking.append([table_name, 'v'])
        else:
            table_checking.append([table_name, 'x'])

    table_headers = ['table_name', 'is_exist']
    table = tabulate(table_checking, headers=table_headers, tablefmt='grid')
    # return table
    print('=> STEP 1: Check Table')
    print(table)

def check_shape(actual_table):

    table_shape = []

    for table, data in actual_table.items():
        table_shape.append([table, data.shape[0], data.shape[1]])

    table_headers = ['table_name', 'Number of rows', 'Number of Columns']
    table = tabulate(table_shape, headers=table_headers, tablefmt='grid')
    # return table
    print('=> STEP 2: Check Data Shape')
    print(table)

def check_columns(actual_table, req_table):
    print('=> STEP 3: Check Columns')
    for key in req_table:
        column_names = []
        columns_req = [col['column_name'] for col in req_table[key]]
        columns_actual = actual_table[key].columns

        for column in columns_actual:
            if column in columns_req:
                column_names.append([column, 'v', 'v'])
            else:
                column_names.append([column, 'v', 'x'])

        for column in columns_req:
            if column not in columns_actual:
                column_names.append([column, 'x', 'v'])

        table_headers = ['column_name', 'in_actual_table', 'in_requirements_table']
        table = tabulate(column_names, headers=table_headers, tablefmt='grid') 
        print(f'Table: {key}')
        print(f'{table}\n')


def check_data_types(actual_table, requirements_table):
    print("=> STEP 4: Check Data Types")
    summary_data = []

    for table_name, df in actual_table.items():
        if table_name in requirements_table:
            for column_info in requirements_table[table_name]:
                column_name = column_info["column_name"]
                requirements_type = column_info["data_type"]
                
                if column_name in df.columns:
                    actual_type = str(df[column_name].dtype)
                    match = "✔" if actual_type == requirements_type else "X"
                    summary_data.append([table_name, column_name, actual_type, requirements_type, match])
                else:
                    summary_data.append([table_name, column_name, "N/A", requirements_type, "X (Column not found)"])

    headers = ["Table Name", "Column Name", "Actual Type", "Requirements Type", "Match"]

    mismatch_data = [row for row in summary_data if "X" in row[4]]
    
    if mismatch_data:
        print("\nSummary of Mismatches Data Types:")
        print(tabulate(mismatch_data, headers = headers, tablefmt = "grid"))
    
    else:
        print("All Data Types Match")


def check_missing_values(actual_table):
    missing = []
    print('=> STEP 5: Check Missing Values\n')
    print('Missing Value Summary')

    for table_name, data in actual_table.items():
        if data.isna().sum().sum() != 0:
            temp = data.isnull().sum()[data.isnull().any()].reset_index()
            temp.columns = ['column_name', 'missing_count']
            temp['missing_pct'] = ((temp['missing_count'] / len(data)) * 100).round(2)

            for _, row in temp.iterrows():
                missing.append([table_name, row['column_name'], row['missing_count'], row['missing_pct']])

    if missing:
        table_headers = ['Table Name', 'Column Name', 'Missing Value Count', 'Missing Value Percentage']
        table = tabulate(missing, headers=table_headers, tablefmt='grid')
        print(table)
    else:
        print("No missing values found.\n")

def check_duplicate(actual_table):
    print("=> STEP 6: Check Duplicates Data")
    duplicate_summary = []

    for table_name, data in actual_table.items():
        try:
            duplicate_rows = data[data.duplicated(keep = False)]
            
            if not duplicate_rows.empty:
                duplicate_summary.append([table_name, len(duplicate_rows)])
        except:
            pass

    if duplicate_summary:
        print("Duplicate Data Summary:")
        print(tabulate(duplicate_summary, headers=["Table Name", "Duplicate Rows Count"], tablefmt="grid"))
    else:
        print("No Duplicate Data Found")


# DATA CLEANSING

def missmatch_table_columns(actual_table):
    actual_table['country']['country_id'] = [i for i in range(len(actual_table['country']))]

    city_df = actual_table['city'].merge(actual_table['country'], on = 'country', how = 'left')

    city_df = city_df[['city_id', 'country_id', 'city', 'last_update']]

    actual_table['city'] = city_df.copy()

    return actual_table


def missmatch_data_types(actual_table):
    actual_table['customer']['create_date'] = pd.to_datetime(actual_table['customer']['create_date'])
    actual_table['country']['last_update'] = pd.to_datetime(actual_table['customer']['create_date'])
    actual_table['city']['country_id'] = actual_table['city']['country_id'].astype('int64')
    actual_table['city']['last_update'] = pd.to_datetime(actual_table['city']['last_update'])

    return actual_table


def remove_missing_values(actual_table):
    final_actual_data = {}
    for table, data in actual_table.items():
        cleaned_data = data.dropna()
        final_actual_data[table] = cleaned_data.copy()
    
    return final_actual_data

def remove_duplicate(actual_table):
    actual_table['city'] = actual_table['city'].drop_duplicates()
    
    return actual_table

def extract_film_list(actual_data):
    actor_data = actual_data['actor'].copy()
    film_actor_data = actual_data['film_actor'].copy()
    film_data = actual_data['film'].copy()
    film_category_data = actual_data['film_category'].copy()
    category_data = actual_data['category'].copy()

    film_list = category_data.merge(film_category_data, how='left', on='category_id', suffixes=('_x1', '_y1'))
    film_list = film_list.merge(film_data, how='left', on='film_id', suffixes=('_x2', '_y2'))
    film_actor_detail = film_actor_data.merge(actor_data, how='left', on='actor_id', suffixes=('_x3', '_y3'))
    film_actor_detail['full_name'] = film_actor_detail['first_name'] + ' ' + film_actor_detail['last_name']
    film_actor_detail = film_actor_detail.groupby(['film_id', 'last_update_x3', 'last_update_y3'])['full_name'].apply(lambda x: ', '.join(x))

    film_actor_detail = pd.DataFrame(film_actor_detail)
    film_actor_detail = film_actor_detail.reset_index()

    film_list = film_list.merge(film_actor_detail, how='left', on='film_id', suffixes=('_x4', '_y4'))
    film_list = film_list[['film_id', 'title', 'description', 'name', 'rental_rate', 'length', 'rating', 'full_name']].copy()

    rename_column_map = {
        'film_id' : 'fid',
        'name' : 'category',
        'rental_rate' : 'price',
        'full_name' : 'actors'
    }

    film_list.rename(columns=rename_column_map, inplace=True)

    return film_list