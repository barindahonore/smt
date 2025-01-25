# admin.py
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from authentication.models import *
from authentication.admin import *

from citizen.models import *
from core.models import Stories




from import_export import resources
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


class MyAdminSite(admin.AdminSite):
    site_header = _("Smart Mudugudu Admin")
    site_title = _("Smart Mudugudu")
    index_title = _("Welcome to My Smart Mudugudu")

admin_site = MyAdminSite(name='myadmin')

admin_site.register(CustomUser, MyAdminUser)


class DisplayCitizens(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'birth_date', 'gender', 'is_employed']
    
    # resource_class = FertiRequestsResource
    # date_hierarchy = 'created'
    list_filter = ['is_employed', 'gender']

    # Remove Dashes on Select Action Dropdown
    def get_action_choices(self, request):
        default_choices = [("", "Select action")]
        return super(DisplayCitizens, self).get_action_choices(request, default_choices)

    def Print_Report(self, request, queryset):
        # sector = request.GET.get('user__sector') if request.GET.get('user__sector') is not None else ""
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        day_ = str(datetime.now().day)
        pdf_export_title = "List of Citizens as on "+ day_+", "+month+", "+year
        queryset_for_export = queryset
        return export_statistics(self, request, queryset_for_export, pdf_export_title)
    
    actions = ['Print_Report']


def export_statistics(self, request, queryset=None, title=None):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ReportExport.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    p = canvas.Canvas(response, pagesize=letter)
    elements = []

    logo_path = os.getcwd() + '\static\images\\logo.png'
    image = Image(logo_path, width=200, height=50) # You can add hAlign='LEFT' attribute to position image
    elements.append(image)
    header = 'SMART MUDUGUDU'
    # location = 'Rubona, Huye District'
    email = 'info@mudugudu.gov.rw'
    pobox = 'P.O Box 5016'
    elements.append(Paragraph(header))
    # elements.append(Paragraph(location))
    elements.append(Paragraph(email))
    elements.append(Paragraph(pobox))
    title_margin_top = 10
    
    # Add title to the PDF (use the provided title or a default title)
    title = title if title is not None else "My Report"
    title_style = getSampleStyleSheet()['Title']
    title_style.spaceAfter = title_margin_top  # Add custom margin-top to the title
    elements.append(Paragraph(title, title_style))



    data = [['No','First Name', 'Last Name', 'Gender', 'Date',]]  # Table header
    counter = 1
    for obj in queryset:
        data.append([counter, obj.first_name, obj.last_name, obj.gender, obj.is_employed])
        counter+=1

    data.append([""])
    
    num_columns = len(data[0])
    page_width, page_height = letter
    # Calculate the total padding for left and right (you can adjust the padding value)
    padding = 50
    total_padding = padding * 2

    # Calculate the width of each column based on the page width, number of columns, and padding
    column_width = (page_width - total_padding) / num_columns

    # Set the width of each column in the table with padding
    col_widths = [column_width] * num_columns

    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # ('GRID', (0, 0), (-1, -1), 1, 'black'),
    ])
    table.setStyle(style)
    elements.append(table)

    # Get the user data (first name, last name, username) to be printed in the footer
    user_data = (request.user.first_name.strip(), request.user.last_name.strip(), request.user.username)

    # Build the document and add the footer with the user data
    doc.build(elements, onFirstPage=lambda canvas, doc: add_footer(canvas, doc, user_data),
              onLaterPages=lambda canvas, doc: add_footer(canvas, doc, user_data))

    return response


class DisplayAbakandidas(admin.ModelAdmin):
    list_display = ['citizen', 'post', 'votes']
    
    # resource_class = FertiRequestsResource
    # date_hierarchy = 'created'
    list_filter = ['post__post']

    # Remove Dashes on Select Action Dropdown
    def get_action_choices(self, request):
        default_choices = [("", "Select action")]
        return super(DisplayAbakandidas, self).get_action_choices(request, default_choices)

    def Print_Report(self, request, queryset):
        # sector = request.GET.get('user__sector') if request.GET.get('user__sector') is not None else ""
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        day_ = str(datetime.now().day)
        pdf_export_title = "List of Votes as on "+ day_+", "+month+", "+year
        queryset_for_export = queryset
        return export_abakandidas(self, request, queryset_for_export, pdf_export_title)
    
    actions = ['Print_Report']


