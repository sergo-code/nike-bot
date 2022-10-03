import json
import aiohttp
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/104.0.5112.124 YaBrowser/22.9.2.1495 Yowser/2.5 Safari/537.36',
    'cookie': 'CONSUMERCHOICE=us/en_us'
}


async def request(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            await response.text()
            return response


async def get_item(url):
    if len(url.split('/')) == 7:
        model = url.split('/')[-1]
    elif len(url.split('/')) == 6:
        response = await request(url, headers)
        assert response.status == 200
        soup = BeautifulSoup(await response.text(), 'html.parser')
        model = soup.find('li', class_='description-preview__style-color ncss-li').text.split()[1]

    dict_model_size = {}
    dict_model_available_size = {}

    array_available = []
    response = await request(url, headers)
    assert response.status == 200
    soup = BeautifulSoup(await response.text(), 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__')
    data = json.loads(data.text)
    product = data['props']['pageProps']['initialState']['Threads']['products'][model]

    data_product = dict(
        model=model,
        title=product['title'].replace("'", ""),
        full_price=product["fullPrice"],
        current_price=product["currentPrice"],
        discounted=product['discounted'],
        cloud_product_id=product["id"],
        image_url=product['nodes'][0]['nodes'][0]['properties']['squarishURL'],
        product_type=product["productType"],
        seller=soup.find('h2', class_="headline-5").text.replace("'", ""),
        url=url
    )
    for i in range(len(product["skus"])):
        sizeUS = product["skus"][i]['nikeSize']
        sizeID = product["skus"][i]['skuId']
        dict_model_size.setdefault(model, []).append(sizeUS)
        dict_model_size.setdefault(model, []).append(sizeID)
    dict_model_available_size.setdefault(model, [])
    for i in range(len(product["availableSkus"])):
        products_sku_available = product["availableSkus"][i]['skuId']
        dict_model_available_size.setdefault(model, []).append(products_sku_available)

    for i in range(0, len(dict_model_size[model]), 2):
        if dict_model_size[model][i + 1] in dict_model_available_size[model]:
            array_available.append(dict_model_size[model][i])

    data_product['size'] = array_available
    return data_product


if __name__ == '__main__':
    url = input()
    get_item(url)
