from tkinter import *
from bs4 import BeautifulSoup
import requests
import csv

def scrape():
    # Get URL from entry field
    url = url_entry.get()
    
    # Make request
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    r = requests.get(url, headers=headers)

    # Parse HTML
    soup = BeautifulSoup(r.text, 'html.parser')

    # Get HTML tags
    tags = ['title', 'h1', 'h2', 'h3']
    tag_values = {tag: soup.find(tag).get_text() if soup.find(tag) else 'none' for tag in tags}

    meta_tags = ['description', 'keywords', 'robots']
    meta_values = {tag: soup.find('meta', attrs={'name': tag})['content'] if soup.find('meta', attrs={'name': tag}) else 'none' for tag in meta_tags}

    canonical = soup.find('link', {'rel': 'canonical'})
    canonical_value = canonical['href'] if canonical else 'none'

    # Find img tags
    img_tags = soup.find_all('img')

    # Create CSV file name using URL
    csv_file_name = f"{url.replace('/', '-').replace(':', '-').replace('.', '-')}.csv"

    # Save data as CSV file
    with open(csv_file_name, mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Canonical'])
        writer.writerow([canonical_value])
        writer.writerow(['Title'])
        writer.writerow([tag_values['title']])
        writer.writerow(['Description'])
        writer.writerow([meta_values['description']])
        writer.writerow(['Keywords','Meta Robots'])
        writer.writerow([meta_values['keywords'], meta_values['robots']])
        
        for tag in tags[1:]:
            writer.writerow([tag.capitalize()])
            writer.writerow([tag_values[tag]])
        
        # Loop img tags and fetch source - alt text
        for img in img_tags:
            img_src = img.get('src')
            img_alt = img.get('alt')
            # Writing data to CSV file
            writer.writerow([img_src, img_alt])

# Create GUI window and widgets
root = Tk()
root.title("Web Scraper")

url_label = Label(root, text="Enter URL:")
url_entry = Entry(root)
go_button = Button(root, text="Go", command=scrape)

# Layout widgets using grid layout manager
url_label.grid(row=0, column=0)
url_entry.grid(row=0, column=1)
go_button.grid(row=1,columnspan=2)

root.mainloop()