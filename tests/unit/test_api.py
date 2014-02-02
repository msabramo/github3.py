import github3
import mock
import unittest


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.mocked_github = mock.patch('github3.api.gh',
                                        autospec=github3.GitHub)
        self.gh = self.mocked_github.start()

    def tearDown(self):
        self.mocked_github.stop()

    def test_all_events(self):
        github3.all_events()
        self.gh.iter_events.assert_called_once_with(-1, None)

    def test_all_gists(self):
        github3.all_gists()
        self.gh.iter_gists.assert_called_once_with(None, -1, None)

    def test_all_repos(self):
        github3.all_repos()
        # TODO(Ian): When you fix GitHub, fix this test too
        self.gh.iter_all_repos.assert_called_once_with(-1, None)

    def test_all_users(self):
        github3.all_users()
        # TODO(Ian): Fix this when GitHub changes
        self.gh.iter_all_users.assert_called_once_with(-1, None)

    def test_authorize(self):
        args = ('login',  'password', ['scope'], 'note', 'url.com', '', '')
        github3.authorize(*args)
        self.gh.authorize.assert_called_once_with(*args)

    def test_enterprise_login(self):
        args = ('login', 'password', None, 'https://url.com/', None)
        with mock.patch.object(github3.GitHubEnterprise, 'login') as login:
            g = github3.enterprise_login(*args)
            assert isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with('login', 'password', None, None)

    def test_followers_of(self):
        github3.followers_of('login')
        self.gh.iter_followers.assert_called_with('login', -1, None)

    def test_followed_by(self):
        github3.followed_by('login')
        self.gh.iter_following.assert_called_with('login', -1, None)

    def test_gist(self):
        gist_id = 123
        github3.gist(gist_id)
        self.gh.gist.assert_called_once_with(gist_id)

    def test_gists_for(self):
        github3.gists_for('username')
        self.gh.iter_gists.assert_called_once_with('username', -1, None)

    def test_gitignore_template(self):
        language = 'Python'
        github3.gitignore_template(language)
        self.gh.gitignore_template.assert_called_once_with(language)

    def test_gitignore_templates(self):
        github3.gitignore_templates()
        assert self.gh.gitignore_templates.called is True

    def test_login(self):
        args = ('login', 'password', None, None)
        with mock.patch.object(github3.GitHub, 'login') as login:
            g = github3.login(*args)
            assert isinstance(g, github3.GitHub)
            assert not isinstance(g, github3.GitHubEnterprise)
            login.assert_called_once_with(*args)

    def test_organizations(self):
        args = ('login', -1, None)
        github3.organizations(*args)
        self.gh.iter_orgs.assert_called_with(*args)

    def test_repo_issues(self):
        args = ('owner', 'repository', None, None, None, None, None, None,
                None, None, -1, None)
        github3.repo_issues(*args)
        self.gh.iter_repo_issues.assert_called_with(*args)

    def test_starred(self):
        github3.starred('login')
        self.gh.iter_starred.assert_called_with('login', -1, None)

    def test_subcriptions(self):
        github3.subscriptions('login')
        self.gh.iter_subscriptions.assert_called_with('login', -1, None)

    def test_user_repos(self):
        args = ('login', None, None, None, -1, None)
        github3.user_repos('login')
        self.gh.iter_user_repos.assert_called_with(*args)