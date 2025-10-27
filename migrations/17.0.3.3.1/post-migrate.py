# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Post-migration script to populate computed fields"""

    # Update all operation lines to recompute parent fields
    cr.execute("""
        UPDATE work_order_operation_line wol
        SET execution_id = wel.execution_id,
            component_id = wel.component_id,
            production_id = wel.production_id
        FROM work_order_execution_line wel
        WHERE wol.execution_line_id = wel.id;
    """)

    cr.execute("""
        UPDATE work_order_operation_line wol
        SET project_id = we.project_id,
            product_id = we.product_id
        FROM work_order_execution we
        WHERE wol.execution_id = we.id;
    """)