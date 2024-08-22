import datetime

from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer


class CoverPageBuilder:
    def __init__(self, title="Main Title"):
        self.title = title
        self.styles = getSampleStyleSheet()

    def build_cover_page(self):
        cover_content = []
        # Add top title
        top_title = Paragraph("Lorem PDF", style=self.styles["Title"])
        cover_content.append(top_title)
        cover_content.append(Spacer(1, 100))  # Add space between titles
        # Add main title
        main_title = Paragraph(self.title, style=self._center_style)
        cover_content.append(main_title)
        # Add bottom datetime
        current_dt = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        bottom_dt = Paragraph(current_dt, style=self._center_style)
        cover_content.append(Spacer(1, 100))  # Add space before datetime
        cover_content.append(bottom_dt)
        return cover_content

    @property
    def _center_style(self):
        return ParagraphStyle(name="Center", alignment=1)
