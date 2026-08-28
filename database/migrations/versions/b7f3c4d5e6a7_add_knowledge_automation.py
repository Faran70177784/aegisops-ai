"""add knowledge and automation tables"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
revision: str = "b7f3c4d5e6a7"
down_revision: Union[str, Sequence[str], None] = "0906a1e85550"
branch_labels = None
depends_on = None
def upgrade() -> None:
    op.create_table("knowledge_documents", sa.Column("id",sa.Integer(),primary_key=True),sa.Column("title",sa.String(255),nullable=False),sa.Column("source",sa.String(500),nullable=False),sa.Column("content",sa.Text(),nullable=False),sa.Column("content_hash",sa.String(64),nullable=False),sa.Column("chunk_count",sa.Integer(),nullable=False,server_default="0"),sa.Column("metadata_json",sa.JSON(),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_knowledge_documents_id","knowledge_documents",["id"])
    op.create_index("ix_knowledge_documents_title","knowledge_documents",["title"])
    op.create_index("ix_knowledge_documents_content_hash","knowledge_documents",["content_hash"],unique=True)
    op.create_table("knowledge_chunks",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("document_id",sa.Integer(),nullable=False),sa.Column("chunk_index",sa.Integer(),nullable=False),sa.Column("content",sa.Text(),nullable=False),sa.Column("metadata_json",sa.JSON(),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_knowledge_chunks_id","knowledge_chunks",["id"]); op.create_index("ix_knowledge_chunks_document_id","knowledge_chunks",["document_id"])
    op.create_table("automation_jobs",sa.Column("id",sa.Integer(),primary_key=True),sa.Column("name",sa.String(150),nullable=False),sa.Column("job_type",sa.String(80),nullable=False),sa.Column("status",sa.String(30),nullable=False,server_default="queued"),sa.Column("payload_json",sa.JSON(),nullable=True),sa.Column("result_json",sa.JSON(),nullable=True),sa.Column("error",sa.Text(),nullable=True),sa.Column("created_at",sa.DateTime(timezone=True),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_automation_jobs_id","automation_jobs",["id"]); op.create_index("ix_automation_jobs_status","automation_jobs",["status"])
def downgrade() -> None:
    op.drop_index("ix_automation_jobs_status",table_name="automation_jobs"); op.drop_index("ix_automation_jobs_id",table_name="automation_jobs"); op.drop_table("automation_jobs")
    op.drop_index("ix_knowledge_chunks_document_id",table_name="knowledge_chunks"); op.drop_index("ix_knowledge_chunks_id",table_name="knowledge_chunks"); op.drop_table("knowledge_chunks")
    op.drop_index("ix_knowledge_documents_content_hash",table_name="knowledge_documents"); op.drop_index("ix_knowledge_documents_title",table_name="knowledge_documents"); op.drop_index("ix_knowledge_documents_id",table_name="knowledge_documents"); op.drop_table("knowledge_documents")
