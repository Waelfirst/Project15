# -*- coding: utf-8 -*-

def migrate(cr, version):
    """Pre-migration to ensure all fields exist"""

    # Check if table exists
    cr.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'work_order_operation_line'
        );
    """)

    if not cr.fetchone()[0]:
        return  # Table doesn't exist yet, skip

    # Add all fields if they don't exist
    fields_to_add = [
        ('execution_line_id', 'INTEGER'),
        ('execution_id', 'INTEGER'),
        ('project_id', 'INTEGER'),
        ('product_id', 'INTEGER'),
        ('component_id', 'INTEGER'),
        ('production_id', 'INTEGER'),
        ('workorder_id', 'INTEGER'),
        ('workcenter_id', 'INTEGER'),
        ('operation_id', 'INTEGER'),
    ]

    for field_name, field_type in fields_to_add:
        cr.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='work_order_operation_line' 
            AND column_name=%s;
        """, (field_name,))

        if not cr.fetchone():
            cr.execute(f"""
                ALTER TABLE work_order_operation_line 
                ADD COLUMN {field_name} {field_type};
            """)

    # Create indexes
    indexes = [
        ('work_order_operation_line_execution_id_index', 'execution_id'),
        ('work_order_operation_line_project_id_index', 'project_id'),
        ('work_order_operation_line_production_id_index', 'production_id'),
    ]

    for index_name, column_name in indexes:
        cr.execute(f"""
            CREATE INDEX IF NOT EXISTS {index_name} 
            ON work_order_operation_line({column_name});
        """)