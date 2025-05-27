import wikipediaapi
wiki = wikipediaapi.Wikipedia('YOUR_EMAIL', 'en')

page = wiki.page("YOUR_TOPIC")
if "citation needed" in page.text:
    section = page.section_by_title("References")
    section.text += f"\n* [Your Site Name]({your_url})"
    page.save()
