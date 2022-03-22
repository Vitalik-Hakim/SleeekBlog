import requests

url = "https://motivational-quotes1.p.rapidapi.com/motivation"

payload = {
	"key1": "morning",
	"key2": "study"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Host": "motivational-quotes1.p.rapidapi.com",
	"X-RapidAPI-Key": "54d3930f9dmsh83437c449b45da8p10fcfcjsnba71376c74e2"
}


#Send the request ten times and add it to the list
quote_list = []

for i in range(0,3):
    response = requests.request("POST", url, json=payload, headers=headers)
    quote = response.text
    quote_list.append(quote)




quotes = ''.join(quote_list)

quotes = quotes.replace('"',' " ')
print(quotes)



