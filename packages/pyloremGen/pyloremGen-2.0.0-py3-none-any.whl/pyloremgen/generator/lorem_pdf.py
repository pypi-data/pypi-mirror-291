from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph

from pyloremgen.generator.lorem_text import LoremIpsum
from pyloremgen.generator.pdf_utils.cover_page_template import CoverPageBuilder
from pyloremgen.generator.pdf_utils.pdf_page_settings import PagesConfigPDF


class PDFGenerator:
    def __init__(self, pages_config=None):
        self.pages_config = pages_config or PagesConfigPDF()
        self.lorem = LoremIpsum()

    def generate_pdf(self, filename, num_pages=1, cover_page_count=True):
        self.num_pages = num_pages
        doc = self.pages_config.create_document(filename)
        content = []

        # Add cover page
        cover_builder = CoverPageBuilder()
        cover_content = cover_builder.build_cover_page()
        content.extend(cover_content)

        # Determine starting page based on cover page count
        start_page = 1 if cover_page_count else 0

        # Add page breaks and additional pages if necessary
        for _ in range(start_page, self.num_pages + start_page):
            content.append(PageBreak())

            # Generate lorem ipsum paragraphs for each page
            max_characters_per_page = self.pages_config.get_max_characters_per_page()
            remaining_characters = max_characters_per_page

            while remaining_characters > 0:
                lorem_paragraphs = self.lorem.paragraphs(paragraphs_numbers=1)
                paragraph = " ".join(lorem_paragraphs)
                paragraph_length = len(paragraph)
                if paragraph_length > remaining_characters:
                    # Truncate the paragraph to fit the remaining characters on the page
                    paragraph = paragraph[:remaining_characters]
                content.append(Paragraph(paragraph, getSampleStyleSheet()["Normal"]))
                remaining_characters -= paragraph_length

        doc.build(content)
