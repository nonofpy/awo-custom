# -*- encoding: utf-8 -*-

from openerp import models, api

class stock_quant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def move_quants_write(self, quants, move, location_dest_id, dest_package_id):
        res = super(stock_quant, self).move_quants_write(quants, move,
                                                         location_dest_id,
                                                         dest_package_id)
        picking = move.picking_id
        quant_ids = [q.id for q in quants]
        quant_ids = self.browse(quant_ids)
        owner_id = picking.owner_id and picking.owner_id.id or False
        #quant_ids.sudo().write({'owner_id': owner_id or False})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
