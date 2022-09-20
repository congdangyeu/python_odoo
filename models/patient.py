from odoo import fields, api, models, _


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread"]
    _description = "Hospital Management"

    name = fields.Char(string="Name", required=True, track_visibility='always')
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    age = fields.Integer(string="Age", track_visibility='always')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', track_visibility='always', string='Gender')
    note = fields.Text(string="Description", track_visibility='always')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('done', 'Done'), ('cancel', 'Cancel')], string='State', default="draft",
                             track_visibility='always')
    responsible_id = fields.Many2one('res.partner', string="Responsible", required=True)
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')

    def _compute_appointment_count(self):
        print('self.id: ', self.id)
        appointment_count = self.env['hospital.appointment'].sudo().search_count([('patient_id', '=', self.id)])
        self.appointment_count = appointment_count

    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals.get('note'):
            vals['note'] = 'New patient'
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        return super(HospitalPatient, self).create(vals)
