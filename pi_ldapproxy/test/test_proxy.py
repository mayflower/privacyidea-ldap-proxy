from ldaptor.protocols.ldap import ldaperrors
from twisted.internet import defer

from pi_ldapproxy.test.util import ProxyTestCase


class TestProxy(ProxyTestCase):
    privacyidea_credentials = {
        'hugo@default': 'secret'
    }

    @defer.inlineCallbacks
    def test_bind_succeeds(self):
        server, client = self.create_server_and_client([])
        yield client.bind('uid=hugo,cn=users,dc=test,dc=local', 'secret')

    def test_bind_fails_wrong_password(self):
        server, client = self.create_server_and_client([])
        d = client.bind('uid=hugo,cn=users,dc=test,dc=local', 'wrong')
        self.assertFailure(d, ldaperrors.LDAPInvalidCredentials)

    def test_bind_fails_unknown_user(self):
        server, client = self.create_server_and_client([])
        d = client.bind('uid=unknown,cn=users,dc=test,dc=local', 'secret')
        self.assertFailure(d, ldaperrors.LDAPInvalidCredentials)

    def test_bind_fails_no_matching_dn(self):
        server, client = self.create_server_and_client([])
        d = client.bind('uid=hugo,cn=users,dc=somewhere-else,dc=local', 'secret')
        self.assertFailure(d, ldaperrors.LDAPInvalidCredentials)

    def test_bind_fails_invalid_dn(self):
        server, client = self.create_server_and_client([])
        d = client.bind('dn=uid=hugo,cn=users,dc=test,dc=local', 'secret')
        self.assertFailure(d, ldaperrors.LDAPInvalidCredentials)
