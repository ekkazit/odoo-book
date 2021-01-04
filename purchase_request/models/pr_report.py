from odoo import models, api


class ReportPRForm(models.AbstractModel):
    _name = 'report.purchase_request.report_pr_form'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['pr.pr'].browse(docids)
        my_text = 'Hello QWeb'
        my_product = self.env['product.template'].browse([1])
        return {
            'doc_ids': docs.ids,
            'doc_model': 'pr.pr',
            'data': data,
            'docs': docs,
            'my_text': my_text,
            'my_product': my_product,
        }