def export_abakandidas(self, request, queryset=None, title=None):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ReportExport.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    p = canvas.Canvas(response, pagesize=letter)
    elements = []

    logo_path = os.getcwd() + '\static\images\\logo.png'
    image = Image(logo_path, width=200, height=50) # You can add hAlign='LEFT' attribute to position image
    elements.append(image)
    header = 'SMART MUDUGUDU'
    # location = 'Rubona, Huye District'
    email = 'info@mudugudu.gov.rw'
    pobox = 'P.O Box 5016'
    elements.append(Paragraph(header))
    # elements.append(Paragraph(location))
    elements.append(Paragraph(email))
    elements.append(Paragraph(pobox))
    title_margin_top = 10
    
    # Add title to the PDF (use the provided title or a default title)
    title = title if title is not None else "My Report"
    title_style = getSampleStyleSheet()['Title']
    title_style.spaceAfter = title_margin_top  # Add custom margin-top to the title
    elements.append(Paragraph(title, title_style))



    data = [['No','First Name', 'Last Name', 'Post', 'Votes',]]  # Table header
    counter = 1
    for obj in queryset:
        data.append([counter, obj.citizen.first_name, obj.citizen.last_name, obj.post.post, obj.votes])
        counter+=1

    data.append([""])
    
    num_columns = len(data[0])
    page_width, page_height = letter
    # Calculate the total padding for left and right (you can adjust the padding value)
    padding = 50
    total_padding = padding * 2

    # Calculate the width of each column based on the page width, number of columns, and padding
    column_width = (page_width - total_padding) / num_columns

    # Set the width of each column in the table with padding
    col_widths = [column_width] * num_columns

    table = Table(data, colWidths=col_widths)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), 'lightgrey'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # ('GRID', (0, 0), (-1, -1), 1, 'black'),
    ])
    table.setStyle(style)
    elements.append(table)

    # Get the user data (first name, last name, username) to be printed in the footer
    user_data = (request.user.first_name.strip(), request.user.last_name.strip(), request.user.username)

    # Build the document and add the footer with the user data
    doc.build(elements, onFirstPage=lambda canvas, doc: add_footer(canvas, doc, user_data),
              onLaterPages=lambda canvas, doc: add_footer(canvas, doc, user_data))

    return response

def add_footer(canvas, doc, user_data):
    first_name, last_name, username = user_data

    if not first_name.strip() and not last_name.strip():
        footer_text = f"Printed by {username} on "+str(datetime.now())
    else:
        footer_text = f"Printed by {first_name} {last_name} on "+str(datetime.now())

    # Reduce font size
    canvas.saveState()
    canvas.setFont("Helvetica", 8)

    # Get the width and height of the footer text
    footer_paragraph = Paragraph(footer_text, getSampleStyleSheet()['Normal'])
    # footer_width, footer_height = footer_paragraph.wrap(doc.width, doc.bottomMargin)

    # Calculate the X coordinate to align the footer at the left margin
    footer_x = doc.leftMargin + 380

    # Calculate the Y coordinate to align the footer at the bottom of the page
    footer_y = doc.bottomMargin + 170

    # Draw the footer at the left margin and bottom of the page
    canvas.drawString(footer_x, footer_y, footer_text)
    canvas.restoreState()

export_statistics.short_description = "Export to PDF"



admin_site.register(Isibo)
admin_site.register(Citizens, DisplayCitizens)
admin_site.register(Messages)
admin_site.register(Family)
admin_site.register(Events)
admin_site.register(Files)
admin_site.register(Stories)
admin_site.register(Post)
admin_site.register(Abakandida, DisplayAbakandidas)
admin_site.register(Votes)
admin_site.register(Kwimuka)