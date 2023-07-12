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
        "Type": "text",
        "ContentType": "Json",
        "Content": "eyJzbiI6MiwibHMiOnRydWUsImJnIjowLCJlZCI6MCwid3MiOlt7ImJnIjowLCJjdyI6W3sic2MiOjAsInciOiLvvJ8ifV19XX0="
    }
}
