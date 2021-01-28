from django.shortcuts import render, HttpResponse
import requests
# Create your views here.
from django.views import View
from covid19_data.models import Global, India, IndiaRegion, CountryData
from datetime import date


# for global data
class Index(View):
    def get(self, request):
        try:
            if Global.objects.filter(date=date.today()).exists():
                from django.db import connection
                cursor = connection.cursor()
                todays_date = date.today()
                query = (
                    f"select * from covid19_data_global where date='{todays_date}'")
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                connection.close()
                for data in result:
                    total_confirm = data[0]
                    total_deaths = data[1]
                    total_recovered = data[2]
                k = CountriesData()
                country = k.getdata(request)
                # print("ok")
                # print(country)
                i = india()
                india_data = i.getdata(request)
                # print(india_data)
                ir = indiaregions()
                india_regions = ir.getdata(request)
                # print(india_regions)
                # print("ok1")
                global_data = {
                    "TotalConfirmed": total_confirm,
                    "TotalDeaths": total_deaths,
                    "TotalRecovered": total_recovered,
                    "country_data": country,
                    "india": india_data,
                    "india_regions": india_regions,
                }
                return render(request, "index.html", global_data)
            else:
                result = requests.get("https://api.covid19api.com/summary")
                # print(result)
                # print(result.json())
                data = result.json()
                global_data = data["Global"]
                # print(global_data)
                # print(global_data["TotalConfirmed"],
                #      global_data["TotalDeaths"], global_data["TotalRecovered"])
                from django.db import connection
                cursor = connection.cursor()
                query = ("insert into covid19_data_global values(%s,%s,%s,%s)")
                values = (global_data["TotalConfirmed"], global_data["TotalDeaths"],
                          global_data["TotalRecovered"], date.today())
                cursor.execute(query, values)
                # now fetch data of todays date
                todays_date = date.today()
                query = (
                    f"select * from covid19_data_global where date='{todays_date}'")
                cursor.execute(query)
                result = cursor.fetchall()
                for data in result:
                    total_confirm = data[0]
                    total_deaths = data[1]
                    total_recovered = data[2]
                k = CountriesData()
                country = k.getdata(request)
                # print(ok)
                i = india()
                india_data = i.getdata(request)
                # print(india_data)
                ir = indiaregions()
                india_regions = ir.getdata(request)
                # print(india_regions)
                global_data = {
                    "TotalConfirmed": total_confirm,
                    "TotalDeaths": total_deaths,
                    "TotalRecovered": total_recovered,
                    "country": country,
                    "india": india_data,
                    "india_regions": india_regions,
                }
                # print("total confirm:",global_data["TotalConfirmed"])
                cursor.close()
                connection.close()
                return render(request, "index.html", global_data)
        except Exception as e:
            print(e)

    def post(self, request):
        return HttpResponse("<h1>Page Not Found! 404 </h1>")


