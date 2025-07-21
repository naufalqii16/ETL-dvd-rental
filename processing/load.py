from processing.extract import connect_engine

def load_to_postgres(list_engine, cleaned_data):
    engine = connect_engine(list_engine)
    try:
        cleaned_data.to_sql('film_list', engine, if_exists='replace', index=False)
        print("load to postgres successful")
    except Exception as e:
        print("load to postgres failed:", e)


