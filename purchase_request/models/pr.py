from odoo import models, fields, api, exceptions, _
from datetime import datetime
from .bahttext import bahttext


class PR(models.Model):
    _name = 'pr.pr'
    _rec_name = 'name'
    name = fields.Char('Name')
    date_pr = fields.Datetime('PR Date', required=True)
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True)
    project_id = fields.Many2one('pr.project', string='Project')
    approve_id = fields.Many2one('res.users', string='Approver')
    amount_untaxed = fields.Float(string='Untaxed Amount', store=True, readonly=True)
    amount_tax = fields.Float(string='Taxes', store=True, readonly=True)
    amount_total = fields.Float(string='Total', store=True, readonly=True)
    note = fields.Text('Note')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('revise', 'Revise'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
    ], string='Status', default='draft')
    pr_lines = fields.One2many('pr.pr_line', 'pr_id', string='PR Line')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    def get_baht_text(self):
        return bahttext(self.amount_total)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('pr.pr_num') or '-'
        vals['name'] = seq
        return super(PR, self).create(vals)

    @api.onchange('pr_lines')
    def get_total_amount(self):
        amount_untaxed = 0
        tax_rate = self.env.user.company_id.account_purchase_tax_id.amount or 7
        for r in self:
            for item in r.pr_lines:
                amount_untaxed += item.amount
        self.amount_untaxed = amount_untaxed
        self.amount_tax = (self.amount_untaxed * tax_rate) / 100
        self.amount_total = self.amount_untaxed + self.amount_tax

    def do_pr_draft(self):
        self.write({'state': 'draft'})

    def do_pr_approve(self):
        if not self.project_id.budget:
            raise exceptions.ValidationError(_('Project budget invalid amount!'))

        if self.amount_total > self.project_id.budget:
            raise exceptions.ValidationError(_('This PR is over budget!!'))

        self.create_rfq()
        self.write({'state': 'approve'})

    def create_rfq(self):
        rfq = self.env['purchase.order'].sudo().create({
            'partner_id': self.partner_id.id,
            'state': 'draft',
        })

        for line in self.pr_lines:
            rfq_line = self.env['purchase.order.line'].sudo().create({
                'order_id': rfq.id,
                'name': line.name,
                'product_id': line.product_id.id,
                'product_qty': line.qty,
                'product_uom': line.product_id.uom_id.id,
                'price_unit': line.price,
                'price_subtotal': line.amount,
                'date_planned': datetime.now(),
            })

    def do_pr_cancel(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pr.cancel.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_pr_id': self.id,
                'default_pr_name': self.name,
            }
        }

    def do_add_products(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.multi.wizard',
            'target': 'new',
            'type': 'ir.actions.act_window',
            'context': {
                'default_pr_id': self.id,
            }
        }


class PRLine(models.Model):
    _name = 'pr.pr_line'
    _rec_name = 'name'
    pr_id = fields.Many2one('pr.pr', string='PR')
    product_id = fields.Many2one('product.template', string='Product')
    name = fields.Char('Name')
    qty = fields.Float('Qty')
    price = fields.Float('Unit Price')
    amount = fields.Float('Amount', store=True, readonly=True)

    @api.onchange('product_id')
    def product_id_changed(self):
        self.name = '[{0}] {1}'.format(self.product_id.default_code, self.product_id.name)
        self.price = self.product_id.list_price
        if not self.qty:
            self.qty = 1
        self.amount = self.price * self.qty

    @api.onchange('price', 'qty')
    def price_changed(self):
        self.amount = self.price * self.qty
