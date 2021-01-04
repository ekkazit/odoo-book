from odoo import models, fields


class Product(models.Model):
    _inherit = 'product.template'
    gallery = fields.Binary("Gallery", attachment=True)
