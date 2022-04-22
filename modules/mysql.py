import pymysql;

import configparser;
import os;

import threading , queue;

class Config(object):
    def __init__(self, configFileName='db.cnf'):
        file = os.path.join(os.path.dirname(__file__), configFileName)
        self.config = configparser.ConfigParser()
        self.config.read(file)

    def getSections(self):
        return self.config.sections()

    def getOptions(self, section):
        return self.config.options(section)

    def getContent(self, section):
        result = {}
        for option in self.getOptions(section):
            value = self.config.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result

class parameter(object):
    def __init__(self, password, database, host, port, user, initsize, maxsize):
        self.host = str(host)
        self.port = int(port)
        self.user = str(user)
        self.password = str(password)
        self.database = str(database)
        self.maxsize = int(maxsize)
        self.initsize = int(initsize)

class ThemisPool(parameter):
    def __init__(self, fileName='db.cnf', configName='mysql'):
        self.config = Config(fileName).getContent(configName)
        super(ThemisPool, self).__init__(**self.config)
        self.pool = queue.Queue(maxsize=self.maxsize)
        self.idleSize = self.initsize
        self._lock = threading.Lock()
        for i in range(self.initsize):
            self.pool.put(self.createConn())

    def createConn(self):
        return pymysql.connect(host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password,
                                database=self.database,
                                charset='utf8')
    
    def getConn(self):
        self._lock.acquire()
        try:
            if not self.pool.empty():
                self.idleSize -= 1
            else:
                if self.idleSize < self.maxsize:
                    self.idleSize += 1
                    self.pool.put(self.createConn())
        finally:
            self._lock.release()
            return self.pool.get()
     
    def releaseCon(self, conn=None):
        try:
            self._lock.acquire()
            if self.pool.qsize() < self.initsize:
                self.pool.put(conn)
                self.idleSize += 1
            else:
                try:
                    surplus = self.pool.get()
                    surplus.close()
                    del surplus
                    self.idleSize -= 1
                except pymysql.ProgrammingError as e:
                    raise e
        finally:
            self._lock.release()
      
    def fetchone(self, sql):
        themis = None
        cursor = None
        try:
            themis = self.getConn()
            cursor = themis.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except pymysql.ProgrammingError as e:
            raise e
        except pymysql.OperationalError as e:
            raise e
        except pymysql.Error as e:
            raise e
        finally:
            cursor.close()
            self.releaseCon(themis)
     
    def update(self, sql):
        themis = None
        cursor = None
        try:
            themis = self.getConn()
            cursor = themis.cursor()
            cursor.execute(sql)
            data = cursor.lastrowid
            print(type(data))
            return data
        except pymysql.ProgrammingError as e:
            raise e
        except pymysql.OperationalError as e:
            raise e
        except pymysql.Error as e:
            raise e
        finally:
            themis.commit()
            cursor.close()
            self.releaseCon(themis)
            
    def __del__(self):
        try:
            while True:
                conn = self.pool.get_nowait()
            if conn:
                conn.close()
        except queue.Empty:
            pass