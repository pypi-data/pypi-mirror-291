import msgspec


class JsonHelper:

    @staticmethod
    def decode(data, raise_error=False):
        try:
            return msgspec.json.decode(data)
        except Exception as error:
            if raise_error:
                raise error
            return data

    @staticmethod
    def encode(data, raise_error=False):
        try:
            encoded = msgspec.json.encode(data)
            if isinstance(encoded, (bytes, bytearray)):
                return encoded.decode("utf-8")
            return encoded # pragma: no cover
        except Exception as error:
            if raise_error:
                raise error
            return data
