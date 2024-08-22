import time
import requests
import datetime
import pytz


class Shopify:
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_inventory_locations(self):
        try:
            response = requests.request(
                "GET",
                f"https://{self.url}.myshopify.com/admin/api/2023-10/locations.json?limit=250",
                headers={"X-Shopify-Access-Token": self.token},
            )
            return response.json()["locations"]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_orders(self):
        try:
            shopify_orders = requests.get(
                f"https://{self.url}.myshopify.com/admin/api/2024-01/orders.json?financial_status=paid,refunded&fields=id,location_id,phone,billing_address,fulfillment_status,email,created_at,financial_status,shipping_lines,order_number,customer,created_at,line_items,tags,current_subtotal_price,note,discount_codes&created_at_min={datetime.date.today() - datetime.timedelta(days=7)}&created_at_max={datetime.datetime.now(pytz.timezone('US/Central')) - datetime.timedelta(seconds=10)}&status=any&limit=250",  # noqa
                headers={"X-Shopify-Access-Token": self.token},
            )
            if shopify_orders.status_code == 429:
                retry_after = float(shopify_orders.headers.get("Retry-After", 4))
                print(
                    "Service exceeds Shopify API call limit, "
                    "will retry to send request in %s seconds" % retry_after
                )
                time.sleep(retry_after)
                self.get_orders(self)
            orders_from = shopify_orders.json()["orders"]
            return orders_from
        except requests.exceptions.RequestException as e:
            print(e)

    def mark_order_closed(self, order_id: int, note: str) -> int:
        try:
            new_note = f"zenoti_closed, {note}"
            order_update = requests.put(
                f"https://{self.url}.myshopify.com/admin/api/2024-01/orders/{order_id}.json",  # noqa
                json={"order": {"id": order_id, "note": new_note}},
                headers={"X-Shopify-Access-Token": self.token},
            )
            if order_update.status_code == 429:
                retry_after = float(order_update.headers.get("Retry-After", 4))
                print(
                    "Service exceeds Shopify API call limit, "
                    "will retry to send request in %s seconds" % retry_after
                )
                time.sleep(retry_after)
                self.mark_order_closed(self)
            return order_update.status_code
        except requests.exceptions.RequestException as e:
            print(e)

    def tag_customer_as_patient(self, customerID: int):
        try:
            customer_update = requests.post(
                f"https://{self.url}.myshopify.com/admin/api/2024-01/customers/{customerID}.json",  # noqa
                json={"customer": {"id": customerID, "tags": "patient"}},
                headers={"X-Shopify-Access-Token": self.token},
            )
            if customer_update.status_code == 429:
                retry_after = float(customer_update.headers.get("Retry-After", 4))
                print(
                    "Service exceeds Shopify API call limit, "
                    "will retry to send request in %s seconds" % retry_after
                )
                time.sleep(retry_after)
                self.tag_customer_as_patient(self)
            return customer_update.status_code
        except requests.exceptions.RequestException as e:
            print(e)

    def mark_order_invoiced(
        self, order_id: int, zenoti_invoice_id: int, note: str
    ) -> int:
        try:
            new_note = f"https://options.zenoti.com/Appointment/DlgAppointment1.aspx?history=1&appgroupid=&nbsp;&invoiceid={zenoti_invoice_id}, {note}"  # noqa
            order_update = requests.put(
                f"https://{self.url}.myshopify.com/admin/api/2024-01/orders/{order_id}.json",  # noqa
                json={"order": {"id": order_id, "note": new_note}},
                headers={"X-Shopify-Access-Token": self.token},
            )
            if order_update.status_code == 429:
                retry_after = float(order_update.headers.get("Retry-After", 4))
                print(
                    "Service exceeds Shopify API call limit, "
                    "will retry to send request in %s seconds" % retry_after
                )
                time.sleep(retry_after)
                self.mark_order_invoiced(self)
            print(f"marked order for invoice {zenoti_invoice_id} as invoiced")
            return order_update.status_code
        except requests.exceptions.RequestException as e:
            print(e)

    def order_has_disabled_product(self, order, disabled_barcodes):
        try:
            disabled_product_found = any(
                json_item["variant_id"]
                for json_item in order["line_items"]
                if requests.get(
                    f"https://{self.url}.myshopify.com/admin/api/2024-01/variants/{json_item['variant_id']}.json",  # noqa
                    headers={"X-Shopify-Access-Token": self.token},
                ).json()["variant"]["barcode"]
                in disabled_barcodes
            )
            return disabled_product_found
        except requests.exceptions.RequestException as e:
            print(e)

    def find_location_id(self, order):
        try:
            fulfillment = requests.get(
                f"https://{self.url}.myshopify.com/admin/api/2024-01/orders/{order['id']}/fulfillment_orders.json",  # noqa
                headers={"X-Shopify-Access-Token": self.token},
            )
            if fulfillment.status_code == 429:
                retry_after = float(fulfillment.headers.get("Retry-After", 4))
                print(
                    "Service exceeds Shopify API call limit, "
                    "will retry to send request in %s seconds" % retry_after
                )
                time.sleep(retry_after)
                self.find_location_id(self)

            location = fulfillment.json()["fulfillment_orders"][0]["assigned_location"]
            if location["location_id"] == 80254959897:
                return "Drop Shipping Center"
            else:
                return location["name"]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_item_variant(self, json_item):
        try:
            item_variant = requests.get(
                f"https://{self.url}.myshopify.com/admin/api/2024-01/variants/{json_item['variant_id']}.json",  # noqa
                headers={"X-Shopify-Access-Token": self.token},
            )
            if item_variant.status_code == 429:
                retry_after = float(item_variant.headers.get("Retry-After", 4))
                print(
                    "Service exceeds Shopify API call limit, "
                    "will retry to send request in %s seconds" % retry_after
                )
                time.sleep(retry_after)
                self.get_item_variant(self)
            return item_variant.json()["variant"]
        except requests.exceptions.RequestException as e:
            print(e)


    def get_order_phone_number(self, order):
        if order["billing_address"]["phone"]:
            return order["billing_address"]["phone"]
        elif order["phone"]:
            return order["phone"]
        else:
            return order["customer"]["phone"]

    def get_order_email(self, order):
        if order["email"]:
            return order["email"]
        else:
            return order["customer"]["email"]

    def get_inventory_levels(self, location_id):
        try:
            response = requests.request(
                "GET",
                f"https://{self.url}.myshopify.com/admin/api/2023-10/inventory_levels.json?limit=250&location_ids="
                + str(location_id),
                headers={"X-Shopify-Access-Token": self.token},
            )
            return response.json()["inventory_levels"]
        except requests.exceptions.RequestException as e:
            print(e)

    def get_products(self):
        try:
            response = requests.request(
                "GET",
                f"https://{self.url}.myshopify.com/admin/api/2024-04/products.json?limit=250",
                headers={"X-Shopify-Access-Token": self.token},
            )
            products = response.json()["products"]
            return products
        except requests.exceptions.RequestException as e:
            print(e)

    def is_lipo10(self, item_bar_code):
        if item_bar_code == "INJ-LIPO10ml":
            return True
        else:
            return False

    def is_lipo30(self, item_bar_code):
        if item_bar_code == "INJ-LIPO30ml":
            return True
        else:
            return False

    def get_inventory_item_barcode_and_name(self, item_id):
        try:
            inventory_item_response = requests.post(
                f"https://{self.url}.myshopify.com/admin/api/2023-10/graphql.json",
                headers={"X-Shopify-Access-Token": self.token},
                json={
                    "query": """{
                        inventoryItem(id: "gid://shopify/InventoryItem/"""
                    + str(item_id)
                    + """"){
                            variant{
                                barcode
                                product {
                                    title
                                    status
                                }
                            }
                        }
                    }""",
                },
            )
            inventory_item = inventory_item_response.json()
            status = inventory_item["data"]["inventoryItem"]["variant"]["product"][
                "status"
            ]
            if status != "ACTIVE":
                return None, None

            barcode = inventory_item["data"]["inventoryItem"]["variant"]["barcode"]
            title = inventory_item["data"]["inventoryItem"]["variant"]["product"][
                "title"
            ]

            return barcode, title
        except requests.exceptions.RequestException as e:
            print(e)

    def set_inventory_item_level(self, item_id, location_id, quantity):
        if quantity < 0:
            quantity = 0
        try:
            query = """
                    mutation inventorySetOnHandQuantities($input: InventorySetOnHandQuantitiesInput!) {
                    inventorySetOnHandQuantities(input: $input) {
                        userErrors {
                            field
                            message
                        }
                        inventoryAdjustmentGroup {
                            createdAt
                            reason
                            referenceDocumentUri
                            changes {
                                name
                                delta
                            }
                        }
                    }
                    }
            """
            input = {
                "reason": "correction",
                "referenceDocumentUri": "uri://options.zenoti.com",
                "setQuantities": [
                    {
                        "inventoryItemId": f"gid://shopify/InventoryItem/{item_id}",
                        "locationId": f"gid://shopify/Location/{location_id}",
                        "quantity": round(quantity),
                    }
                ],
            }
            variables = {"input": input}
            response = requests.post(
                f"https://{self.url}.myshopify.com/admin/api/2023-10/graphql.json",
                headers={"X-Shopify-Access-Token": self.token},
                json={"query": query, "variables": variables},
            )
            output = response.json()
            if len(output["data"]["inventorySetOnHandQuantities"]["userErrors"]) > 0:
                raise Exception(
                    output["data"]["inventorySetOnHandQuantities"]["userErrors"]
                )
            return output

        except requests.exceptions.RequestException as e:
            print(e)

    def set_product_name(self, product_id, newName):
        try:
            response = requests.request(
                "PUT",
                f"https://{self.url}.myshopify.com/admin/api/2024-04/products/{product_id}.json",
                headers={"X-Shopify-Access-Token": self.token},
                json={"product": {"id": product_id, "title": newName}},
            )
            print(response.json())

        except requests.exceptions.RequestException as e:
            print(e)

    def make_product_inactive(self, product_id):
        try:
            response = requests.request(
                "POST",
                f"https://{self.url}.myshopify.com/admin/api/2024-04/products/{product_id}/.json",
                headers={"X-Shopify-Access-Token": self.token},
                json={"product": {"id": product_id, "status": "archived"}},
            )
            print(response.json())
        except requests.exceptions.RequestException as e:
            print(e)
