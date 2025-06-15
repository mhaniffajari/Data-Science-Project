from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")
NEWS_API_BASE = "https://api.weather.gov/"
USER_AGENT = "weather-app/1.0"

async def make_news_request(url :str) -> dict[str,any] | None:
    """
    Make a request to NWS API with proper error handling.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept":"application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url,headers=headers,timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            return "I can't access the weather API right now. Please try again later."

def format_alert(feature:dict) -> str:
    """
    Format an altert feature into readable string
    """
    props = feature["properties"]
    return f"""
    Event : {props.get("event","Unknown")}
    Area : {props.get("areaDesc","Unknown")}
    Severity : {props.get("severity","Unknown")}
    Description : {props.get("description","Unknown")}
    Instruction : {props.get("instruction","Unknown")}        
    """
@mcp.tool()

async def get_alerts(state: str) -> str:
    print(f"[DEBUG] Fetching weather alerts for state: {state}")
    url = f"{NEWS_API_BASE}alerts/active?area={state}"
    data = await make_news_request(url)

    if not data or "features" not in data:
        print("[DEBUG] No data or no 'features' key in response.")
        return "Unable to fetch alerts or no alerts found"
    
    if not data["features"]:
        print("[DEBUG] No active alerts in 'features'.")
        return "No active alerts"
    
    alerts = [format_alert(feature) for feature in data["features"]]
    print(f"[DEBUG] Found {len(alerts)} alerts")
    return "\n--\n".join(alerts)

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

CUSTOMER_API_BASE = "https://services.odata.org/v2/northwind/northwind.svc/Customers"
USER_AGENT = "customers-app/1.0"

async def make_customers_request(url: str) -> dict[str, Any] | None:
    """
    Make a request to Customers API with proper error handling.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"  # FIX: should be JSON not GeoJSON
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"[ERROR] {e}")
            return None

def format_customers_data(customer: dict) -> str:
    """
    Format a customer data record into a readable string
    """
    return f"""
    CustomerID : {customer.get("CustomerID", "Unknown")}
    CompanyName : {customer.get("CompanyName", "Unknown")}
    ContactName : {customer.get("ContactName", "Unknown")}
    ContactTitle : {customer.get("ContactTitle", "Unknown")}
    Address : {customer.get("Address", "Unknown")}
    City : {customer.get("City", "Unknown")}
    Region : {customer.get("Region", "Unknown")}
    Country : {customer.get("Country", "Unknown")}        
    """

@mcp.tool()
async def get_customer_data(
    customer_id: str = "",
    company_name: str = "",
    contact_name: str = "",
    contact_title: str = "",
    address: str = "",
    city: str = "",
    region: str = "",
    country: str = ""
) -> str:
    print(f"[DEBUG] Fetching customers data with provided filters")

    # Build dynamic OData filter
    filters = []
    if customer_id:
        filters.append(f"CustomerID eq '{customer_id}'")
    if company_name:
        filters.append(f"CompanyName eq '{company_name}'")
    if contact_name:
        filters.append(f"ContactName eq '{contact_name}'")
    if contact_title:
        filters.append(f"ContactTitle eq '{contact_title}'")
    if address:
        filters.append(f"Address eq '{address}'")
    if city:
        filters.append(f"City eq '{city}'")
    if region:
        filters.append(f"Region eq '{region}'")
    if country:
        filters.append(f"Country eq '{country}'")

    # Build query string
    if filters:
        filter_query = "?$filter=" + " and ".join(filters) + "&$format=json"
    else:
        filter_query = "?$format=json"  # No filters provided

    url = f"{CUSTOMER_API_BASE}{filter_query}"
    print(f"[DEBUG] Generated URL: {url}")

    data = await make_customers_request(url)

    if not data or "d" not in data or "results" not in data["d"]:
        print("[DEBUG] No data or 'results' key not found in response.")
        return "Unable to fetch customers or no customers found."

    customers_list = data["d"]["results"]

    if not customers_list:
        print("[DEBUG] No customers found in 'results'.")
        return "No customers found."

    customers = [format_customers_data(customer) for customer in customers_list]
    print(f"[DEBUG] Found {len(customers)} customers")
    return "\n--\n".join(customers)



@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """ 
    echo a messagge as resource
    """
    return f"Resource echo : {message}"


