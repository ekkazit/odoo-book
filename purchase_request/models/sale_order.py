from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    total_discount = fields.Float(string='Total Discount')

    @api.onchange('total_discount')
    def get_total_discount(self):
        price_after_discount = self.amount_untaxed - self.total_discount
        tax_rate = self.env.user.company_id.account_sale_tax_id.amount or 7
        self.amount_tax = price_after_discount * tax_rate / 100
        self.amount_total = price_after_discount + self.amount_tax
