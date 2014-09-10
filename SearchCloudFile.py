from dropbox import session, client

class MyDropboxAPI():


    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

    def connect(self, token_key='', token_secret=''):
        """
        Authorizing with Dropbox
        :param token_key: token key/secret from older sessions. If exists,
                            prevents the user from another authorization
        :param token_secret: see above
        :return:
        """
        self.currentSession = session.DropboxSession(self.app_key, self.app_secret)

        if token_key and token_secret:
            self.currentSession.set_token(token_key,token_secret)

        else:
            request_token = self.currentSession.obtain_request_token()
            auth_url = self.currentSession.build_authorize_url(request_token)
            print "Please, follow this link for auth"
            print auth_url
            raw_input("and press 'Enter' when you're done")
            self.currentSession.obtain_access_token(request_token)

        self.currentClient = client.DropboxClient(self.currentSession)

    def isRecentlyChanged(self, filename='report.otd', path=''):
        """
        Checks if file exists and last modified in 3 days,
        if so - sets self.new_file True
        :param filename: name of file
        :param path: search in this path
        """

        file = self.currentClient.search(path,filename)

        if file:
            file_meta = file[0]

            from dateutil import parser
            from datetime import datetime, timedelta

            # using replace to make mod_date offset-naive for correct subtraction
            mod_date = parser.parse(file_meta['modified']).replace(tzinfo=None)

            if datetime.now() - mod_date < timedelta(days=3):
                self.new_file = True