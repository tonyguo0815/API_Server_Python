from modules.mysql import ThemisPool;
from modules.tool import ResultPackage;

db = ThemisPool();

def test_get():
    return 'Test Get1';

def test_post(data):
    result = list(db.fetchone('SELECT * FROM try_db.account'));
    keys = ['id','account','password'];
    if result:
        result = ResultPackage(result,keys);
        return result;
    else:
        return 'Error';