# Mysqllib
Simple mysql database

## Connect
```text
connect(
        user: str,
        password: str,
        database: str,
        host: str='127.0.0.1',
        port: int=3306
)
```

## Fetch one
```text
fetchone(query, args=None) -> Optional[dict]
```

## Fetch all
```text
fetchall(query, args=None) -> Optional[list]:
```

## Execute
```text
execute(query, args=None) -> bool:
```