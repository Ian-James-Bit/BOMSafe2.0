import pytest
from src.excel import reading

@pytest.fixture
def example_response():
    return {'Messages': [],
             'PartResults': [
                    {
                    'PartNumber': 'BAT54BRW-7-F', 
                    'Manufacturer': 'Diodes Incorporated', 
                    'ManufacturerId': 529, 'ProductUrl': 'https://www.trustedparts.com/en/part/diodes/BAT54BRW-7-F', 
                    'Specifications': 
                        [
                            {'Key': 'Configuration', 'Value': 'Double Dual Series'}, 
                            {'Key': 'If - Forward Current', 'Value': '200 mA'}, 
                            {'Key': 'Ifsm - Forward Surge Current', 'Value': '600 mA'}, 
                            {'Key': 'Ir - Reverse Current', 'Value': '2 uA'}, 
                            {'Key': 'Maximum Operating Temperature', 'Value': '+ 125 C'}, 
                            {'Key': 'Minimum Operating Temperature', 'Value': '- 65 C'}, 
                            {'Key': 'Mounting Style', 'Value': 'SMD/SMT'}, 
                            {'Key': 'Package / Case', 'Value': 'SOT-363-6'}, 
                            {'Key': 'Product', 'Value': 'Schottky Diodes'}, 
                            {'Key': 'Series', 'Value': 'BAT54BRW'}, {'Key': 'Technology', 'Value': 'Si'}, 
                            {'Key': 'Vf - Forward Voltage', 'Value': '1 V'}, 
                            {'Key': 'Vrrm - Repetitive Reverse Voltage', 'Value': '30 V'}
                        ], 
                    'IsAffectedByTariff': True, 
                    'LifecycleRisk': 'Low', 
                    'SupplyChainRisk': 'High', 
                    'Distributors': 
                        [
                            {
                                'Id': 4, 
                                'Name': 'DigiKey', 
                                'DistributorResults': 
                                    [
                                        {
                                            'Description': 'Diode Array 2 Pair Series Connection 30 V 200mA (DC) Surface Mount 6-TSSOP, SC-88, SOT-363', 
                                            'DistributorPartNumber': 'BAT54BRW-FDICT-ND', 
                                            'Compliance': {'RoHS':[{'Region': None, 'IsCompliant': True, 'Description': None}]}, 
                                            'Stock': {'QuantityOnHand': 0.0, 'Availability': 'Factory Lead Time: 44 Weeks'}, 
                                            'Links': [{'Type': 'View', 'Url': 'https://www.trustedparts.com/productredirect?e=UHJlY2lzZSBTeXN0ZW1z&id=H4sIAAAAAAAAA1WQW2vCQBhE_8s8r8aaRO1CKN4KQgVJtD60JWx3v6aLJhv20mBL_3vJk_X1zDAD5wcr8IRhC56O7xmKHfgLFvN9mizy42A6eMQbQ74Dv4UMBTjmu83XGAxLcCyD86YmC4Y1eBPOZ4YDOD69bx2Poq7rhkpX-kSXoTQ1T5I4oiZqrVFBehcp8kKfI6WNIjfQjTS2NVZ4UtH_5-huFk8no_ThuB9-l1KrzNJH2ZASpTrJ8j1cGtOVrSWpHbmL81S71zAajSfB16UzwUrKSGpxhTUpHepMVJWlSnhjr5EUdSt01WS3g2DYg-NZUweGvDexXeeb5bwAwxM4qOmt9FoOxapvF-B309kkmaVxHP_-Aa-zw6R2AQAA&h=47007023304216B00F78F2295A7D1139A10F6D60'}, {'Type': 'Datasheet', 'Url': 'https://www.trustedparts.com/productredirect?e=UHJlY2lzZSBTeXN0ZW1z&id=H4sIAAAAAAAAA1WOSwuCQBSF_8tZ35RSe9ydOgVBgcwYs4gQyYkCzWimXET_PaZF0O5wOI_vBQGOCVtwMlkQVAHeI0vLJM6kHs1GKxwIsgD_mwQFRlqsnxMQcjDyh3V9Z-4gLMHXR9sSdmCcnbtZDsNhGILm0jfGBse-C2trjbOhqF1tz8bL736pq1ToKhe6UkJXmdTBrTmBUILxC4Mg_f12Kdd5qkDYgGGuHsWz7JTwFQUez-bTeJ5EUfT-APQtdVHrAAAA&h=74962AFE66BE540EC2EE87868E93FCBE3121DA30'}], 
                                            'Pricing': {'CurrencyCode': 'USD', 'MinimumQuantity': 1.0, 'QuantityMultiple': None, 'Prices': [{'Quantity': 1.0, 'Amount': 0.94, 'FormattedAmount': '$0.94', 'Text': '0.94'}, {'Quantity': 10.0, 'Amount': 0.581, 'FormattedAmount': '$0.581', 'Text': '0.581'}, {'Quantity': 25.0, 'Amount': 0.4852, 'FormattedAmount': '$0.4852', 'Text': '0.4852'}, {'Quantity': 50.0, 'Amount': 0.4258, 'FormattedAmount': '$0.4258', 'Text': '0.4258'}, {'Quantity': 100.0, 'Amount': 0.3755, 'FormattedAmount': '$0.3755', 'Text': '0.3755'}, {'Quantity': 3000.0, 'Amount': 0.22214, 'FormattedAmount': '$0.22214', 'Text': '0.22214'}, {'Quantity': 9000.0, 'Amount': 0.19455, 'FormattedAmount': '$0.19455', 'Text': '0.19455'}]}, 
                                            'Packaging': [{'PackageType': 'Digi-Reel®', 'MinimumOrderQuantity': 1}, {'PackageType': 'Cut Tape (CT)', 'MinimumOrderQuantity': 1}, {'PackageType': 'Tape & Reel (TR)', 'MinimumOrderQuantity': 1}]
                                        }
                                    ]
                            }
                        ]
                    }
                ], 
                'OriginalRequest': {"secret data" : "you dont get to know"}
    }

@pytest.fixture
def variables():
    return {
            'BAT54BRW-7-F': {
                'row_number': 2,
                'suppliers': [
                    reading.Supplier(name='DigiKey', index=3)
                ]
            }
        }

@pytest.fixture
def expected_output():
    return {
            2: {
                'risk': 'Life Cycle Risk: Low; Supply Chain Risk: High\n',
                3: {
                    'stock': 'Offer 1 (SKU: BAT54BRW-FDICT-ND):\n Quantity on Hand: 0.0; Availibility: Factory Lead Time: 44 Weeks\n',
                    'price': 'Offer 1 (SKU: BAT54BRW-FDICT-ND):\n Minimum Quantity: 1.0; Price: $0.94\nMinimum Quantity: 10.0; Price: $0.581\nMinimum Quantity: 25.0; Price: $0.4852\nMinimum Quantity: 50.0; Price: $0.4258\nMinimum Quantity: 100.0; Price: $0.3755\nMinimum Quantity: 3000.0; Price: $0.22214\nMinimum Quantity: 9000.0; Price: $0.19455\n'
                }
            }
        }
    