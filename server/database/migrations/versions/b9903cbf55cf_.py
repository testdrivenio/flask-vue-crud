"""empty message

Revision ID: b9903cbf55cf
Revises: 
Create Date: 2022-06-04 12:16:43.633135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9903cbf55cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sqlite_sequence')
    op.drop_table('playlist_items')
    op.drop_index('playlists_id_uindex', table_name='items')
    op.drop_table('items')
    op.drop_index('playlist_names_id_uindex', table_name='playlist_names')
    op.drop_index('playlist_names_name_uindex', table_name='playlist_names')
    op.create_unique_constraint(None, 'playlist_names', ['name'])
    op.create_foreign_key(None, 'playlist_names', 'content', ['name'], ['name'])
    op.drop_index('tags_id_uindex', table_name='tags')
    op.drop_index('tags_name_uindex', table_name='tags')
    op.create_unique_constraint(None, 'tags', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tags', type_='unique')
    op.create_index('tags_name_uindex', 'tags', ['name'], unique=1)
    op.create_index('tags_id_uindex', 'tags', ['id'], unique=1)
    op.drop_constraint(None, 'playlist_names', type_='foreignkey')
    op.drop_constraint(None, 'playlist_names', type_='unique')
    op.create_index('playlist_names_name_uindex', 'playlist_names', ['name'], unique=1)
    op.create_index('playlist_names_id_uindex', 'playlist_names', ['id'], unique=1)
    op.create_table('items',
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('duration', sa.INTEGER(), nullable=True),
    sa.Column('type', sa.VARCHAR(length=8), nullable=False),
    sa.Column('priority', sa.INTEGER(), nullable=True),
    sa.Column('path', sa.VARCHAR(length=8), nullable=False),
    sa.Column('played', sa.INTEGER(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('playlists_id_uindex', 'items', ['id'], unique=1)
    op.create_table('playlist_items',
    sa.Column('playlist_id', sa.INTEGER(), nullable=False),
    sa.Column('item_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['playlist_id'], ['playlist_names.id'], ),
    sa.PrimaryKeyConstraint('playlist_id', 'item_id')
    )
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
