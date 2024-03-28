from ebaysdk.trading import Connection as Trading
import database
import asyncio
from datetime import datetime

class Trader:
    def __init__(self):
        self.api = Trading(domain='api.sandbox.ebay.com',
                  config_file=None,
                  appid='AidanJav-linkedli-SBX-1aec0cd29-2ed6e7cc',
                  devid='dbc7ab68-ddc8-4327-ab11-bcfa8d0f442d',
                  certid='SBX-aec0cd29b2b5-08d2-4fad-bb4c-4909',
                  token='v^1.1#i^1#I^3#f^0#r^1#p^3#t^Ul4xMF85OkE0Q0Q1NEFFQzU5OTA0REIwRUE2M0I2NDU5MkJEMDA5XzBfMSNFXjEyODQ=')

    def find_best_category(self, keywords):
        suggested_categories = self.api.execute('GetSuggestedCategories')

        categories = suggested_categories.get('SuggestedCategoryArray', {}).get('SuggestedCategory', [])
        if not categories:
            print("No categories found.")
            return None

        best_category = categories[0]['Category']
        print(f"Best category for '{keywords}': {best_category['CategoryName']} (ID: {best_category['CategoryID']})")
        return best_category['CategoryID']

    def create_listing(self, title, description, seller, item, price, condition, listing_date):
        request = {
            "Item": {
                "Title": title,
                "Description": description,
                "PrimaryCategory": {"CategoryID": "20081"},
                "StartPrice": str(price),
                "CategoryMappingAllowed": "true",
                "Country": "US",
                "Currency": "USD",
                "ConditionID": "1000", # Brand new
                "DispatchTimeMax": "3",
                "ListingDuration": "Days_7",
                "ListingType": "FixedPriceItem",
                # Payment/Address will be from seller info
                "PaymentMethods": ["PayPal"],
                "PayPalEmailAddress": "seller@example.com",
                "PostalCode": "12345",
                "Quantity": "1",
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_30",
                    "Description": "Temp description. Selling bike",
                    "ShippingCostPaidByOption": "Buyer"
                },
                "ShippingDetails": {
                    "ShippingType": "Flat",
                    "ShippingServiceOptions": {
                        "ShippingServicePriority": "1",
                        "ShippingService": "USPSMedia",
                        "ShippingServiceCost": "10.00"
                    }
                },
                "Site": "US"
            }
        }

        try:
            response = self.api.execute('AddItem', request)
            print(f'Successfully listed item with ItemID: {response.reply.ItemID}')
            asyncio.run(database.add_listing_to_db(title, description, seller, item, response.reply.ItemID, price, condition, listing_date))
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
                return False
        except Exception as e:
            print(f'Exception during end listing: {e}')
            return False

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