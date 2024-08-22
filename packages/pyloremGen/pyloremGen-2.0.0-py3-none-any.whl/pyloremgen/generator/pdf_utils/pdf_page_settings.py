from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate


class PagesConfigPDF:
    def __init__(self):
        self.page_width, self.page_height = letter
        self.left_margin = 72
        self.right_margin = 72
        self.top_margin = 72
        self.bottom_margin = 72
        self.body_style = ParagraphStyle(name="BodyText")
        self.center_style = ParagraphStyle(name="Center", alignment=1)
        self.right_style = ParagraphStyle(name="Right", alignment=2)
        # Additional configurations can be added here

    def set_margins(self, left, right, top, bottom):
        self.left_margin = left
        self.right_margin = right
        self.top_margin = top
        self.bottom_margin = bottom

    def set_page_size(self, width, height):
        self.page_width = width
        self.page_height = height

    def create_document(self, filename):
        return SimpleDocTemplate(
            filename=filename,
            pagesize=(self.page_width, self.page_height),
            leftMargin=self.left_margin,
            rightMargin=self.right_margin,
            topMargin=self.top_margin,
            bottomMargin=self.bottom_margin,
        )

    def get_max_characters_per_page(self):
        usable_width = self.page_width - self.left_margin - self.right_margin
        usable_height = self.page_height - self.top_margin - self.bottom_margin
        average_character_width = 6  # Adjust as needed
        average_line_height = 12  # Adjust as needed
        max_characters_per_line = int(usable_width / average_character_width)
        max_lines_per_page = int(usable_height / average_line_height)
        return max_characters_per_line * max_lines_per_page
