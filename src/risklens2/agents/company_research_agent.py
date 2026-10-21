from dotenv import load_dotenv
import requests
import os
from datetime import date, datetime, timedelta
import numpy as np

from risklens2.models.company_research_schemas import CompanyProfile, DirectorInfo, PSCInfo, FillingsInfo, InsolvencyInfo

BASE_URL = "https://api.company-information.service.gov.uk/company"
API_KEY = os.getenv("COMPANY_HOUSE_API")

class CompanyResearchAgent:
    """This agent uses company registration number and fetches information from the company house. The fetched info contains Company Number, Company Name, Directors, SIC Codes, Industry, Company Status etc"""

    def get_company_profile(self, COMPANY_NUMBER) -> CompanyProfile:
        """This function fetches company information using Company House API"""
        url = f"{BASE_URL}/{COMPANY_NUMBER}"
        response = requests.get(
            url = url,
            auth= (API_KEY, "")
        )

        company_data = response.json()
        
        company_name = company_data.get("company_name", "")
        company_number= company_data.get("company_number", "")
        status= company_data.get('company_status', "")
        incorporation_date = datetime.strptime(company_data['date_of_creation'], "%Y-%m-%d").date()
        age = date.today().year - incorporation_date.year
        type = company_data.get('type', "")
        sic_codes = company_data.get('sic_codes', "")
        reg_address = company_data.get('registered_office_address', "")
        next_confirmation_statement_due= company_data.get("confirmation_statement", "").get("next_due", "")

        return CompanyProfile(
            company_name=company_name,
            company_number=company_number,
            status=status,
            incorporation_date=incorporation_date,
            age=age,
            type= type,
            sic_code=sic_codes,
            reg_address=reg_address,
            next_confirmation_statement_due=next_confirmation_statement_due
        )

    def get_director_details(self, COMPANY_NUMBER) -> DirectorInfo:
        """This function fetches the information about the directors, secratary and other officials of the company using Company House API"""
        url = f"{BASE_URL}/{COMPANY_NUMBER}/officers"
        response = requests.get(
            url = url,
            auth= (API_KEY, "")
        )

        officers_data = response.json()
        
        directors = []
        secretary = []
        others = []

        for item in officers_data['items']:
            
            # if officer is a director, add the details to directors list
            if item['officer_role'] == "director":
                directors.append(
                    {
                        "name": item['name'],
                        "appointment_date": datetime.strptime(item['appointed_on'], "%Y-%m-%d").date(),
                        "nationality": item['nationality'],
                        "tenure_in_years": round((date.today() - datetime.strptime(item['appointed_on'], "%Y-%m-%d").date()).days/365, 2)
                    }
                )

            # if officer is secratary, add the details to secratary list
            elif item['officer_role'] == "secretary":
                secretary.append(
                    {
                        'name': item['name'],
                        "appointment_date": datetime.strptime(item['appointed_on'], "%Y-%m-%d").date(),
                        "nationality": item['nationality'],
                        "tenure_in_years": round((date.today() - datetime.strptime(item['appointed_on'], "%Y-%m-%d").date()).days/365, 2)
                    }
                )

            # for any other officials, add them to others list including their role.
            else:
                others.append(
                    {
                        "name": item['name'],
                        "appointment_date": datetime.strptime(item['appointed_on'], "%Y-%m-%d").date(),
                        "nationality": item['nationality'],
                        "role": item['officer_role']
                    }
                )

        return DirectorInfo(
            directors = directors,
            secretary=secretary,
            others= others,
            director_count=len(directors),
            total_officials = len(directors) + len(secretary) + len(others),
            avg_director_tenure= np.mean([director['tenure_in_years'] for director in directors])
        )

    def get_psc_details(self, COMPANY_NUMBER) -> dict:
        """This function fetches the list of person with significant control. The details include the type of psc, shareholding info etc."""
        url =  f"{BASE_URL}/{COMPANY_NUMBER}/persons-with-significant-control"
        response = requests.get(
            url = url,
            auth = (API_KEY, "")
        )

        psc_data = response.json()
        psc = []

        active_psc_count = psc_data.get("active_count", None)
        psc_shareholding_band = None
        psc_voting_rights_band = None
        psc_right_to_add_remove_director = False
        
        for item in psc_data['items']:
            psc_name = item['name']
            psc_type = item['kind']
            psc_ceased = item['ceased']
            psc_reg_number = item.get('identification').get('registration_number') if "corporate" in psc_type else None
            psc_reg_country = item.get('identification').get('country_registered') if "corporate" in psc_type else None
            psc_ownership = item['natures_of_control']
            for value in psc_ownership:
                if "ownership-of-shares-25-to-50-percent" in value:
                    psc_shareholding_band = "25% to 50%"
                elif "ownership-of-shares-50-to-75-percent" in value:
                    psc_shareholding_band = "50% to 75%"
                elif "ownership-of-shares-75-to-100-percent" in value:
                    psc_shareholding_band = "75% above"
                elif "voting-rights-25-to-50-percent" in value:
                    psc_voting_rights_band = "25% to 50%"
                elif "voting-rights-50-to-75-percent" in value:
                    psc_voting_rights_band = "50% to 75%"
                elif "voting-rights-75-to-100-percent" in value:
                    psc_voting_rights_band = "75% above"
                elif "right-to-appoint-and-remove-directors" in value:
                    psc_right_to_add_remove_director = True
                
                
            psc.append(
                PSCInfo(
                    psc_name = psc_name,
                    psc_type = psc_type,
                    psc_ceased = psc_ceased,
                    psc_reg_number = psc_reg_number,
                    psc_reg_country = psc_reg_country,
                    psc_shareholding_band = psc_shareholding_band,
                    psc_voting_rights_band = psc_voting_rights_band,
                    psc_right_to_add_remove_director = psc_right_to_add_remove_director
                )
            )

        return {
            "psc": psc,
            "active_psc_count": active_psc_count
        }

    def get_filings_details(self, COMPANY_NUMBER) -> FillingsInfo:
        """This function fetches the details of company's filling history. Example last_filing_date, last_confirmation statement, company_disolved_flag, director_change_count_24m, director_termination_count_12m, director_termination_count_24m, etc"""
        url = f"{BASE_URL}/{COMPANY_NUMBER}/filing-history"
        response = requests.get(
            url,
            auth = (API_KEY, "")
        )
        filings_data = response.json()

        strike_off_action_flag:bool = False
        last_accounts_filed_date = None
        last_confirmation_statement_date = None
        director_change_counts_24m = 0
        director_termination_count_24m = 0
        share_capital_change_count = 0

        for filing in filings_data.get("items", []):
            filing_type = filing.get("type")
            if filing_type == "AA" and last_accounts_filed_date is None:
                last_accounts_filed_date = filing.get("date", None)       # last account filed date
            elif filing_type == "CS01" and last_confirmation_statement_date is None:
                last_confirmation_statement_date = filing.get("date", None)      # last confirmation statement submission date
            elif filing_type in ["GAZ1", "GAZ2", "GAZ2(A)", "DISS40"]:
                strike_off_action_flag = True       # any stricke off action on the company

        # directors appointment and termination frequency
        # cutoff date -> 24months
        cut_off_date = (datetime.today() - timedelta(days = 730)).date()

        for filing in filings_data.get('items', []):
            if filing.get('type') in ["AP01", "AP02"] and datetime.fromisoformat(filing.get('date')).date() >= cut_off_date:
                director_change_counts_24m += 1
            elif filing.get('type') == "TM01" and datetime.fromisoformat(filing.get('date')).date() >= cut_off_date:
                director_termination_count_24m += 1
            elif filing.get('type') in ["SH01", "SH02", "SH03", "SH06"]:
                share_capital_change_count += 1

        director_change_frequency_per_year = (director_change_counts_24m / 2)

        return FillingsInfo(
            strike_off_action_flag=strike_off_action_flag,
            last_accounts_filed_date=last_accounts_filed_date,
            last_confirmation_statement_date= last_confirmation_statement_date,
            director_change_counts_24m=director_change_counts_24m,
            director_termination_count_24m=director_termination_count_24m,
            director_change_frequency_per_year = director_change_frequency_per_year,
            share_capital_change_count=share_capital_change_count
        )

    def get_insolvency_details(self, COMPANY_NUMBER) -> InsolvencyInfo:
        """This functions finds any insolvency for a given company. Returns true if present."""
        url = f"{BASE_URL}/{COMPANY_NUMBER}/insolvency"

        response = requests.get(
            url,
            auth = (API_KEY, "")
        )

        has_insolvency = False
        if response.status_code == 200:
            has_insolvency = True

        return InsolvencyInfo(
            has_insolvency=has_insolvency
        )

    def get_charge_details(self, COMPANY_NUMBER):
        pass
            








            



        
