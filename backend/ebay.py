from ebaysdk.trading import Connection as Trading
import database
import asyncio
from datetime import date
from fuzzywuzzy import process

class Trader:
    def __init__(self):
        self.api = Trading(domain='api.sandbox.ebay.com',
                  config_file=None,
                  appid='AidanJav-linkedli-SBX-1aec0cd29-2ed6e7cc',
                  devid='dbc7ab68-ddc8-4327-ab11-bcfa8d0f442d',
                  certid='SBX-aec0cd29b2b5-08d2-4fad-bb4c-4909',
                  token='v^1.1#i^1#I^3#f^0#r^1#p^3#t^Ul4xMF85OkE0Q0Q1NEFFQzU5OTA0REIwRUE2M0I2NDU5MkJEMDA5XzBfMSNFXjEyODQ=')

    def get_category(self, search_name):
        try:
            api = Trading(domain='api.sandbox.ebay.com',
                config_file=None,
                appid='AidanJav-linkedli-SBX-1aec0cd29-2ed6e7cc',
                devid='dbc7ab68-ddc8-4327-ab11-bcfa8d0f442d',
                certid='SBX-aec0cd29b2b5-08d2-4fad-bb4c-4909',
                token='v^1.1#i^1#I^3#f^0#r^1#p^3#t^Ul4xMF85OkE0Q0Q1NEFFQzU5OTA0REIwRUE2M0I2NDU5MkJEMDA5XzBfMSNFXjEyODQ=')

            response = api.execute('GetCategories', {
                'DetailLevel': 'ReturnAll',
                'CategorySiteID': '0',
                'LevelLimit': 10  # Adjust based on depth (keep 10)
            })

            categories = response.dict().get('CategoryArray', {}).get('Category', [])
            names = [(category['CategoryName'], category['CategoryID']) for category in categories]
            
            # Find the closest match
            best_match = process.extractOne(search_name, names, score_cutoff=70)  # Adjust score_cutoff as needed
            
            if best_match:
                return str(best_match[0][1])
            else:
                return '37978'

        except Exception as e:
            print("Error:", e)
        
    def create_listing(self, title, description, item, price):
        request = {
        'Item': {
            'Title': title,
            'Description': description,
            'PrimaryCategory': {'CategoryID': self.get_category(item)}, # Category id
            'StartPrice': price,
            'ConditionID': '3000',  # Condition ID (used)
            'CategoryMappingAllowed': True,
            'Country': 'US',
            'Currency': 'USD',
            'DispatchTimeMax': '3',
            'ListingDuration': 'GTC',  # Good Til Cancelled
            'ListingType': 'FixedPriceItem',
            'PaymentMethods': [],
            'PostalCode': '94043',
            'Quantity': '1',
            'ReturnPolicy': {
                'ReturnsAcceptedOption': 'ReturnsAccepted',
                'RefundOption': 'MoneyBack',
                'ReturnsWithinOption': 'Days_30',
                'ShippingCostPaidByOption': 'Buyer'
            },
            'ShippingDetails': {
                'ShippingType': 'Flat',
                'ShippingServiceOptions': {
                    'ShippingServicePriority': '1',
                    'ShippingService': 'UPSGround',
                    'ShippingServiceCost': '0.00'
                }
            },
            'Site': 'US'
        }
    }

        try:
            response = self.api.execute('AddItem', request)
            print(f'Successfully listed item with ItemID: {response.reply.ItemID}')
            # asyncio.run(database.add_listing_to_db(title, description, seller, item, response.reply.ItemID, price, date.today().strftime("%m/%d/%y")))
        except Exception as e:
            print(f'Failed to list item: {e}')
    
    def end_listing(self, item_id, reason = "NotAvailable"):
        try:
            response = self.api.execute('EndItem', {
                'ItemID': item_id,
                'EndingReason': reason
            })
            if response.reply.Ack == 'Success':
                print(f'Successfully ended listing with ItemID: {item_id}')
                return True
            else:
                print(f'Failed to end listing. Error: {response.reply.Errors.LongMessage}')
        except Exception as e:
            print(f'Exception during end listing: {e}')

    def change_listing_title(self, item_id, new_title):

        request = {
            'Item': {
                'ItemID': item_id,
                'Title': new_title
            }
        }

        try:
            response = self.api.execute('ReviseItem', request)
            if response.reply.Ack == 'Success':
                print(f"Listing {item_id} has been successfully updated with the new title: {new_title}")
            else:
                print(f"Failed to update the listing {item_id}. Error: {response.reply.Errors.ErrorClassification}")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def get_messages(self):
        try:
            request = {
                'DetailLevel': 'ReturnSummary',
                'Pagination': {
                    'EntriesPerPage': 100,
                    'PageNumber': 1
                }
            }

            # Call the GetMyMessages eBay API
            response = self.api.execute('GetMyMessages', request)
            
            response_dict = response.dict()
            if int(response_dict['Summary']['NewMessageCount']) > 0:
                messages = response_dict['Messages']['Message']
                for message in messages:
                    print(f"Message ID: {message['MessageID']}")
                    print(f"Sender: {message['Sender']}")
                    print(f"Subject: {message['Subject']}")

            return int(response_dict['Summary']['NewMessageCount'])

        except Exception as e:
            print(f"Error: {str(e)}")

# Code which creates a listing for a camry
# x = Trader()
# x.create_listing("2008 Toyota Camry", "old car for sale", "Automobile", 2000) # title, description, item, price
