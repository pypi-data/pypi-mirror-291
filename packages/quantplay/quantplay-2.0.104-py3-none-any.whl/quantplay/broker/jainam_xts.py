from quantplay.broker.xts import XTS


class Jainam(XTS):
    def __init__(
        self,
        api_secret: str | None = None,
        api_key: str | None = None,
        md_api_key: str | None = None,
        md_api_secret: str | None = None,
        wrapper: str | None = None,
        md_wrapper: str | None = None,
        client_id: str | None = None,
        load_instrument: bool = True,
        is_dealer: bool = False,
    ):
        super().__init__(
            root_url=f"http://ctrade.jainam.in:{3000 if is_dealer else 3001}",
            api_key=api_key,
            api_secret=api_secret,
            md_api_key=md_api_key,
            md_api_secret=md_api_secret,
            wrapper=wrapper,
            md_wrapper=md_wrapper,
            ClientID=client_id,
            is_dealer=is_dealer,
            load_instrument=load_instrument,
        )


# c = Jainam(api_key="263c59f6f4819ccbebf318", api_secret="Kqkp821@Jd", md_api_key="534366e91e9bcf84115624", md_api_secret="Yvnf855@bn", client_id="DLL11257")
# c = Jainam(api_key="cfd1d450a247a68bfc4447", api_secret="Wvvi122$ST", md_api_key="7e83f15231a2e249938492", md_api_secret="Uyfk361#cn", client_id="DLL9814", is_dealer=True)
