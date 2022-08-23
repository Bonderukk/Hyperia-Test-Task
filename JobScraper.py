from bs4 import BeautifulSoup
import requests
import json

url = "https://www.hyperia.sk/kariera/"
request = requests.get(url)
soup = BeautifulSoup(request.text, "html.parser")

# Find all divs with job information
job_divs = soup.find_all(class_="offset-lg-1 col-md-10")


def get_job_titles():
    job_titles = []
    for job_div in job_divs:
        job_title = list(job_div)[0].getText()
        # Slovak characters will show correctly
        job_titles.append(job_title.encode('latin-1').decode('utf-8'))

    return job_titles


def get_job_links():
    job_links = []
    for job_div in job_divs:
        k = job_div.find("a", href=True)
        job_links.append("https://www.hyperia.sk" + k['href'])

    return job_links


def get_final_info():
    job_links = get_job_links()
    job_titles = get_job_titles()
    final_info_form = []
    
    for i in range(len(job_links)):
        request = requests.get(job_links[i])
        soup = BeautifulSoup(request.text, "html.parser")
        # Place, salary, contract type
        div_with_rest_of_info = soup.find_all(class_="col-md-4 icon")
        final_job_info = [job_titles[i]]
        
        for job_info in div_with_rest_of_info:
            info_txt = job_info.find("br").next_sibling
            final_job_info.append(info_txt.encode('latin-1').decode('utf-8'))

        final_info_form.append(final_job_info)

    return final_info_form


def dump_to_json():
    final_info = get_final_info()
    json_dump = []
    for job_info in final_info:
        one_job = {
            "title": job_info[0],
            "place": job_info[1],
            "salary": job_info[2],
            "contract_type": job_info[3],
            "contact_email": "hr@hyperia.sk"

        }
        json_dump.append(one_job)

    with open("data.json", "w") as file:
        jsonString = json.dumps(json_dump)
        file.write(jsonString)


def test_output():
    with open("data.json", "r") as file:
        output = json.load(file)

    for x in output:
        print(x)


def main():
    dump_to_json()
    test_output()


if __name__ == "__main__":
    main()
