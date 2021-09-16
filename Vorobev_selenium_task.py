from selenium import webdriver
import time
import sys

def main():

    # initialize some variables
    is_day = True
    i = 0
    min_time_of_contribution_array = []
    min_summary_array = []
    min_time_and_summary_array = []
    bank_names_array = []
    effective_rate_array = []
    url = 'https://www.banki.ru/products/deposits/?source=main_menu_deposits'

    # set the necessary parameters
    try:
        driver = webdriver.Firefox()
        driver.get(url)
    except Exception as e:
        print(e, '\n', 'input link not found')
        driver.close()
        sys.exit(-1)

    # click the button needs to change the city
    name_city = "Брянск"
    choise_city_button = driver.find_element_by_xpath \
        ("//span[@data-module-dependencies='react-common']") \
            .click()
    input_text_line = driver.find_element_by_xpath \
        ("//input[@placeholder='Введите название города']") \
            .send_keys(name_city)
    time.sleep(1)
    first_proposed_city = driver.find_element_by_xpath \
        ("//li[@data-suggestion-index='0']").click()

    # choose the rest parameters
    sum_of_contribution = "1500"
    currency = '$'
    term = '1 год'

    # click the button to change the currency
    change_the_sum_and_term = driver.find_elements_by_xpath(
        "//div[@data-test='dropdown-button']")
    change_the_sum_and_term[0].click()

    choice_the_sum_and_term = driver.find_element_by_xpath(
        "//div[@data-placement='bottom']").find_elements_by_css_selector(
        'ul')[0].find_element_by_xpath("//div[text()='" + currency + "']")
    choice_the_sum_and_term.click()

    # click the button to change the term
    change_the_sum_and_term[1].click()

    # choice_the_sum_and_term = driver.find_element_by_xpath(
    #     "//div[@data-placement='bottom']").find_elements_by_css_selector(
    #     'ul')[0].find_element_by_xpath("//div[text()='" + term + "']")

    element = driver.find_element_by_xpath('//div[text()="1 год"]/..') 
    driver.execute_script("arguments[0].click();", element)
    # choice_the_sum_and_term.click()

    # input the sum of contribution in line
    input_sum_of_contribution_line = driver.find_element_by_xpath \
        ("//input[@placeholder='Любая сумма']").send_keys(sum_of_contribution)
    time.sleep(1)

    # searching a button "Show more" and click while it won't disappear
    try:
        while driver.find_element_by_xpath \
            ("//span[text()='Показать еще']") != None:
            append_banks_button = driver.find_element_by_xpath \
                ("//span[text()='Показать еще']").click()
            time.sleep(1)
    except Exception as e:
        pass
    
    # table parsing proccess
    rows = driver.find_elements_by_xpath("//div[@data-test='grid-row']")
    for row in rows[1:]:
        # parsing the names of proposed banks 
        temp = row.find_elements_by_xpath("//div[@data-test='bank-logo']")
        bank_names_column = temp[i].find_elements_by_css_selector('img')
        i += 1
        for bank_name in bank_names_column:
            bank_names_array.append(bank_name.get_attribute('title'))
        
        # parsing the persents of proposed banks
        percent_column = row.find_elements_by_css_selector('div.text-size-3')
        for percent in percent_column:
            effective_rate_array.append(percent.text)
        
        # parsing the minimum time of contribution and min summary of proposed banks
        min_time_of_contribution_col = row.find_elements_by_css_selector(
            'div.text-size-4')
        for min_time_of_contribution in min_time_of_contribution_col:
            min_time_and_summary_array = min_time_of_contribution.text.split("\n")

            # to separate a two columns
            for value in min_time_and_summary_array:
                if is_day:
                    min_time_of_contribution_array.append(value)
                    is_day = False
                    continue
                else:
                    min_summary_array.append(value)
                    is_day = True
                    continue
    
    # show the parsed data
    for i in range(len(bank_names_array)):
        print(str(i + 1) + '. ', bank_names_array[i], " ", effective_rate_array[i], " ",
        min_time_of_contribution_array[i], " ", 
        min_summary_array[i], '\n')
    driver.close()

if __name__ == "__main__":
    main()