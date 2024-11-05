from math import ceil

from fastapi import HTTPException, Request, Response, status


async def service_name_indentifier(request:Request) -> str|None:
    service = request.headers.get("Service-Name")
    return service


async def custom_callback(request:Request,response:Response,pexpire:int):
    expire = ceil(pexpire/1000)
    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail=f"Too many requests. Retry after {expire} seconds.",
        headers={"Retry-After":str(expire)}
    )
    