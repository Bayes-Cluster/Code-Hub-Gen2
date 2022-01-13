import json
from configparser import ConfigParser
from ldap3 import Connection, Server, SIMPLE, SUBTREE, SYNC, MODIFY_REPLACE

__SETTINGS_PATH__ ="ldap.ini"

def get_config():
    config = ConfigParser()
    config.read(__SETTINGS_PATH__)
    return config


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


def auth_ldap(username, password):
    config = get_config()["ldap"]
    with connect_ldap(config, client_strategy=SYNC) as c:
        c.open()
        try:
            user_dn = find_user_dn(config, c, username)
        except Exception as e:
            return False
        try:
            connection = connect_ldap(conf=config, user=user_dn, password=password)
        except Exception as e:
            return False
    if connection.bind():
        return True
    else:
        return False


def change_password_ldap(username, old_pass, new_pass):
    config = get_config()["ldap"]
    with connect_ldap(config) as c:
        c.bind()
        user_dn = find_user_dn(config, c, username)
        c.unbind()
    # Note: raises LDAPUserNameIsMandatoryError when user_dn is None.
    with connect_ldap(config,
                      authentication=SIMPLE,
                      user=user_dn,
                      password=old_pass) as c:
        c.bind()
        c.extend.standard.modify_password(user_dn, old_pass, new_pass)
        c.unbind()
        return True
