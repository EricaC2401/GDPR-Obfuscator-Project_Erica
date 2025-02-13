import pytest
from src.obfuscator import obfuscate_file
import pandas as pd


@pytest.fixture
def test_data():
    content = """student_id,name,course,graduation_date,email_address\n
                1234,John Smith,Software,2024-03-31,j.smith@email.com\n
                """

    fields = ['name', 'email_address']
    return content, fields


class TestCsv:
    @pytest.mark.it('Test if obfuscate_file obfuscated fields in the list')
    def test_obfuscate_csv_specified_fields(self, test_data):
        test_content, test_fields = test_data
        obfuscated_output = obfuscate_file(test_content, test_fields, 'csv')
        df_obfuscated = pd.read_csv(obfuscated_output)
        assert all(df_obfuscated['name'] == '***')
        assert all(df_obfuscated['email_address'] == '***')

    @pytest.mark.it('Test if the other fields remains the same')
    def test_obfuscate_csv_other_fields(self, test_data):
        test_content, test_fields = test_data
        obfuscated_output = obfuscate_file(test_content, test_fields, 'csv')
        df_obfuscated = pd.read_csv(obfuscated_output)
        assert 'student_id' in df_obfuscated.columns
        assert df_obfuscated['student_id'].iloc[0] == 1234
        assert 'graduation_date' in df_obfuscated.columns
        assert df_obfuscated['graduation_date'].iloc[0] == '2024-03-31'
    

class TestException:
    @pytest.mark.it('Test ValueError when an unsupported type is inputed')
    def test_obfuscate_file_unsupported_file_type(self, test_data):
        test_content, test_fields = test_data
        with pytest.raises(ValueError):
            obfuscate_file(test_content, test_fields, 'xlsx')
    
    @pytest.mark.it('Test KeyError when a field in the fields_list is not in the data')
    def test_obfuscate_file_unrelated_field(self, test_data):
        test_content = test_data[0]
        test_fields = ['name', 'cohort']
        with pytest.raises(KeyError):
            obfuscate_file(test_content, test_fields, 'csv')

