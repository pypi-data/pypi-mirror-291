# PrettyId

Pretty cool IDs for your APIs.

```bash
poetry add prettyid
```

## Synopsis

Generate prefixed IDs, like Stripe does:

```python
>>> from pretty_id import PrettyId
>>> pid = PrettyId.random("task")
PrettyId("task_068n34jrjdth1fqr2nm9a0sh50")
>>> pid.type, pid.id
('task', '068n34jrjdth1fqr2nm9a0sh50')
>>> pid.bytes
b'...'
```

Backwards compatible with UUID:

```python
>>> pid = PrettyId.from_uuid("1d4e2ea4-c1ab-4a98-8eeb-898051ef0f71", type="task")
PrettyId("task_3n72x961nd59h3qbh6053vrfe4")
>>> pid.uuid
UUID('1d4e2ea4-c1ab-4a98-8eeb-898051ef0f71')
```

<!-- Works with Pydantic and FastAPI (TODO):

```python
@app.route("/tasks/{id}")
def get_task_by_id(id: FriendlyId):
    if id.type != "task":
        raise HTTPException(status_code=400, detail="ID should start with 'task_'")

    return {
        "id": id,
        "title": "TODO",
    }
``` -->

<!-- Works with SQLAlchemy:

```python
from pretty_id.ext.sqlalchemy import PrettyIdType

class TaskModel(Base):
    id: Mapped[PrettyId] = Column(PrettyIdType(type="type"))
    title: Mapped[str]

# Pass PrettyId instance or just string
select(TaskModel).filter(
    TaskModel.id == "task_068n34jrjdth1fqr2nm9a0sh50"
)
``` -->


## Design

Generated IDs use UUIDv7 underneath:

```python
>>> u = UUID(bytes=pid.bytes)
UUID('01917192-7b9b-7b10-bf5b-15ec95039128')
>>> u.version
7
```

This means they inherit some useful properties:

- **Natural Sorting:** UUIDv7 values are time-sortable, which means you can sort them in increasing order based on when they were generated. Databases often require additional timestamp columns to sort records based on creation time. With PrettyId, you can achieve this sorting using the ID itself, eliminating the need for extra columns.

- **Optimized Indexing:** Since UUIDv7 is time-sortable, database indexing mechanisms can better optimize the storage and retrieval processes, leading to faster query times especially for time-based queries.

- **Concurrency and Distribution:** In distributed systems, generating unique, sequential IDs can be a challenge. UUIDv7 can be generated concurrently across multiple nodes without the risk of collisions, making it suitable for distributed architectures.

IDs are encoded as lowercase Base32 using [Douglas Crockford’s alphabet][crockford]. This makes them compact, readable, and case-insensitive.

[crockford]: https://www.crockford.com/base32.html

In database, IDs are stored without prefix using a native UUID type or `BINARY(16)`. (We assume that the prefix can be determined from the table name.)
