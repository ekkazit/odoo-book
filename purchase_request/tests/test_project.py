from odoo.tests import common


class TestProject(common.TransactionCase):
    def setUp(self):
        super(TestProject, self).setUp()
        self.project = self.env['pr.project'].create({
            'name': 'Test Project',
        })

    def test_project_name(self):
        self.assertEqual(self.project.name, 'Test Project')

    def test_department_name(self):
        self.assertTrue(self.project.department == 'ICT')

    def test_year_in_bc(self):
        self.assertEqual(self.project.year, 2563)
