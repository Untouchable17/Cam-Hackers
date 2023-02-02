#!/usr/bin/env python3

import re

import requests
import colorama
from fake_useragent import UserAgent

from banner import show_banner
from countries import countries_data


colorama.init()
show_banner()


class ScanCameras(object):

    def __init__(self, target: int, headers: dict):

        self.target = target
        self.current_url = "http://www.insecam.org/en/bycountry"
        self.headers = headers
        self.data = countries_data


    def send_request(self):

        if self.target not in range(1, 146):
            print("The specified range does not have this country")
            main()

        country = self.data[self.target - 1]

        request = requests.get(
            f"{self.current_url}/{country}/", headers=self.headers
        )

        return request, country


    def get_cameras_ip(self, status, country: str):
        
        try:
            self.last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', status.text)[0]
        except:
            pass

        for page in range(int(self.last_page)):

            status = requests.get(
                f"{self.current_url}/{country}/?page={page}", headers=self.headers
            )

            ip_addresses = re.findall(r"http://\d+.\d+.\d+.\d+.\d+", status.text)

            for ip in ip_addresses:
                print(f"Found IP: \033[1;31m {ip}")


def main():

    user_agent = UserAgent()

    headers = {
        "User-Agent": user_agent.chrome
    }

    try:
        target = int(input("Choice country: "))
    except ValueError:
        main()

    scanner = ScanCameras(target, headers)
    response = scanner.send_request()

    if response[0].status_code == 404:
        print("No cameras found | HTTP_STATUS_CODE: %d" % response[0].status_code)
        main()

    scanner.get_cameras_ip(response[0], response[1])


main()

