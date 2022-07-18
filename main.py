import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

DRIVER_PATH = '/home/guillaume/Documents/scraping/chromedriver'
options = Options()
options.add_argument('--headless')
dir_name = "strix_examples"


# options.add_argument("--window-size=1920,1200")

def open_page():
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
    driver.get('https://meyerphi.github.io/strix-demo/')
    list_examples_folders_name, list_examples_folders_id = get_all_folder_examples(driver)
    get_all_examples(driver, list_examples_folders_name, list_examples_folders_id)

    driver.quit()


def get_assumptions(driver):
    # ici on recup tous les elements CodeMirror-code donc 4 pour assumption, guarantees etc
    all_title = driver.find_elements(by=By.XPATH, value="//div[@class = 'CodeMirror-code']")
    # Ici [0] va chercher toutes les assumptions
    all_assumptions = all_title[0].find_elements(by=By.XPATH, value=".//div/pre/span[@role = 'presentation']")
    assumptions_list = []
    for assumption in all_assumptions:
        assumption_value = assumption.text
        if assumption_value == '':
            assumption_value = "true"
        assumptions_list.append(assumption_value)
    return assumptions_list


def get_guarantees(driver):
    all_title = driver.find_elements(by=By.XPATH, value="//div[@class = 'CodeMirror-code']")
    all_guarantees = all_title[1].find_elements(by=By.XPATH, value=".//div/pre[@role = 'presentation']/span[@role = 'presentation']")
    guarantees_list = []
    print("la taille va être de", len(all_guarantees))
    print(all_guarantees)

    for guarantee in all_guarantees:
        guarantee_value = guarantee.text
        if guarantee_value == '':
            print('ERROR')
            guarantee_value = 'ERROR'
        guarantees_list.append(guarantee_value)
    print(guarantees_list)

    return guarantees_list


def get_input_propositions(driver):
    # ici on recup tous les elements CodeMirror-code donc 4 pour assumption, guarantees etc
    all_title = driver.find_elements(by=By.XPATH, value="//div[@class = 'CodeMirror-code']")

    # Ici [1] va chercher toutes les guarantee
    all_input_propositions = all_title[2].find_elements(by=By.XPATH, value=".//pre/span[@role = 'presentation']")
    input_propositions_list = []
    for input_proposition in all_input_propositions:
        input_proposition_value = input_proposition.text
        input_propositions_list.append(input_proposition_value)
    return input_propositions_list


def get_output_propositions(driver):
    # ici on recup tous les elements CodeMirror-code donc 4 pour assumption, guarantees etc
    all_title = driver.find_elements(by=By.XPATH, value="//div[@class = 'CodeMirror-code']")
    # Ici [1] va chercher toutes les guarantees
    all_guarantees = all_title[3].find_elements(by=By.XPATH, value=".//pre/span[@role = 'presentation']")
    output_propositions_list = []
    for output_proposition in all_guarantees:
        output_proposition_value = output_proposition.text
        output_propositions_list.append(output_proposition_value)
    return output_propositions_list


def get_all_folder_examples(driver):
    list_examples_folders_name = []
    list_examples_id = []
    time.sleep(0.3)
    examples_ul = driver.find_element(by=By.XPATH, value="//li[@id = 'examples']/ul")
    examples_all_li = examples_ul.find_elements(by=By.TAG_NAME, value="li")

    for li in examples_all_li:
        list_examples_folders_name.append(li.text)
        list_examples_id.append(li.get_attribute("id"))

    return list_examples_folders_name, list_examples_id


def get_all_examples(driver, list_examples_folders_name, list_examples_folder_id):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print("Directory " + "\"" + dir_name + "\"" + " created ")

    for i in range(len(list_examples_folders_name)):
        path, list_examples_name, list_examples_id = get_simple_folder_example(driver, list_examples_folders_name[i],
                                                                               list_examples_folder_id[i])
        get_example_data(driver, path, list_examples_name, list_examples_id)


def get_simple_folder_example(driver, folder_name, examples_id):
    path = dir_name + "/" + folder_name
    if not os.path.exists(path):
        os.mkdir(path)
        print("Directory " + "\"" + folder_name + "\"" + " created ")

    examples_anchor = driver.find_element(By.ID, examples_id + "_anchor")
    examples_anchor.click()  # open the anchor to display lists
    time.sleep(1)

    examples_ul = driver.find_element(By.ID, examples_id)
    examples_all_li = examples_ul.find_elements(by=By.TAG_NAME, value="li")
    list_examples_name = []
    list_examples_id = []

    for li in examples_all_li:
        list_examples_name.append(li.text)
        list_examples_id.append(li.get_attribute("id"))
    return path, list_examples_name, list_examples_id


def get_example_data(driver, path, list_examples_name, list_examples_id):
    for i in range(len(list_examples_name)):
        examples_anchor = driver.find_element(By.ID, list_examples_id[i] + "_anchor")
        examples_anchor.click()  # open the anchor to display list
        time.sleep(1)
        create_txt_file(driver, path, list_examples_name[i])
        print("File " + "\"" + list_examples_name[i] + "\"" + " created")


def create_txt_file(driver, path, example):
    file = open(path + "/" + example, "w")
    file.write("**NAME**\n\n")
    file.write(example + "\n\n")

    file.write("**ASSUMPTIONS**\n\n")
    assumptions_list = get_assumptions(driver)
    for assumption in assumptions_list:
        file.write(assumption + "\n\n")

    file.write("**GUARANTEES**\n\n")
    guarantees_list = get_guarantees(driver)
    for guarantee in guarantees_list:
        if guarantee == '':
            print('ERROR IN', example)
        file.write(guarantee + "\n\n")

    file.write("**INPUTS**\n\n")
    input_proposition_list = get_input_propositions(driver)
    for input_proposition in input_proposition_list:
        file.write(input_proposition + "\n\n")

    file.write("**OUTPUTS**\n\n")
    output_proposition_list = get_output_propositions(driver)
    for output_proposition in output_proposition_list:
        file.write(output_proposition + "\n\n")

    file.write("**END**")
    file.close()


if __name__ == '__main__':
    open_page()
