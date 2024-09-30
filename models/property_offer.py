from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offers'

    @api.depends('partner_id','property_id')
    def _compute_name(self):
        for rec in self:
            if rec.partner_id and rec.property_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False
    
    name = fields.Char('Name', compute='_compute_name')
    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted', 'Accepted'), ('refused', 'Refused')
    ], string='Status')

    partner_id = fields.Many2one('res.partner', string='Customer')
    property_id = fields.Many2one('estate.property', string='Property')
    validity = fields.Integer('Validity', default=7)
    deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')


    @api.model
    def _set_creation_date(self):
        return fields.Date.today()
    
    creation_date = fields.Date('Create Date', default=_set_creation_date) # manggil fungsinya ga boleh jadi string

    # creation_date = fields.Date('Create Date')

    # kode ini ga bakal jalan kalo modulnya diinstall duluan baru dibikin kode ini jadi harus diinstall dulu,
    #makanya mending pakai python @api.constrains aja
    # _sql_constraints = [
    #     ('check_validity', 'check(validity > 0)', "Deadline tidak boleh kurang dari Create Date")
    # ]

    @api.depends('creation_date','validity')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:  
                rec.validity = False

    # @api.model_create_multi
    # def create(self, vals):
    #     for rec in vals:
    #         if not rec.get('creation_date'):
    #             rec['creation_date'] = fields.Date.today()
    #     return super(PropertyOffer, self).create(vals)

    # buat menjalankan autovacuum (liat di settings, scheduled actions), unlink() fungsinya buat ngehapus
    # @api.autovacuum
    # def _clean_offers(self):
    #     self.search([('status', '=', 'refused')]).unlink()

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError("Deadline tidak boleh kurang dari Create Date")
            

    def action_accept_offer(self):
        self._validate_accept_offer()
        if self.property_id:
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })
            # self.property_id.selling_price = self.price
        self.status = 'accepted'

    def action_decline_offer(self):
        self.status = 'refused'
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    def _validate_accept_offer(self):
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])
        if offer_ids:
            raise ValidationError('You already have an accepted offer.')