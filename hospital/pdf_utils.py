import logging
from io import BytesIO

from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def render_invoice_pdf(context):
    try:
        from xhtml2pdf import pisa

        html = render_to_string("hospital/patient_final_bill.html", context)
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            logger.error("PDF generation failed with pisa error")
            return None
        return pdf_file.getvalue()
    except Exception:
        logger.exception("PDF generation failed")
        return None
