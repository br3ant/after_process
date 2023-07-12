from pydantic import BaseModel


class MsgContent(BaseModel):
    Type: str
    ContentType: str
    Content: str


class MessageBody(BaseModel):
    Msg: MsgContent


data = {
    "UserId": "123456",
    "Msg": {
        "Type": "Type",
        "ContentType": "json",
        "Content": "Base64"
    }
}
