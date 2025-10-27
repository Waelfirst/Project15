# -*- coding: utf-8 -*-

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Create default specification definitions and update operation line view"""

    _logger.info('Running post-init hook...')

    # Create default specifications
    _create_default_specifications(env)

    # Update work order operation line view with parent fields
    _update_operation_line_view(env)

    _logger.info('Post-init hook completed successfully')


def _create_default_specifications(env):
    """Create default specification definitions after module installation"""

    _logger.info('Creating default specification definitions...')

    SpecDef = env['component.specification.definition']

    # Check if specifications already exist
    existing = SpecDef.search([('code', 'in', [
        'MATERIAL', 'DIMENSIONS', 'COLOR', 'FINISH', 'THICKNESS',
        'WEIGHT_CAP', 'QUALITY', 'CERT', 'SUPPLIER', 'NOTES'
    ])])

    if existing:
        _logger.info('Default specifications already exist, skipping creation')
        return

    # Create default specifications
    specifications = [
        {'name': 'Material', 'code': 'MATERIAL', 'sequence': 10},
        {'name': 'Dimensions', 'code': 'DIMENSIONS', 'sequence': 20},
        {'name': 'Color', 'code': 'COLOR', 'sequence': 30},
        {'name': 'Finish', 'code': 'FINISH', 'sequence': 40},
        {'name': 'Thickness', 'code': 'THICKNESS', 'sequence': 50},
        {'name': 'Weight Capacity', 'code': 'WEIGHT_CAP', 'sequence': 60},
        {'name': 'Quality Grade', 'code': 'QUALITY', 'sequence': 70},
        {'name': 'Certification', 'code': 'CERT', 'sequence': 80},
        {'name': 'Preferred Supplier', 'code': 'SUPPLIER', 'sequence': 90},
        {'name': 'Special Notes', 'code': 'NOTES', 'sequence': 100},
    ]

    for spec_data in specifications:
        try:
            SpecDef.create(spec_data)
            _logger.info('Created specification: %s', spec_data['name'])
        except Exception as e:
            _logger.error('Error creating specification %s: %s', spec_data['name'], e)

    _logger.info('Default specifications created successfully')


def _update_operation_line_view(env):
    """Update work order operation line tree view to include parent fields"""

    _logger.info('Updating work order operation line view...')

    try:
        # Find the view
        view = env.ref('project_product_costing.view_work_order_operation_line_tree', raise_if_not_found=False)

        if not view:
            _logger.warning('View not found, skipping update')
            return

        # Update the arch with parent fields
        new_arch = """<?xml version="1.0"?>
<tree string="Work Order Operations"
      decoration-success="state=='done'"
      decoration-info="state=='progress'"
      decoration-warning="state in ('ready','waiting')"
      decoration-muted="state=='cancel'"
      create="false" delete="false">
    <field name="sequence" widget="handle"/>
    <field name="selected" widget="boolean_toggle"/>
    <field name="project_id" optional="show"/>
    <field name="product_id" optional="show"/>
    <field name="production_id" optional="show"/>
    <field name="component_id" optional="show"/>
    <field name="additional_code" optional="show" widget="text"/>
    <field name="specification_text" optional="show" widget="text"/>
    <field name="name"/>
    <field name="workcenter_id"/>
    <field name="state" widget="badge"/>
    <field name="qty_production" optional="hide"/>
    <field name="qty_produced" optional="hide"/>
    <field name="progress_percentage" widget="progressbar"/>
    <field name="duration_expected"/>
    <field name="actual_duration" optional="show"/>
    <field name="workers_assigned" optional="show"/>
    <field name="machines_assigned" optional="show"/>
    <field name="date_start" optional="hide"/>
    <button name="action_start" type="object"
            icon="fa-play" string="Start"
            invisible="state not in ('pending','ready','waiting')"/>
    <button name="action_finish" type="object"
            icon="fa-check" string="Finish"
            invisible="state not in ('progress','to_close')"/>
    <button name="action_open_workorder" type="object"
            icon="fa-external-link" string="Open"/>
</tree>"""

        view.write({'arch': new_arch})
        _logger.info('View updated successfully with parent fields')

    except Exception as e:
        _logger.error('Error updating view: %s', e)