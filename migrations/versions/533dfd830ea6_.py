"""empty message

Revision ID: 533dfd830ea6
Revises: 919f7812e528
Create Date: 2025-02-20 02:12:23.306621

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '533dfd830ea6'
down_revision = '919f7812e528'
branch_labels = None
depends_on = None


def upgrade():
    # Create new sequence for labels if it doesn't exist
    op.execute("""
        DECLARE
            seq_exists NUMBER;
        BEGIN
            SELECT COUNT(*) INTO seq_exists 
            FROM user_sequences 
            WHERE sequence_name = 'NOTES_APP_LABELS_ID_SEQ';
            
            IF seq_exists = 0 THEN
                EXECUTE IMMEDIATE 'CREATE SEQUENCE notes_app_labels_id_seq START WITH 1 INCREMENT BY 1';
            END IF;
        END;
    """)
    
    # Modify existing tables - handle email column addition carefully
    with op.batch_alter_table('tbl_notes_app_users', schema=None) as batch_op:
        # First add email as nullable
        batch_op.add_column(sa.Column('email', sa.String(length=256), nullable=True))
        
    # Set a default value for existing rows (using username + default domain)
    op.execute("UPDATE tbl_notes_app_users SET email = username || '@default.com' WHERE email IS NULL")
    
    # Now make it not nullable
    with op.batch_alter_table('tbl_notes_app_users', schema=None) as batch_op:
        batch_op.alter_column('email', nullable=False)
        batch_op.create_unique_constraint('uq_email', ['email'])

    with op.batch_alter_table('tbl_notes_app_notes', schema=None) as batch_op:
        batch_op.alter_column('content', 
                             existing_type=sa.VARCHAR(length=256),
                             type_=sa.String(length=2048))
        batch_op.add_column(sa.Column('colour', sa.String(length=7), nullable=False, server_default='#ffffff'))
        batch_op.add_column(sa.Column('is_pinned', sa.String(length=1), nullable=True))

    # Create new tables
    op.create_table('TBL_NOTES_APP_LABELS',
        sa.Column('id', sa.Integer(), server_default=sa.text('notes_app_labels_id_seq.nextval'), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('is_system_label', sa.Boolean(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['tbl_notes_app_users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )



    op.create_table('TBL_NOTES_APP_NOTES_LABELS',
        sa.Column('note_id', sa.Integer(), nullable=False),
        sa.Column('label_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['label_id'], ['TBL_NOTES_APP_LABELS.id'], ),
        sa.ForeignKeyConstraint(['note_id'], ['tbl_notes_app_notes.id'], ),
        sa.PrimaryKeyConstraint('note_id', 'label_id')
    )



def downgrade():
    # Drop new tables
    op.drop_table('TBL_NOTES_APP_NOTES_LABELS')
    op.drop_table('TBL_NOTES_APP_LABELS')
    
    # Revert changes to existing tables
    with op.batch_alter_table('tbl_notes_app_notes', schema=None) as batch_op:
        batch_op.drop_column('is_pinned')
        batch_op.drop_column('colour')
        batch_op.alter_column('content',
                             existing_type=sa.String(length=2048),
                             type_=sa.VARCHAR(length=2048))

    with op.batch_alter_table('tbl_notes_app_users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_email', type_='unique')
        batch_op.drop_column('email')

    # Drop sequence if it exists
    op.execute("""
        DECLARE
            seq_exists NUMBER;
        BEGIN
            SELECT COUNT(*) INTO seq_exists 
            FROM user_sequences 
            WHERE sequence_name = 'NOTES_APP_LABELS_ID_SEQ';
            
            IF seq_exists = 1 THEN
                EXECUTE IMMEDIATE 'DROP SEQUENCE notes_app_labels_id_seq';
            END IF;
        END;
    """)
