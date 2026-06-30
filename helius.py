import requests
from config import API_KEY, BASE_URL, WALLET, PAGE_LIMIT, MAX_PAGES

#function to fetch the transactions from the api for the given wallet
def fetch_transactions(wallet: str = WALLET) -> list[dict]:
    url = _build_url(wallet)
    all_txns = [] #start with an empty list to store all transactions
    before = None

    for page in range(MAX_PAGES): #for loop to loop through all the pages of transactions
        params = {
            "api-key": API_KEY, #utilzing the api and limit
            "limit":   PAGE_LIMIT,
        }

        # if before is not None means that we only get transactions that occurred before that transaction.
        if before is not None:
            params["before"] = before
        page_data = _get_page(url, params)
        #exit loop if there are no more transactions to fetch
        if not page_data:
            break
        #adds all the transactions that was just collected into page_data
        all_txns.extend(page_data)
        before = page_data[-1]["signature"]
        #print a message to the console to show how many transactions were fetched for that page
        print(f"  Page {page + 1}: fetched {len(page_data)} transactions")

    return all_txns


def _build_url(wallet: str) -> str:
    return f"{BASE_URL}/v0/addresses/{wallet}/transactions"


def _get_page(url: str, params: dict) -> list[dict]:
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()  # throws HTTPError on 4xx/5xx so fetch_transactions sees it
    return response.json()
