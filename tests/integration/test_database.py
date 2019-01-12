import pytest
from manager.database.Database import Database

@pytest.mark.parametrize('host','user','password','dbname','ssl', [
    ('localhost', 'postgres', 'postgres', 'manager', False)
])
def test_connection(host, user, password, dbname, ssl):
    db = Database(host, user, password,dbname, ssl)
    print(db.run_sql_stmt('SELECT * FROM %s'),('view_name'))