# for country wise data
class CountriesData:
    def getdata(self, request):
        try:
            if CountryData.objects.filter(date=date.today()).exists():
                country_data = self.SelectData(request)
                # print(country_data)
                return country_data
            else:
                country_result = requests.get(
                    "https://api.covid19api.com/summary")
                # print(country_result)
                # print(country_result.json())
                data = country_result.json()
                country_data = data["Countries"]
                # print(country_data)
                from django.db import connection
                cursor = connection.cursor()
                if CountryData.objects.count() > 0:
                    for country_d in country_data:
                        if country_d['Country'] == "Côte d'Ivoire":
                            c = country_d['Country']
                            c1 = c.replace("'", "")
                            country_d['Country'] = c1
                        query = (
                            f"update covid19_data_countrydata set Country='{country_d['Country']}',NewConfirmed={country_d['NewConfirmed']},TotalConfirmed={country_d['TotalConfirmed']},NewDeaths={country_d['NewDeaths']},TotalDeaths={country_d['TotalDeaths']},NewRecovered={country_d['NewRecovered']},TotalRecovered={country_d['TotalRecovered']},date='{date.today()}' where CountryCode='{country_d['CountryCode']}'")
                        # print(query)
                        # print(country_d['Country'])
                        cursor.execute(query)
                else:
                    for country_d in country_data:
                        # to insert cases data into database
                        query = (
                            "insert into covid19_data_countrydata(CountryCode,Country,NewConfirmed,TotalConfirmed,NewDeaths,TotalDeaths,NewRecovered,TotalRecovered,date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                        values = (country_d['CountryCode'], country_d['Country'], country_d['NewConfirmed'], country_d['TotalConfirmed'], country_d['NewDeaths'], country_d['TotalDeaths'],
                                  country_d['NewRecovered'], country_d['TotalRecovered'], date.today())
                        cursor.execute(query, values)
                cursor.close()
                connection.close()
                country_data = self.SelectData(request)
                # print(country_data)
                return country_data
                # return HttpResponse("<h1>ok,it works!</h1>")
        except Exception as e:
            print(e)

    def SelectData(self, request):
        try:
            country_data = CountryData.objects.filter(date=date.today())
            # print(len(country_data))
            return country_data
        except Exception as e:
            print(e)

    def postdata(self, request):
        return HttpResponse("<h1>hello,it's post request!</h1>")


# for indian regions(parts/destricts/states) data
class india:
    def getdata(self, request):
        try:
            if India.objects.filter(date=date.today()).exists():
                india_total = self.selectdata(request)
                return india_total
            else:
                india_result = requests.get(
                    "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true")
                india_data = india_result.json()
                # print("total confirmed:",india_data["totalCases"],"totaldeaths:",india_data["deaths"],"totalrecovered:",india_data["recovered"])
                i = India(TotalConfirmed=india_data["totalCases"], TotalDeaths=india_data["deaths"],
                          TotalRecovered=india_data["recovered"], date=date.today())
                i.save()
                india_total = self.selectdata(request)
                return india_total
            # return HttpResponse("<h1>ok,india!</h1>")
        except Exception as e:
            print(e)

    def selectdata(self, request):
        try:
            india_total = India.objects.filter(date=date.today())
            return india_total
        except Exception as e:
            print(e)

    def postdata(self, request):
        return HttpResponse("<h1>hello,it's post request!</h1>")


class indiaregions:
    def getdata(self, request):
        try:
            if IndiaRegion.objects.filter(date=date.today()).exists():
                india_regions_data = self.selectdata(request)
                return india_regions_data
            else:
                india_result = requests.get(
                    "https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true")
                india_data = india_result.json()
                for region_data in india_data["regionData"]:
                    # print(region_data["region"],region_data["totalInfected"],region_data["newInfected"],region_data["recovered"],region_data["newRecovered"],region_data["deceased"],region_data["newDeceased"],date.today())
                    re = IndiaRegion(Region=region_data["region"], NewConfirmed=region_data["newInfected"], TotalConfirmed=region_data["totalInfected"], NewDeaths=region_data["newDeceased"],
                                     TotalDeaths=region_data["deceased"], NewRecovered=region_data["newRecovered"], TotalRecovered=region_data["recovered"], date=date.today())
                    re.save()
                india_regions_data = self.selectdata(request)
                return india_regions_data
            # return HttpResponse("<h1>ok,india regions!</h1>")
        except Exception as e:
            print(e)

    def selectdata(self, request):
        try:
            india_regions_data = IndiaRegion.objects.filter(date=date.today())
            # for data in regions_data:
            #   print(data.Region,data.NewConfirmed,data.TotalConfirmed,data.NewDeaths,data.TotalDeaths,data.NewRecovered,data.TotalRecovered)
            return india_regions_data
        except Exception as e:
            print(e)

    def postdata(self, request):
        return HttpResponse("<h1>hello,it's post request!</h1>")
