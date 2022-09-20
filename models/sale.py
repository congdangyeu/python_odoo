from odoo import fields, api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"


    sale_description = fields.Char(string='Sale Description')