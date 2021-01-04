from datetime import datetime
from odoo import models, fields, api, exceptions
import urllib.request
import json
import logging

_logger = logging.getLogger(__name__)


class Project(models.Model):
    _name = 'pr.project'
    _rec_name = 'name'
    _order = 'name'
    image = fields.Image('Image', attatchment=True)
    name = fields.Char('Name', required=True)
    budget = fields.Float('Budget')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    type = fields.Selection([('N', 'Normal'), ('U', 'Urgent')], string='Type', default='N')
    department = fields.Char('Department', default='ICT')
    year = fields.Char('Year', default=lambda x: x.get_bc_year())
    duration_days = fields.Integer('Duration Days', default=0)
    responsible_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    def get_bc_year(self):
        return datetime.now().year + 543

    def get_exchange_rate(self):
        _logger.info('** Start job **')
        try:
            response = urllib.request.urlopen('https://api.exchangeratesapi.io/latest?base=THB')
            byte_data = response.read()
            json_data = json.loads(byte_data)
            rates = json_data.get('rates')
            _logger.debug('THB={}'.format(rates.get('THB')))
            _logger.debug('USD={}'.format(rates.get('USD')))
            _logger.debug('EUR={}'.format(rates.get('EUR')))
            _logger.debug('JPY={}'.format(rates.get('JPY')))
        except Exception as err:
            _logger.error('Error! execute job', err)
        _logger.info('** Finish job **')
