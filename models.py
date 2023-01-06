from tortoise import Model, fields


class GayDay(Model):
    id = fields.IntField(pk=True, generated=True)  # айди события (затычка на похуй)
    peer_id = fields.IntField()
    day = fields.IntField()  # день
    mes = fields.IntField()  # месяц
    god = fields.IntField(null=True)  # год
    name = fields.CharField(max_length=8192)  # имя события
    sozd_id = fields.IntField()  # айди создателя/организатора (похуй если честно)


class DR(Model):
    "напомните нахуя я этим занимаюсь?"
    id = fields.IntField(pk=True, generated=True)
    user_id = fields.IntField()
    peer_id = fields.IntField()
    day = fields.IntField(null=True)
    mes = fields.IntField(null=True)
    god = fields.IntField(null=True)

    @classmethod
    async def get_or_new(cls, **kwargs) -> "DR":
        log, _ = await cls.get_or_create(**kwargs)
        return log


class ChatSettings(Model):
    peer_id = fields.IntField(pk=True)
    user = fields.BooleanField(default=False)

    @classmethod
    async def get_or_new(cls, **kwargs) -> "ChatSettings":
        log, _ = await cls.get_or_create(**kwargs)
        return log
