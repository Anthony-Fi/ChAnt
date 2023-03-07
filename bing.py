from bs4 import BeautifulSoup
import requests
from tkinter import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def search():
    query = entry.get()
    url = f"https://www.bing.com/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('li', class_='b_algo')
    top_10_websites = []
    for result in results[:10]:
        website_url = result.find('a')['href']
        top_10_websites.append(website_url)

    text.delete('1.0', END)
    text.insert(END, '\n'.join(top_10_websites))

def save():
    query = entry.get()
    filename = f"{query}_bing.txt"
    with open(filename, 'w') as f:
        f.write(text.get('1.0', END))
    
root = Tk()
root.title("Bing Search")

label = Label(root, text="Enter search query:")
label.pack()

entry = Entry(root)
entry.pack()

search_button = Button(root, text="Search", command=search)
search_button.pack()

text = Text(root)
text.pack()

save_button = Button(root, text="Save", command=save)
save_button.pack()

root.mainloop()