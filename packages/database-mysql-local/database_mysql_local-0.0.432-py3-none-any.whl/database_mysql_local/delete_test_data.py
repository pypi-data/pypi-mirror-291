import _mysql_connector
import mysql
from .generic_crud_ml import GenericCRUDML
from mysql.connector import ProgrammingError
import mysql.connector
from mysql.connector import errorcode
import warnings

import sys
import os
from dotenv import load_dotenv
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '../src'))


# TODO Check the number of records in the begging and in the end in all tables involved

#is_safe mode, if not, then if null or columns don't exist then we assume test data and delete
#doubel pointing, recursive pointing

#Need to implement recursive deleting in order for this to work

class DeleteTestData(GenericCRUDML):
    
    
    # TODO Should not delete the line with the lowest id (i.e. we want to keep the campaign with the lowest id which is is_test_data as this campaign is used for message-send-local-python)
    def delete_test_data(self, schema_name: str, table_name: str, is_safe_mode: bool = True, is_interactive: bool = True):
        #print('THIS IS THE CORRECT CODE')
        self.is_interactive = is_interactive
        if not self.is_interactive:
            is_safe_mode = True
        gcrml = GenericCRUDML(default_schema_name=schema_name, default_table_name=table_name)
        original_schema_name = self.default_schema_name
        original_table_name = self.default_table_name
        ## get a list of all the rows in the table which contain test data

        test_data_list = gcrml.select_multi_value_by_column_and_value(select_clause_value=f"{schema_name}_id",
                                                                      column_name='is_test_data', column_value=1)

        ## get a list of all the referenced tables of the main table

        select_query = """
            SELECT
              TABLE_SCHEMA,
              TABLE_NAME,
              COLUMN_NAME,
              CONSTRAINT_NAME,
              REFERENCED_TABLE_NAME,
              REFERENCED_COLUMN_NAME
            FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
            WHERE
              REFERENCED_TABLE_NAME LIKE %s
              AND REFERENCED_COLUMN_NAME = %s
        """

        params = (f'{schema_name}_table', f'{schema_name}_id')
        self.connection.commit()  # Ensure the connection is committed
        results =None
        try:
            self.cursor.execute(select_query, params)
            results = self.cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")

        for row_id in test_data_list:
            for result in results:
                #print(f"Changing the schema name to {result[0]}")
                gcrml1 = GenericCRUDML(default_schema_name=result[0], default_table_name=result[1])
                #rint(f"Changing the table name to {result[1]}")
                gcrml1.default_table_name = result[1]
                if result[1].endswith('table'):
                    gcrml1.default_view_table_name = result[1].replace("table", "view")
                if result[1].endswith('old'):
                    continue
                if is_safe_mode:
                    global to_delete
                    try:
                        to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value="is_test_data",
                                                                                 column_name=f"{schema_name}_id",
                                                                                 column_value=row_id,
                                                                                 view_table_name=gcrml1.default_view_table_name)
                    except ProgrammingError as e:
                        if e.errno == 1054:
                            print(
                                f"The column is_test_data does not exist in {gcrml1.default_table_name}. This column will be added to the table now.")
                            try:
                                gcrml1.create_column(schema_name=gcrml1.default_schema_name, table_name=gcrml1.default_table_name, column_name='is_test_data', data_type='TINYINT')
                            except ProgrammingError as e:
                                try:
                                    gcrml1.create_view()
                                except ProgrammingError as e:
                                    continue

                            to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value="is_test_data", column_name=f"{schema_name}_id", column_value=row_id, view_table_name=gcrml1.default_view_table_name)
                            continue
                        else:
                            #print(f"At this point the default_schema_name is {gcrml1.default_schema_name}")
                            gcrml1.create_view()
                            #print(f"view_created: {gcrml1.default_view_table_name}")
                            to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value="is_test_data", column_name=f"{schema_name}_id", column_value=row_id, view_table_name=gcrml.default_view_table_name)
                            continue
                    for entry in to_delete:
                        if entry == 1:
                            delete_query = f"""
                            DELETE from {result[0]}.{result[1]}
                            WHERE {result[0]}_id = {row_id} and 'is_test_data' = 1;

                            """
                            if self.is_interactive:
                                if self.ask_user_confirmation(delete_query) == 'yes':
                                    self.cursor.execute(delete_query)
                            else:
                                #print(delete_query)
                                self.cursor.execute(delete_query)

                        else:
                            print("ERROR: Trying to delete non-test-data")
                else:
                    to_delete = gcrml1.select_multi_value_by_column_and_value(select_clause_value=f"{schema_name}_id",
                                                                             column_name=f"{schema_name}_id",
                                                                             column_value=row_id,
                                                                             view_table_name=gcrml1.default_view_table_name)

                for entry in to_delete:
                    delete_query = f"""
                    DELETE from {result[0]}.{result[1]}
                    WHERE {original_schema_name}_id = {row_id};
                    
                    """
                    if self.is_interactive:
                        if self.ask_user_confirmation(delete_query) == 'yes':
                            self.cursor.execute(delete_query)
                    else:
                        self.cursor.execute(delete_query)
            #If no errors, delete from the original table
            delete_query = f"""DELETE from {original_schema_name}.{original_table_name} Where {original_schema_name}_id = {row_id};"""
            if self.is_interactive:
                if self.ask_user_confirmation(delete_query) == 'yes':
                    self.cursor.execute(delete_query)
            else:
                #print(delete_query)
                self.cursor.execute(delete_query)

    def ask_user_confirmation(self, sql_query):
        global user_preference
        print(f"SQL Query:\n{sql_query}")
        user_choice = input("Do you want to execute this query? (yes/no/all): ").strip().lower()
        if user_choice in ['yes', 'no']:
            user_preference = (user_choice == 'yes')
            return user_preference
        elif user_choice in ['all']:
            self.is_interactive = False
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")
            return self.ask_user_confirmation(sql_query)


