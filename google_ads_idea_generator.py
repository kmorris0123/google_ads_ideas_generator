import tkinter as tk
from tkinter import ttk
import openai
import csv
import os


def update_progressbar(value):
    progress_bar['value'] = value
    root.update_idletasks()

def generate_ad_ideas():
    openai.api_key = api_key_entry.get()

    company_name = company_name_entry.get()
    keyword = keyword_entry.get()
    city = city_entry.get()
    state = state_entry.get()
    notes = notes_entry.get('1.0', 'end-1c')
    num_ad_ideas = int(num_ad_ideas_entry.get())

    ad_ideas = []

    for i in range(num_ad_ideas):
        ad_idea = {}

        # Generate heading
        heading_prompt = [
            {"role": "system", "content": "You are an AI language model."},
            {"role": "user", "content": f"Generate a Google Ads Heading (max 30 characters) for a company called {company_name} offering {keyword} in {city}, {state}. Additional notes: {notes}"}
        ]

        heading_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=heading_prompt,
            max_tokens=40,
            n=1,
            stop=None,
            temperature=1,
        )
        heading = heading_response.choices[0].message['content'].strip().replace('"',"")
        ad_idea['heading'] = heading

        # Generate descriptions
        descriptions = []
        for i in range(3):
            description_prompt = [
                {"role": "system", "content": "You are an AI language model."},
                {"role": "user", "content": f"Generate a Google Ads Description (max 90 characters) for a company called {company_name} offering {keyword} in {city}, {state} with the heading '{heading}'. Additional notes: {notes}"}
            ]

            description_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=description_prompt,
                max_tokens=100,
                n=1,
                stop=["\n", "\r"],
                temperature=1,
            )
            description = description_response.choices[0].message['content'].strip()
            description = description.replace('\n', ' ').replace('\r', '').replace('"', '')
            descriptions.append(description)
        ad_idea['descriptions'] = descriptions

        ad_ideas.append(ad_idea)
        save_ads_to_csv(company_name, ad_idea)

        update_progressbar((i + 1) / num_ad_ideas * 100)

    progress_bar['value'] = 0


def save_ads_to_csv(company_name, ad_idea):
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    file_name = f"{company_name} Ad Ideas.csv"
    file_path = os.path.join(downloads_folder, file_name)

    # Open the CSV file in append mode
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write the ad idea to the CSV file
        row = [ad_idea['heading']] + ad_idea['descriptions']
        writer.writerow(row)

root = tk.Tk()
root.title("Ad Ideas Generator")

root.geometry("600x400")

company_name_label = tk.Label(root, text="Company Name:")
company_name_label.grid(row=0, column=0, sticky="e")
company_name_entry = tk.Entry(root,width=40)
company_name_entry.grid(row=0, column=1)

keyword_label = tk.Label(root, text="Keyword:")
keyword_label.grid(row=1, column=0, sticky="e")
keyword_entry = tk.Entry(root,width=40)
keyword_entry.grid(row=1, column=1)

num_ad_ideas_label = tk.Label(root, text="Number of Ad Ideas:")
num_ad_ideas_label.grid(row=2, column=0, sticky="e")
num_ad_ideas_entry = tk.Entry(root,width=40)
num_ad_ideas_entry.grid(row=2, column=1)

notes_label = tk.Label(root, text="Notes:")
notes_label.grid(row=3, column=0, sticky="ne")
notes_entry = tk.Text(root, width=40, height=5)
notes_entry.grid(row=3, column=1)

api_key_label = tk.Label(root, text="OpenAI API Key:")
api_key_label.grid(row=4, column=0, sticky="e")
api_key_entry = tk.Entry(root,width=40)
api_key_entry.grid(row=4, column=1)

city_label = tk.Label(root, text="City:")
city_label.grid(row=3, column=0, sticky="e")
city_entry = tk.Entry(root,width=40)
city_entry.grid(row=3, column=1)

state_label = tk.Label(root, text="State:")
state_label.grid(row=4, column=0, sticky="e")
state_entry = tk.Entry(root,width=40)
state_entry.grid(row=4, column=1)

# Update the grid row numbers for the remaining widgets
notes_label.grid(row=5, column=0, sticky="ne")
notes_entry.grid(row=5, column=1)

api_key_label.grid(row=6, column=0, sticky="e")
api_key_entry.grid(row=6, column=1)

progress_label = tk.Label(root, text="Progress:")
progress_label.grid(row=8, column=0, sticky="e")

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.grid(row=8, column=1)

generate_button = tk.Button(root, text="Generate Ad Ideas", command=generate_ad_ideas)
generate_button.grid(row=7, column=1, pady=10)

root.mainloop()

