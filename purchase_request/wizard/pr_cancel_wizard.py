from odoo import models, fields


class PRCancelWizard(models.TransientModel):
    _name = 'pr.cancel.wizard'
    pr_id = fields.Integer('PR ID')
    pr_name = fields.Char('PR Name')

    def do_confirm_cancel(self):
        self.env['pr.pr'].browse([self.pr_id]).sudo().write({
            'state': 'cancel',
        })
