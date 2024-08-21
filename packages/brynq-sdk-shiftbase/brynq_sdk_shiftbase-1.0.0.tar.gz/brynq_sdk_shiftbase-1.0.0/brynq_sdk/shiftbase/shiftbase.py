import pandas as pd
import requests
from typing import Union, List
from brynq_sdk.brynq import BrynQ


class Shiftbase(BrynQ):
    """
    This class is meant to be a simple wrapper around the Shiftbase API. In order to start using it, authorize your application in BrynQ.
    You will need to provide a token for the authorization, which can be set up in BrynQ and referred to with a label.
    You can find the Shiftbase API docs here: https://developer.shiftbase.com/
    """
    def __init__(self, label: Union[str, List], api_type: str = "API"):
        super().__init__()
        credentials = self.get_system_credential(system='shiftbase', label=label)
        self.url = "https://api.shiftbase.com/api/"
        # Shiftbase has two token types, USER and API. API is a fixed token, USER is a token that is generated for a specific user when you do a post request to user/login.
        self.headers = {"Authorization": f"{api_type} {credentials['api_token']}",
                        "Accept": "application/json",
                        "Content-Type": "application/json"}

    def get_absence(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the absence data from Shiftbase.
        :param filters: A dict with filters. See the Shiftbase API docs for more info: https://developer.shiftbase.com/docs/core/2e1fba402f9bb-list-absentees.
        :return:
        """
        response = requests.get(url=f"{self.url}absentees?",
                                headers=self.headers,
                                params=filters)
        # {"min_date": "2022-01-01", "status": "Approved", "max_date": end_of_next_year})
        response.raise_for_status()
        response_json = response.json()['data']
        absence_data = [absence.get("Absentee") for absence in response_json]

        return pd.DataFrame(absence_data)

    def get_absence_types(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the get_absence_types data from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}absentee_options?",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        absence_type_data = [absence_type.get("AbsenteeOption") for absence_type in response_json]

        return pd.DataFrame(absence_type_data)

    def get_employees(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the employees from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}users?",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        employees = [employee.get("User") for employee in response_json]

        return pd.DataFrame(employees)

    def get_mappings(self, employer_id: int) -> pd.DataFrame:
        """
        This method retrieves the employees from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}integrations/map/{employer_id}",
                                headers=self.headers)
        response.raise_for_status()
        mapping_data = response.json()["data"]["ApiMapping"]["employee_import_mapped_employees"]
        mapping = pd.DataFrame(mapping_data, columns=["internal_id", "external_id"])

        return mapping

    def get_timesheets(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the timesheets from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}timesheets",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        worked_time = [rateblock.get("RateBlock") for rateblock in response_json]
        worked_time_list = [item for sublist in worked_time for item in sublist]
        timesheets_meta = [timesheet.get("Timesheet") for timesheet in response_json]
        worked_time = pd.DataFrame(worked_time_list)
        timesheets_meta = pd.DataFrame(timesheets_meta)
        del timesheets_meta["Rates"]
        timesheets = pd.merge(worked_time, timesheets_meta, how="left", left_on="timesheet_id", right_on="id", suffixes=("", "_meta"))

        return timesheets

    def get_contracts(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the contracts from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}contracts",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        contracts = [contract.get("Contract") for contract in response_json]

        return pd.DataFrame(contracts)

    def get_contract_types(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the contract types from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}contract_types",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        contract_types = [contract_type.get("ContractType") for contract_type in response_json]

        return pd.DataFrame(contract_types)

    def get_absentees(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the absentees from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}absentees",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        absentees = [contract_type.get("Absentee") for absentee in response_json]

        return pd.DataFrame(absentees)

    def get_absentee_options(self, filters: dict = None) -> pd.DataFrame:
        """
        This method retrieves the absentee options from Shiftbase.
        :return:
        """
        response = requests.get(url=f"{self.url}absentee_options",
                                headers=self.headers,
                                params=filters)
        response.raise_for_status()
        response_json = response.json()['data']
        absentee_options = [contract_type.get("AbsenteeOption") for absentee_option in response_json]

        return pd.DataFrame(absentee_options)


