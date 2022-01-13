import json
from configparser import ConfigParser
from ldap3 import Connection, Server, SIMPLE, SUBTREE, MODIFY_REPLACE


def get_config():
    config = ConfigParser()
    config.read('ldap.ini')
    return config


def connect_ldap(conf, **kwags):
    server = Server(host=conf["host"],
                    port=conf.getint("port", None),
                    use_ssl=conf.getboolean("use_ssl", False),
                    connect_timeout=5)
    return Connection(server, raise_exceptions=True, **kwags)


def find_user_dn(conf, conn, uid):
    search_filter = conf['search_filter'].replace('{uid}', uid)
    conn.search(conf['base'], "(%s)" % search_filter, SUBTREE)
    return conn.response[0]['dn'] if conn.response else None


def auth_ldap(username, password):
    config = get_config()["ldap"]
    connection = connect_ldap(conf=config, user=username, password=password)
    if connection.bind():
        return True
    else:
        return False


def change_password_ldap(conf, username, old_pass, new_pass):
    with connect_ldap(conf) as c:
        user_dn = find_user_dn(conf, c, username)

    # Note: raises LDAPUserNameIsMandatoryError when user_dn is None.
    with connect_ldap(conf,
                      authentication=SIMPLE,
                      user=user_dn,
                      password=old_pass) as c:
        c.bind()
        c.extend.standard.modify_password(user_dn, old_pass, new_pass)
