from morningstar.provider.on_demand import OnDemand
from morningstar.config import config
from morningstar.models.rips import RIPS
from morningstar.spec.on_demand_spec import OnDemandReturnType
from lxml import etree
from typing import Optional


class OnDemandClient():

    xpath_share_performanceid_basecurrency = "/FundShareClass/PerformanceId/Result[./IsBaseCurrency = 'true']/PerformanceId/text()"
    xpath_universe_morningstarid = "/FundShareClassList/ShareClass/Id/text()"

    def __init__(self, provider=None):
        """ Wraps Provider

        Args:
            provider (Provider): provider instance
        """
        if provider is None:
            provider = OnDemand(config=config.get('provider')['ondemand'])
        self.provider = provider


    def get_historical_rips(self,
                            isin: str,
                            return_type: OnDemandReturnType,
                            start_date: str = '',
                            end_date: str = '',
                            universe: str = '') -> [RIPS]:
        """Fetches RIPS for the fundshare with the given ISIN using the performance id in basecurrency

            Note:
                The ISIN is searched in the specified universe to obtain the morningstar id its associated performance id.
                If the share is obsolete for too long (45d), or not found in the given universe, or if no
                performance id in base currency can be found, a ValueError is raised. 

            Args:
                isin (str): e.g. "IE00BYML7P29"
                return_type (OnDemandReturnType): e.g. TotalReturn
                start_date (str): "%Y-%m-%d"
                end_date (str): "%Y-%m-%d"
                universe (str): e.g. "CHE"

            Returns:
                List of RIPS objects with one for each date
            """

        # Login before using any other method of provider
        self.provider.login()

        # Get universe to find Morningstar Id corresponding to isin
        #   no start and end date for search of isin in universe.
        #   Should be everything possible
        data_get_fundshare_universe = {'ClientId': self.provider.config['clientid'],
                                       'ActiveStatus':  '',     # obsolete and active, max coverage (last 45d)
                                       'InvestorType': '',      # both, dont care as only to get id
                                       'LegalStructureId': '',  # all types of funds
                                       'ISIN': isin,
                                       'CountryId': universe}
        root_n_universe = self.provider.get_universe(params=data_get_fundshare_universe)

        # read out ms id from universe xml
        #   It is unfortunately possible that a search by ISIN results in the correct fundshare which has
        #   a different ISIN than the one used for searching. In the resulting universe xml, it is also only
        #   listed with this other ISIN and hence cannot be found by subsetting in the xpath with the searched ISIN.
        #   (ie by using [./ISIN = '"+isin+"'] in xpath). Therefore, because only maximum a single share 
        #   should be found, read out directly withouth searching by ISIN in the xml
        ms_id = root_n_universe.xpath(self.xpath_universe_morningstarid)
        if len(ms_id) == 0:
            raise ValueError(
                "No Morningstar Id could be found for the given ISIN. Maybe the share is dead for too long or in a different universe?")
        if len(ms_id) > 1:
            raise ValueError(
                "More than one Morningstar Id found for this ISIN.")
        ms_id = str(ms_id[0])

        # With this morningstar id, get the respective share's xml and its performance id for basecurrency
        params_sharexml = {'Package': 'EDW', 'IDType': 'FundShareClassId',
                           'ClientId': self.provider.config['clientid'],
                           'Id': ms_id}
        root_n_share = self.provider.data_output(params=params_sharexml)

        share_performanceid_basecurrency = root_n_share.xpath(
            self.xpath_share_performanceid_basecurrency)
        if len(share_performanceid_basecurrency) == 0:
            raise ValueError(
                "No performance id in basecurrency could be found")
        if len(share_performanceid_basecurrency) > 1:
            raise ValueError(
                "More than 1 performance id in basecurrency was found: "+str(share_performanceid_basecurrency))
        share_performanceid_basecurrency = str(
            share_performanceid_basecurrency[0])

        # Download csv data from this performance id
        params_historydata = {'ClientId': self.provider.config['clientid'],
                              'DataType': 'rips',
                              'StartDate': start_date,
                              'EndDate': end_date,
                              'PriceType': str(return_type.value),
                              'PerformanceId': share_performanceid_basecurrency}
        return self.provider.history_data(params=params_historydata)