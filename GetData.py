from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
import re
from itertools import groupby
import pandas as pd
import googlemaps

browser = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/apartamento_residencial/#onde=BR-Santa_Catarina-NULL-Florianopolis&tipos=apartamento_residencial'
browser.get(url)
API_key = 'INSERIR API KEY'
gmaps = googlemaps.Client(key=API_key)

quartos = []
tamanho = []
garagem = []
suite = []
mobiliado = []
prices = []
endereco = []
bairro = []
suites = []
banheiros = []
areaServico = []
churrasqueira = []
varanda = []
lavanderia = []
playground = []
arCondicionado = []
salaoFestas = []
piscina = []
distancia = []

for idxPage in range(2,75): # sub 15 para todas as paginas de Florianopolis
    print('Iniciando Pagina ' + str(idxPage))
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Tamanho
    spans = soup.find_all('span', {'class' : 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area'})
    spans = spans[0:35]
    for span in spans:
        temp = span.get_text()
        tamanho.append([int(''.join(i)) for is_digit, i in groupby(temp, str.isdigit) if is_digit][0])

    # Apartamentos
    listagems = soup.find_all('div',{'class': 'property-card__main-content'})
    listagems = listagems[0:35]
    for l in listagems:

    #     Tamanho:
        type = ('span','class')
        property = 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area'
        temp = l.find_all(type[0], {type[1] : property})
        if temp:
            temp = temp[0].contents[0]
            temp = [int(''.join(i)) for is_digit, i in groupby(temp, str.isdigit) if is_digit]
            if temp:
                temp = temp[0]
            else:
                temp = 0
            tamanho.append(temp)
        else:
            tamanho.append(0)

    #         Quartos
        type = ('li','class')
        property = 'property-card__detail-item property-card__detail-room js-property-detail-rooms'
        temp = l.find_all(type[0], {type[1] : property})
        if temp:
            temp = temp[0].contents[1].contents[0]
            temp = [int(''.join(i)) for is_digit, i in groupby(temp, str.isdigit) if is_digit]
            if temp:
                temp = temp[0]
            else:
                temp = 0
            quartos.append(temp)
        else:
            quartos.append(0)

    #         Suites
        type = ('li', 'class')
        property = 'property-card__detail-item property-card__detail-item-extra js-property-detail-suites'
        temp = l.find_all(type[0], {type[1]: property})
        if temp:
            temp = temp[0].contents[1].contents[0]
            temp = [int(''.join(i)) for is_digit, i in groupby(temp, str.isdigit) if is_digit]
            if temp:
                temp = temp[0]
            else:
                temp = 0
            suites.append(temp)
        else:
            suites.append(0)

    #     Banheiros
        type = ('li', 'class')
        property = 'property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom'
        temp = l.find_all(type[0], {type[1]: property})
        if temp:
            temp = temp[0].contents[1].contents[0]
            temp = [int(''.join(i)) for is_digit, i in groupby(temp, str.isdigit) if is_digit]
            if temp:
                temp = temp[0]
            else:
                temp = 0
            banheiros.append(temp)
        else:
            banheiros.append(0)

    #     Garagem
        type = ('li', 'class')
        property = 'property-card__detail-item property-card__detail-garage js-property-detail-garages'
        temp = l.find_all(type[0], {type[1]: property})
        if temp:
            temp = temp[0].contents[1].contents[0]
            temp = [int(''.join(i)) for is_digit, i in groupby(temp, str.isdigit) if is_digit]
            if temp:
                temp = temp[0]
            else:
                temp = 0
            garagem.append(temp)
        else:
            garagem.append(0)

    #     Amenities
        type = ('ul', 'class')
        property = 'property-card__amenities'
        temp = l.find_all(type[0], {type[1]: property})
        temp = str(temp)
        if 'Área de serviço' in temp:
            areaServico.append(True)
        else:
            areaServico.append(False)

        if 'Churrasqueira' in temp:
            churrasqueira.append(True)
        else:
            churrasqueira.append(False)

        if 'Varanda' in temp:
            varanda.append(True)
        else:
            varanda.append(False)

        if 'Mobiliado' in temp:
            mobiliado.append(True)
        else:
            mobiliado.append(False)

        if 'Lavanderia' in temp:
            lavanderia.append(True)
        else:
            lavanderia.append(False)

        if 'Playground' in temp:
            playground.append(True)
        else:
            playground.append(False)

        if 'Salão de festas' in temp:
            salaoFestas.append(True)
        else:
            salaoFestas.append(False)

        if 'Ar-condicionado' in temp:
            arCondicionado.append(True)
        else:
            arCondicionado.append(False)

        if 'Piscina' in temp:
            piscina.append(True)
        else:
            piscina.append(False)

    # Endereço
        type = ('span', 'class')
        property = 'poi__address'
        temp = l.find_all(type[0], {type[1]: property})
        if temp[0].contents:
            temp = temp[0].contents[0]
            endereco.append(temp)
            my_dist = gmaps.distance_matrix(temp, 'Shopping Beira Mar - Florianopolis')['rows'][0]['elements'][0]
            if my_dist['status'] == 'NOT_FOUND':
                distancia.append('NaN')
            else:
                distancia.append(my_dist['distance']['text'])
            str2Find = ' - '
            if temp.count(str2Find) <= 1:
                str2Find = ','
                idx1 = temp.find(str2Find)
                temp = temp[:idx1]
            else:
                idx0 = temp.find(str2Find)
                temp = temp[idx0+3:]
                str2Find = ','
                idx1 = temp.find(str2Find)
                temp = temp[:idx1]
            bairro.append(temp)
        else:
            endereco.append(0)
            bairro.append(0)
            distancia.append('NaN')

    #     Preço
        type = ('div', 'class')
        property = 'property-card__price js-property-card-prices js-property-card__price-small'
        temp = l.find_all(type[0], {type[1]: property})
        if temp:
            temp = temp[0].contents[0]
            str2Find = 'R$'
            idx0 = temp.find(str2Find)
            temp = temp[idx0+3:]
            myString = temp
            stringParts = myString.split(".")
            newString = "".join(stringParts)
            temp = float(newString)
            prices.append(temp)
        else:
            prices.append(0)

    newURL = 'https://www.vivareal.com.br/aluguel/santa-catarina/florianopolis/apartamento_residencial/?pagina='+str(idxPage)
    browser.get(newURL)
    time.sleep(2)  # seconds

browser.close()

df = pd.DataFrame(list(zip(tamanho, quartos,suites,banheiros,garagem,areaServico,churrasqueira,varanda,mobiliado,lavanderia,playground,salaoFestas,arCondicionado,piscina,endereco,bairro,prices)),
               columns =['Tamanho', 'Quartos','Suites','Banheiros','Garagem','AreaServico','Churrasqueira','Varanda','Mobiliado','Lavanderia','Playground','SalaoFestas','ArCondicionado','Piscina','Endereco','Bairro','Prices'])

df.to_csv('RealFlorianopolis', index=False)