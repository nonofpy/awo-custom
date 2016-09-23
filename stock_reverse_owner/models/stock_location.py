# -*- encoding: utf-8 -*-

from openerp import models, fields, api


class stock_location(models.Model):
    _inherit = 'stock.location'
    
    is_repaired_location = fields.Boolean(
        string='Is a Repair Location ?',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
