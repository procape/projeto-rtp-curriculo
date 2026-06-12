import os
from ldap3 import Server, Connection, ALL
from ldap3.utils.conv import escape_filter_chars

LDAP_SERVER = os.getenv("LDAP_SERVER", "192.168.150.2")
LDAP_DOMAIN = os.getenv("LDAP_DOMAIN", "huprocape.upe")
LDAP_BASE_DN = os.getenv("LDAP_BASE_DN", "DC=huprocape,DC=upe")


def autenticar_ldap(cpf, senha):
    if not cpf or not senha:
        return {
            "autenticado": False,
            "nome_completo": None,
            "erro": "CPF e senha são obrigatórios"
        }

    try:
        server = Server(LDAP_SERVER, get_info=ALL)

        usuario_completo = f"{cpf}@{LDAP_DOMAIN}"

        conn = Connection(
            server,
            user=usuario_completo,
            password=senha,
            auto_bind=True
        )

        nome_completo = "Usuário Desconhecido"

        cpf_seguro = escape_filter_chars(cpf)

        conn.search(
            search_base=LDAP_BASE_DN,
            search_filter=f"(&(objectClass=user)(sAMAccountName={cpf_seguro}))",
            attributes=["displayName"]
        )

        if conn.entries and hasattr(conn.entries[0], "displayName"):
            nome_completo = str(conn.entries[0].displayName)

        conn.unbind()

        return {
            "autenticado": True,
            "nome_completo": nome_completo,
            "erro": None
        }

    except Exception as e:
        print(f"Erro LDAP: {e}")
        return {
            "autenticado": False,
            "nome_completo": None,
            "erro": str(e)
        }
