# format the data from the trustedparts API into data: dict[int, dict[int | str, dict[Any, Any] | str]]
# so it can be written to excel sheet
from typing import Any

# variables is a dict, each value of the dict is a mpn which is a dict holding row_number: int,
# suppliers: list of dataclasses (name, column index)

# returns a dict of dicts, higher level dicts are by row
# number (from bom dict) representing different mpns holding lower level dicts that are by
# column index (from bom dict) representing different suppliers, holding stock, price,  ect..
def format_data(response: dict, variables: dict[str,dict[str,int | Any]]) -> dict[int, dict[int | str, dict[Any, Any] | str]]:
    data = {}
    # dict holds "PartResults" which is a list of all the different mpn
    for mpn in variables:
        risk_and_column_dict = {}
        for instance in response["PartResults"]:
            if instance["PartNumber"] == mpn:
                #correct results for this mpn
                risk_and_column_dict["risk"] = f"Life Cycle Risk: {instance['LifecycleRisk']}\nSupply Chain Risk: {instance['SupplyChainRisk']}"
                for supplier in variables[mpn]["suppliers"]:
                    for distributor in instance["Distributors"]:
                        if distributor["Name"] == supplier.name:
                            stock = ""
                            price = ""
                            i = 1
                            for distributor_result in distributor["DistributorResults"]:
                                stock += f"Offer {i} (SKU: {distributor_result['DistributorPartNumber']}): Quantity on Hand: {distributor_result['Stock']['QuantityOnHand']}; Availibility: {distributor_result['Stock']['Availability']}\n"
                                price += f"Offer {i} (SKU: {distributor_result['DistributorPartNumber']}): "
                                for price_tier in distributor_result["Pricing"]["Prices"]:
                                    price += f"Minimum Quantity: {price_tier['Quantity']}; Price: {price_tier['FormattedAmount']}\n"
                                i += 1
                            risk_and_column_dict[supplier.index] = {"stock": stock, "price": price}

        data[variables[mpn]["row_number"]] = risk_and_column_dict

    return data