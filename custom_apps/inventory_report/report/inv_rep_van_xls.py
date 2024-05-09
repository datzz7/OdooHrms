from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class PartnerXlsxAgeing(models.AbstractModel):
    _name = 'report.inventory_report.inv_rep_van_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        # for rec in data['form_data']:
        #     _logger.info('Test data: %s',rec)
        sheet = workbook.add_worksheet('Inventory Report - Van')
        font_format_higlight  = workbook.add_format({'bold':True,'font_size':'10px'})
        font_format_regular =  workbook.add_format({'font_size':'10px'})
       
        
        van_no =""
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for obj in partners:
            van_no = partners.location_id.complete_name
            
            break

        sheet.write(1,0, 'Jakkar Marketing Corporation',font_format_higlight)
        sheet.write(2,0,'Location: %s'%(van_no),font_format_higlight)
        sheet.write(4,0,'Date/Time Printed: %s'%(now),font_format_regular)
    

        sheet.write(7,0,'Internal Reference',font_format_higlight)
        sheet.write(7,1, 'Product',font_format_higlight)
        sheet.write(7,2,'Unit of Measure',font_format_higlight)
        sheet.write(7,3,'Available Quantity',font_format_higlight)
        sheet.write(7,4,'Onhand Qty',font_format_higlight)
        sheet.write(7,5,'route Price Unit',font_format_higlight)
        sheet.write(7,6,'Total Price Onhand Route Price',font_format_higlight)

        row = 7
        col = 0
        for obj in partners:
            row += 1
            sheet.write(row,0, obj.internal_ref,font_format_regular)
            sheet.write(row,1,obj.product_id.name,font_format_regular)
            sheet.write(row,2,obj.uom_name_val,font_format_regular)
            sheet.write(row,3,obj.available_quantity,font_format_regular)
            sheet.write(row,4,obj.onhand_qty_per_warehouse,font_format_regular)
            sheet.write(row,5,obj.route_price_uniit,font_format_regular)
            sheet.write(row,6,obj.total_price_onhand_route_price,font_format_regular)
        # for obj in partners:
        #     row += 1
        #     sheet.write(row,1, obj.internal_ref)
        #     sheet.write(row,2, obj.product_id)
        #     sheet.write(row,3,obj.uom_name_val)
        #     sheet.write(row,4,obj.available_quantity)
        #     sheet.write(row,5,obj.inventory_quantity)
        #     sheet.write(row,6,obj.route_price_unit)
        #     sheet.write(row,7,obj.total_price_onhand_route_price)
            
        


            

            

        # for raw in data['form_data']:
        #     sheet.write(row,col, 'Referecence',bold)
        #     sheet.write(row,col+1, 'Items',bold)
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)