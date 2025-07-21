import pandas as pd
import urllib.request, json
from sqlalchemy import create_engine

def get_table_data(table_name, engine):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)

        return df
    except Exception as e:
        print(f"Error: {e}")

        return pd.DataFrame()
    
def connect_engine(db):
    db_name = db['db_name']
    user = db['user']
    password = db['password']
    host = db['host']
    port = db['port']
    
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")

    try:
        with engine.connect() as conn:
            print("Connection successful.")
    except Exception as e:
        print("Connection failed.")
        print(e)
    
    return engine
    
def extract_data(city_url, country_url, requirement_url, list_engine):
    city_raw = pd.read_csv(city_url)
    country_raw = pd.read_csv(country_url)

    with urllib.request.urlopen(requirement_url) as url:
        requirements_table = json.load(url)

    engine = connect_engine(list_engine)

    actor_df = get_table_data('actor', engine)
    store_df = get_table_data('store', engine)
    address_df = get_table_data('address', engine)
    category_df = get_table_data('category', engine)
    customer_df = get_table_data('customer', engine)
    film_actor_df = get_table_data('film_actor', engine)
    film_category_df = get_table_data('film_category', engine)
    inventory_df = get_table_data('inventory',engine)
    language_df = get_table_data('language',engine)
    rental_df = get_table_data('rental',engine)
    staff_df = get_table_data('staff',engine)
    payment_df = get_table_data('payment',engine)
    film_df = get_table_data('film',engine)

    table_dict = {
        'actor': actor_df,
        'store': store_df,
        'address': address_df,
        'category': category_df,
        'customer': customer_df,
        'film_actor': film_actor_df,
        'film_category': film_category_df,
        'inventory': inventory_df,
        'language': language_df,
        'rental': rental_df,
        'staff': staff_df,
        'payment': payment_df,
        'film': film_df,
        'city': city_raw,
        'country': country_raw
    }

    return table_dict, requirements_table
