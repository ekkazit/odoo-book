from odoo import models, fields, api


class ProductWizard(models.TransientModel):
    _name = 'product.multi.wizard'
    pr_id = fields.Integer('PR ID')
    product_ids = fields.Many2many('product.template', string='Products')

    def do_confirm_add_product(self):
        pr = self.env['pr.pr'].browse([self.pr_id])
        for p in self.product_ids:
            pr.pr_lines.sudo().create({
                'pr_id': pr.id,
                'product_id': p.id,
                'qty': 1,
                'price': p.list_price,
                'amount': p.list_price,
            })
