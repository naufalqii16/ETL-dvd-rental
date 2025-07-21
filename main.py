import os
import processing.extract as ex
import processing.transform as tr
import processing.load as lo
from dotenv import load_dotenv


load_dotenv()

setup_engine = {
    'db_name' : os.getenv("DB_NAME_DATA_SOURCE"),
    'user' : os.getenv("USER_DATA_SOURCE"),
    'password' : os.getenv("PASSWORD_DATA_SOURCE"),
    'host' : os.getenv("HOST_DATA_SOURCE"),
    'port' : os.getenv("PORT_DATA_SOURCE")
}

table_dict, requirement_tables = ex.extract_data(os.getenv("CITY_URL"), os.getenv("COUNTRY_URL"), 
                                                os.getenv("REQUIREMENT_URL"), setup_engine)

tr.check_table_requirements(actual_table=table_dict, requirement_table=requirement_tables)
tr.check_shape(actual_table=table_dict)
tr.check_columns(actual_table = table_dict, req_table = requirement_tables)
tr.check_data_types(actual_table = table_dict, requirements_table = requirement_tables)
tr.check_missing_values(actual_table=table_dict)
tr.check_duplicate(actual_table=table_dict)

table_dict = tr.missmatch_table_columns(actual_table=table_dict)
table_dict = tr.remove_missing_values(actual_table=table_dict)
table_dict = tr.missmatch_data_types(actual_table=table_dict)
table_dict = tr.remove_duplicate(actual_table=table_dict)

film_list = tr.extract_film_list(actual_data=table_dict)

# Load Data to Postgres
setup_engine_dest = {
    'db_name' : os.getenv("DB_NAME_DATA_DESTINATION"),
    'user' : os.getenv("USER_DATA_DESTINATION"),
    'password' : os.getenv("PASSWORD_DATA_DESTINATION"),
    'host' : os.getenv("HOST_DATA_DESTINATION"),
    'port' : os.getenv("PORT_DATA_DESTINATION")
}

lo.load_to_postgres(setup_engine_dest, film_list)