from django.shortcuts import render
import requests
import json
import os
from django.urls import reverse_lazy


def currency_data():
    """ All countries currency data"""
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'currencies.json')
    with open(file_path, "r") as f:
        currency_data = json.loads(f.read())
    return currency_data


def currency_data2():
    """ All countries currency data"""
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'currencies2.json')
    with open(file_path, "r") as f:
        currency_data2 = json.loads(f.read())
    return currency_data2


def index(request):
    if request.method == "POST":

        # Get data from the html form
        if request.POST.get('amount').isdigit():
            amount = float(request.POST.get('amount'))
            currency_from = request.POST.get("currency_from")
            currency_to = request.POST.get("currency_to")

            # Get currency exchange rates
            url = f"https://open.er-api.com/v6/latest/{currency_from}"
            d = requests.get(url).json()

            # Converter
            if d["result"] == "success":
                # Get currency exchange of the target
                ex_target = d["rates"][currency_to]

                # Mltiply by the amount
                result = ex_target * amount

                # Set 2 decimal places
                result = "{:.2f}".format(result)

                context = {
                    "result": result,
                    "currency_to": currency_to,
                    "currency_data": currency_data()
                }

                return render(request, "index.html", context)
        else:
            return render(request, "index.html", {"currency_data": currency_data()})

    return render(request, "index.html", {"currency_data": currency_data()})


def dfference(request):
    if request.method == "POST":

        if request.POST.get('amount').isdigit():

            # Get data from the html form
            amount = float(request.POST.get('amount'))
            currency_from = request.POST.get("currency_from")
            currency_to = request.POST.get("currency_to")

            # Get currency exchange rates

            # url = f"https://open.er-api.com/v6/latest/{currency_from}"

            d = {"result": "success", "provider": "https://www.exchangerate-api.com",
                 "documentation": "https://www.exchangerate-api.com/docs/free",
                 "terms_of_use": "https://www.exchangerate-api.com/terms", "time_last_update_unix": 1657497752,
                 "time_last_update_utc": "Mon, 11 Jul 2022 00:02:32 +0000", "time_next_update_unix": 1657585502,
                 "time_next_update_utc": "Tue, 12 Jul 2022 00:25:02 +0000", "time_eol_unix": 0, "base_code": "USD",
                 "rates": {"USD": 1,
                           "1 месяц": 33.67,
                           "3 месяца": 47.53,
                           "6 месяц": 114.07,
                           "1 год": 409.31,
                           "5 лет": 701.79,
                           "10 лет": 1629.56,
                           "15 лет": 3026.03,
                           "30 лет": 5527.46,
                           "50 лет": 12763.79,
                           "100 лет": 36906.69}}

            # Converter
            if d["result"] == "success":
                # Get currency exchange of the target
                #   84    =
                ex_target = d["rates"][currency_to]

                # Mltiply by the amount
                # 8300 =      (84 - 1)   *   100$
                result = (ex_target - 1) * amount

                # Set 2 decimal places
                result = "{:.2f}".format(result)

                ex_target = "{:.2f}".format(ex_target)

                context = {
                    "result": result,
                    "ex_target": ex_target,
                    "currency_to": currency_to,
                    "currency_data2": currency_data2()
                }

                return render(request, "dfference.html", context)
        else:
            return render(request, "dfference.html", {"currency_data2": currency_data2()})

    return render(request, "dfference.html", {"currency_data2": currency_data2()})
