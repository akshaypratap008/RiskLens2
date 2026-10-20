from dotenv import load_dotenv
import requests
import os
from datetime import date, datetime
import numpy as np

from src.risklens2.models.company_research_schema import CompanyProfile, DirectorInfo, PSCInfo

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
        active_psc_count = psc_data["active_count"]
        
        for item in psc_data['items']:
            psc_name = item['name']
            psc_type = item['kind']
            psc_ceased = item['ceased']
            psc_reg_number = item['identification']['registration_number'] if "corporate" in psc_type else None
            psc_reg_country = item['identification']['country_registered'] if "corporate" in psc_type else None
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
                else:
                    psc_shareholding_band = ""
                    psc_voting_rights_band = ""
                    psc_right_to_add_remove_director = False
                
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

            



        
