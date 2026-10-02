import flet as ft


CHAVE_REFRESH_TOKEN = "evalytics.auth.refresh_token"
CHAVE_LEMBRAR_ME = "evalytics.auth.remember_me"


class AuthState:
    def __init__(self):
        self._autenticado = False
        self._usuario = None
        self._id_token = None
        self._refresh_token = None
        self._prefs = None

    async def inicializar_storage(self, page: ft.Page):
        """
        Inicializa o SharedPreferences e adiciona o controle
        à página antes de utilizá-lo.
        """

        if self._prefs is None:
            self._prefs = ft.SharedPreferences()

            page.services.append(self._prefs)

    @property
    def autenticado(self):
        return self._autenticado

    @property
    def usuario(self):
        return self._usuario

    @property
    def id_token(self):
        return self._id_token

    @property
    def refresh_token(self):
        return self._refresh_token

    async def iniciar_sessao(
        self,
        dados,
        page: ft.Page,
        lembrar_me=False,
    ):
        await self.inicializar_storage(page)

        self._autenticado = True
        self._usuario = dados
        self._id_token = dados.get("idToken")
        self._refresh_token = dados.get("refreshToken")

        if lembrar_me and self._refresh_token:
            await self._prefs.set(
                CHAVE_REFRESH_TOKEN,
                self._refresh_token,
            )

            await self._prefs.set(
                CHAVE_LEMBRAR_ME,
                True,
            )

        else:
            await self._remover_sessao_persistida()

    async def encerrar_sessao(
        self,
        page: ft.Page,
    ):
        await self.inicializar_storage(page)

        self._autenticado = False
        self._usuario = None
        self._id_token = None
        self._refresh_token = None

        await self._remover_sessao_persistida()

    async def _remover_sessao_persistida(self):
        if self._prefs is None:
            return

        await self._prefs.remove(
            CHAVE_REFRESH_TOKEN
        )

        await self._prefs.remove(
            CHAVE_LEMBRAR_ME
        )

    async def possui_sessao_persistida(
        self,
        page: ft.Page,
    ):
        await self.inicializar_storage(page)

        refresh_token = await self._prefs.get(
            CHAVE_REFRESH_TOKEN
        )

        return bool(refresh_token)

    async def obter_refresh_token(
        self,
        page: ft.Page,
    ):
        await self.inicializar_storage(page)

        return await self._prefs.get(
            CHAVE_REFRESH_TOKEN
        )

    async def restaurar_sessao(
        self,
        page: ft.Page,
        api_key: str,
    ) -> bool:
        """
        Tenta restaurar uma sessão persistida utilizando
        o refresh token do Firebase.
        """

        refresh_token = await self.obter_refresh_token(page)

        if not refresh_token:
            return False

        try:
            import requests

            url = (
                "https://securetoken.googleapis.com/v1/token"
                f"?key={api_key}"
            )

            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            }

            response = requests.post(
                url,
                data=payload,
                timeout=10,
            )

            if response.status_code != 200:
                await self._remover_sessao_persistida()
                return False

            data = response.json()

            self._autenticado = True
            self._usuario = data

            self._id_token = data.get("id_token")
            self._refresh_token = data.get(
                "refresh_token",
                refresh_token,
            )

            await self._prefs.set(
                CHAVE_REFRESH_TOKEN,
                self._refresh_token,
            )

            return True

        except Exception as erro:
            print(
                f"Erro ao restaurar sessão: {erro}"
            )

            return False


auth_state = AuthState()