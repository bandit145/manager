import pytest
from manager.database.Database import Database


@pytest.mark.parametrize('host,user,password,dbname,port,ssl', [
    ('localhost', 'postgres', 'admin', 'manager', 5432, False)
])
def test_connection(host, user, password, dbname, port, ssl):
    db = Database(host, user, password,dbname, port, ssl)
    assert(db.run_sql_stmt('SELECT * FROM %s',('doot'), False)) == False
