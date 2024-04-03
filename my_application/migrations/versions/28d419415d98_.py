"""empty message

Revision ID: 28d419415d98
Revises: 
Create Date: 2023-11-01 21:05:19.858119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28d419415d98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('api_key', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_api_key'), 'user', ['api_key'], unique=False)
    op.create_table('tweet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=250), nullable=True),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('tweet_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_following',
    sa.Column('followers', sa.Integer(), nullable=False),
    sa.Column('following', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['followers'], ['user.id'], ),
    sa.ForeignKeyConstraint(['following'], ['user.id'], ),
    sa.PrimaryKeyConstraint('followers', 'following')
    )
    op.create_table('like',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tweet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'tweet_id')
    )
    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('media', sa.String(length=150), nullable=True),
    sa.Column('tweet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media')
    op.drop_table('like')
    op.drop_table('user_following')
    op.drop_table('tweet')
    op.drop_index(op.f('ix_user_api_key'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###