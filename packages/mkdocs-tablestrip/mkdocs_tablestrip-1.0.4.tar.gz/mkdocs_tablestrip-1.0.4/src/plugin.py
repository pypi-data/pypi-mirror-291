from bs4 import BeautifulSoup
from mkdocs.config import config_options as option
from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin



class TableStripPluginConfig(Config):
    strip_word = option.Type(str)


class TableStrip(BasePlugin[TableStripPluginConfig]):
    strip_word = ""

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_config(self, config: MkDocsConfig) -> None:
        self.strip_word = self.config.strip_word

    def on_page_content(self, html, **args):
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        for table in tables:
            headings = table.find_all('th')
            heading_index = 0
            found_keyword = False

            for heading in headings:
                if heading.text == self.strip_word:
                    found_keyword = True
                    break
                heading_index += 1

            if found_keyword:
                rows = table.find_all('tr')
                for row in rows:
                    # Clear table header Row
                    heading_elements = row.find_all('th')
                    if heading_elements:
                        headings[heading_index].decompose()

                    # Clear all other rows
                    data_elements = row.find_all('td')
                    if data_elements:
                        data_elements[heading_index].decompose()

        return str(soup)
