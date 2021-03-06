import esipy

from django.conf import settings

from eve_esi.metrics import COUNTER_ESI_REQUESTS
from eve_esi.exceptions import EsiException


class EsiManager:
    _ESI_APP = None

    @property
    def app(self):
        if self._ESI_APP is None:
            self._ESI_APP = esipy.EsiApp(
                datasource=getattr(settings, 'ESI_DATASOURCE', 'tranquility')
            ).get_latest_swagger

        return self._ESI_APP

    def get_security(self):
        return esipy.EsiSecurity(
            # app=self.app,
            redirect_uri=settings.ESI_CALLBACK,
            client_id=settings.ESI_CLIENT_ID,
            secret_key=settings.ESI_SECRET_KEY,
            esi_datasource=getattr(settings, 'ESI_DATASOURCE', 'tranquility'),
            headers={'User-Agent': settings.ESI_USER_AGENT}
        )

    def get_client(self, security=None):
        return esipy.EsiClient(
            security=security,
            headers={'User-Agent': settings.ESI_USER_AGENT}
        )

    def __getitem__(self, key):
        return self.app.op[key]

    def __request_helper(self, method, endpoint, client=None, **kwargs):
        if client is None:
            client = self.get_client()

        op = self[endpoint](**kwargs)

        if method == 'head':
            res = client.head(op)
        elif method == 'request':
            res = client.request(op)

        COUNTER_ESI_REQUESTS.labels(
            endpoint=endpoint,
            status=res.status
        ).inc()

        if 500 <= res.status <= 599 or res.status in [420, 429]:
            raise EsiException(endpoint, res.status, kwargs)

        return res

    def head(self, endpoint, client=None, **kwargs):
        return self.__request_helper('head', endpoint, client, **kwargs)

    def request(self, endpoint, client=None, multi_page=False, **kwargs):
        if not multi_page:
            return self.__request_helper('request', endpoint, client, **kwargs)

        res = []

        pages = self.head(endpoint, client, **kwargs).header['X-Pages'][0]

        for page in range(1, pages + 1):
            res += self.request(endpoint, client, page=page, **kwargs).data

        return res


ESI = EsiManager()
