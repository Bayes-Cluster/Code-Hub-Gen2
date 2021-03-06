import os
import json
from modules.config import BASE_DIR, __SETTINGS_PATH__, get_db_conf
from ldap3 import Connection, Server, SIMPLE, SUBTREE, SYNC, Reader, ObjectDef


def connect_ldap(conf, **kwags):
    server = Server(host=conf["host"],
                    port=conf.getint("port", None),
                    use_ssl=conf.getboolean("use_ssl", False),
                    connect_timeout=5)
    return Connection(server, raise_exceptions=False, **kwags)


def find_user_dn(conf, conn, uid):
    search_filter = conf["search_filter"].replace('{uid}', uid)
    conn.search(conf['base'], "(%s)" % search_filter, SUBTREE)
    return conn.response[0]['dn'] if conn.response else None

def find_usermail_dn(conf, conn, uid):
    search_filter = conf["search_filter"].replace('uid', "mail")
    search_filter = search_filter.replace('{mail}', uid)
    conn.search(conf['base'], "(%s)" % search_filter, SUBTREE)
    return conn.response[0]['dn'] if conn.response else None

def find_user_directory(uid):
    config = get_db_conf()["ldap"]
    base = config["base"]
    with connect_ldap(config) as c:
        obj_person = ObjectDef(['person', 'posixAccount'], c)
        r = Reader(c, obj_person, base, "uid:={}".format(uid))
        r.search()
        return r[0]["homeDirectory"][0]


def auth_ldap(username, password, mail:bool=False):
    config = get_db_conf()["ldap"]
    with connect_ldap(config, client_strategy=SYNC) as c:
        c.bind()
        try:
            if mail == False:
                user_dn = find_user_dn(config, c, username)
            else:
                user_dn = find_usermail_dn(config, c, username)
            if user_dn == None:
                return False
        except Exception as e:
            return False
        try:
            connection = connect_ldap(conf=config, user=user_dn, password=password)
        except:
            return False
        if connection.bind() == True:
            return True
        else:
            return False


def change_password_ldap(username, old_pass, new_pass):
    config = get_db_conf()["ldap"]
    with connect_ldap(config) as c:
        c.bind()
        try:
            user_dn = find_user_dn(config, c, username)
        except Exception as e:
            return False
        c.unbind()
    # Note: raises LDAPUserNameIsMandatoryError when user_dn is None.
    with connect_ldap(config,
                      authentication=SIMPLE,
                      user=user_dn,
                      password=old_pass) as c:
        c.bind()
        try:
            c.extend.standard.modify_password(user_dn, old_pass, new_pass)
            c.unbind()
            return True
        except Exception as e:
            return False

