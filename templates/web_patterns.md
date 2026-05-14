# Web Patterns — Snippet Templates

## FastAPI endpoint chuẩn
```python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

router = APIRouter(prefix="/items", tags=["items"])

class ItemCreate(BaseModel):
    name: str
    price: float

@router.post("/", status_code=201)
async def create_item(payload: ItemCreate, db=Depends(get_db)):
    item = await db.items.create(payload.model_dump())
    return item

@router.get("/{item_id}")
async def get_item(item_id: int, db=Depends(get_db)):
    item = await db.items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
```

## React custom hook
```typescript
import { useState, useEffect } from "react";

function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    fetch(url, { signal: controller.signal })
      .then((r) => r.json())
      .then(setData)
      .catch((e) => { if (e.name !== "AbortError") setError(e); })
      .finally(() => setLoading(false));
    return () => controller.abort();
  }, [url]);

  return { data, loading, error };
}
```

## CSS utility — truncate text
```css
.truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```
