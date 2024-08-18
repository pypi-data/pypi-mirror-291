import requests

def get_assets_by_layout_id(api_baseurl, api_key, asset_layout_id):
    headers = {'x-api-key': api_key}
    url = f'{api_baseurl}/assets?asset_layout_id={asset_layout_id}'
    try:
        response = requests.get(url, headers=headers)
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, f"Error fetching assets: {e}"