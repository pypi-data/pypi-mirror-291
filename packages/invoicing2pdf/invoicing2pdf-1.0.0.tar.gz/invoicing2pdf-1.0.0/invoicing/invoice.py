from fpdf import FPDF
from pathlib import Path
import pandas as pd
import glob
import os


def add_line_pdf(prod_id, prod_name, amount, unit_price, total_price, pdf, bold: bool = False):
    if bold:
        pdf.set_font(family="Times", size=10, style="B")
    else:
        pdf.set_font(family="Times", size=10)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(w=25, h=8, border=1, txt=str(prod_id))
    pdf.cell(w=70, h=8, border=1, txt=str(prod_name))
    pdf.cell(w=35, h=8, border=1, txt=str(amount))
    pdf.cell(w=30, h=8, border=1, txt=str(unit_price))
    pdf.cell(w=30, h=8, border=1, txt=str(total_price), ln=1)


def generate(invoices_folder_path, pdfs_folder_path, image_path,
             product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    This function converts invoice Excel files i,to PDF invoices.
    :param invoices_folder_path:
    :param pdfs_folder_path:
    :param image_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f"{invoices_folder_path}/*.xlsx")

    for filepath in filepaths:
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, date = filename.split("-")

        # Add invoice number and date
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, ln=1, txt=f"Invoice n° {invoice_nr}")

        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=50, h=8, ln=1, txt=f"Date: {date}")
        pdf.ln()

        # Read Excel file
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        # Add a header
        columns = df.columns
        columns = [column.replace("_", " ").title() for column in columns]
        add_line_pdf(columns[0], columns[1], columns[2], columns[3], columns[4], pdf, True)

        # Add rows to the table
        for index, row in df.iterrows():
            add_line_pdf(row[product_id], row[product_name], row[amount_purchased],
                         row[price_per_unit], row[total_price], pdf)

        # Add total amount row to table
        total_sum = df[total_price].sum()
        add_line_pdf("", "", "", "", total_sum, pdf)
        pdf.ln()

        # Add total sum sentence
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=30, h=8, txt=f'The total price is {total_sum}', ln=1)

        # Add company name and logo
        pdf.set_font(family="Times", size=14, style="B")
        pdf.cell(w=25, h=8, txt=f"PythonHow")
        pdf.image(image_path, w=10)

        if not os.path.exists(pdfs_folder_path):
            os.makedirs(pdfs_folder_path)
        pdf.output(f"{pdfs_folder_path}/{filename}.pdf")
