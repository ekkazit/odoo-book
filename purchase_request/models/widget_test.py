from odoo import models, fields, api


class WidgetTest(models.Model):
    _name = 'widget.test'
    _inherit = 'mail.thread'
    product_list = fields.Many2many('product.template', 'product_list')
    my_email = fields.Char('Email')
    my_phone = fields.Char('Phone')
    my_url = fields.Char('URL')
    my_money = fields.Float('Money')
    my_rating = fields.Selection([('0', 'Very Low'), ('1', 'Low'), ('2', 'Normal'), ('3', 'High'), ('4', 'Very High')], string='Rating')
    my_gender = fields.Selection([('1', 'Male'), ('2', 'Female'), ('3', 'N/A')], string='Gender')
    my_date = fields.Datetime(string='My Date')
    my_time = fields.Char(string='My Time')
    my_html = fields.Text('HTML')
    is_published = fields.Boolean('Is Publish')
    is_active = fields.Boolean('Is Active')
    product_count = fields.Integer('Product Count', default=1250)
    product_price = fields.Float('Product Price', default=158980)
    status = fields.Selection([('dft', 'Draft'), ('appr', 'Approve'), ('comp', 'Completed')], default="dft", string='Status')
    user_signature = fields.Binary(string='Signature')
    user_image = fields.Binary(string='Image')
    user_attachments = fields.Many2many('ir.attachment')
    products1 = fields.Many2many('product.template', 'product1')
    products2 = fields.Many2many('product.template', 'product2')
    progress_percent = fields.Integer('Progress Bar', default=65)
    gauge_percent = fields.Integer('Gauge Percent', default=25)
    pie_percent = fields.Integer('Pie Percent', default=80)
