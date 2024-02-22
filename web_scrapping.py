import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

headers_gen = Headers(os='win', browser='chrome')
headers = headers_gen.generate()

main_hh = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers)
main_hh_html = main_hh.text

main_soup = BeautifulSoup(main_hh_html, features='lxml')
vacancies_list = main_soup.find('div', id='a11y-main-content')

vacancies_tags = vacancies_list.find_all('div','serp-item_link')


final_vacancy_list = []
for vacancy_tag in vacancies_tags:
    a_tag = vacancy_tag.find('a', 'bloko-link')
    link = a_tag['href']
    salary_tag = vacancy_tag.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
    # Переходим на страницу каждой вакансии
    vacancy_full= requests.get(link, headers=headers_gen.generate())
   
    vacancy_full_html = vacancy_full.text    

    vacancy_full_soup = BeautifulSoup(vacancy_full_html, features='lxml')
    # Получаем описание вакансии
    vacancy_description_tags = vacancy_full_soup.find('div', 'vacancy-section')
    vacancy_description = vacancy_description_tags.get_text().strip()
    # Получаем название компании
    company_tag = vacancy_full_soup.find('span', 'vacancy-company-name')
    company = company_tag.get_text()
    # Получаем название города
    city_tags = vacancy_full_soup.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tags.get_text().split(',')[0]
    
    if 'Django' in vacancy_description or 'Flask' in vacancy_description:
        vacancy_data ={}

        vacancy_data['link'] = link
        if salary_tag != None:
            vacancy_data['salary'] = salary_tag.get_text()

        else:
            vacancy_data['salary'] = salary_tag

        vacancy_data['company'] = company
        vacancy_data['city'] = city
        final_vacancy_list.append(vacancy_data)

with open('final_vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(final_vacancy_list, f, indent=2, ensure_ascii=False)