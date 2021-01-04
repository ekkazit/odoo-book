from odoo import models, fields, api


class BaseClass(models.Model):
    _name = 'mytest.base_model'
    name = fields.Char('Name')


class BaseType1(models.Model):
    _name = 'mytest.base_model'
    _inherit = 'mytest.base_model'
    field1 = fields.Char('Field1')


class BaseType2(models.Model):
    _name = 'mytest.base_model2'
    _inherit = 'mytest.base_model'
    field2 = fields.Char('Field2')


class BaseType3(models.Model):
    _name = 'mytest.base_model3'
    _inherits = {
        'mytest.base_model': 'model_id',
        'product.category': 'category_id',
    }
    field3 = fields.Char('Field3')
    category_id = fields.Many2one('product.category', string='Category Id')
