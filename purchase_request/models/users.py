from odoo import models, fields, api, exceptions


class MyUser(models.Model):
    _inherit = 'res.users'

    @api.model
    def name_get(self):
        result = []
        for record in self:
            name = '[ID=' + str(record.id) + ']' + ' ' + record.name
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            args += ['|', ('name', operator, '%' + name + '%'), ('email', operator, '%' + name + '%')]
        return super(MyUser, self).name_search(name=name, args=args, operator=operator, limit=limit)
