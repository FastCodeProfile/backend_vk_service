from app.core.config import settings

from .api import API


async def url_to_kwargs(url: str) -> dict | None:
    api = API(settings.VK_TOKEN)
    if url.startswith("https://vk.com/") and url.count("wall"):
        url_args = url.split("wall")[1].split("_")
        owner_id = int(url_args[0])
        if owner_id > 0:
            if await api.is_closed(owner_id):
                return
        if len(url_args) == 2:
            type_ = "post"
            item_id = int(url_args[1])
        else:
            type_ = "comment"
            item_id = int(url_args[2].strip("r"))

        return dict(type_=type_, owner_id=owner_id, item_id=item_id)

    if url.startswith("https://vk.com/id"):
        user_id = int(url.replace("https://vk.com/id", ""))
        if await api.is_closed(user_id):
            return

        return dict(owner_id=user_id)

    if url.startswith("https://vk.com/"):
        screen_name = url.replace("https://vk.com/", "")
        result = await api.request("utils.resolveScreenName", screen_name=screen_name)
        if result:
            user_id = result.get("object_id")
            if await api.is_closed(user_id):
                return
            return dict(owner_id=result.get("object_id"))
