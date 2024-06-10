from datetime import date, datetime
from decimal import Decimal

from fastapi.responses import JSONResponse
import simplejson
from typing import Any


class SimpleJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert (simplejson is not None), "simplejson must be installed to use SimpleJSONResponse"
        if isinstance(content, int) or isinstance(content, float) or isinstance(content, Decimal):
            return simplejson.dumps(content,
                                    ensure_ascii=False,
                                    allow_nan=False,
                                    indent=None,
                                    separators=(",", ":"),
                                    use_decimal=True
                                    ).encode("utf-8")

        if isinstance(content, date):
            content = "%02d-%02d-%04d" % (content.day, content.month, content.year)
            simplejson.dumps(content,
                             ensure_ascii=False,
                             allow_nan=False,
                             indent=None,
                             separators=(",", ":"),
                             use_decimal=True
                             ).encode("utf-8")

        if isinstance(content, datetime):
            content = "%02d-%02d-%04d %02d:%02d" % (content.day, content.month, content.year, content.hour, content.minute)
            simplejson.dumps(content,
                             ensure_ascii=False,
                             allow_nan=False,
                             indent=None,
                             separators=(",", ":"),
                             use_decimal=True
                             ).encode("utf-8")
        try:
            for c in content:
                try:
                    for k in c.keys():
                        if isinstance(c[k], date):
                            c[k] = "%02d-%02d-%04d" % (c[k].day, c[k].month, c[k].year)
                        elif isinstance(c[k], datetime):
                            c[k] = "%02d-%02d-%04d %02d:%02d" % (c[k].day, c[k].month, c[k].year, c[k].hour, c[k].minute)
                        # elif isinstance(c[k], Decimal):
                        #     c[k] = float(c[k])
                except:
                    c = c
        except:
            content = content
        return simplejson.dumps(content,
                                ensure_ascii=False,
                                allow_nan=False,
                                indent=None,
                                separators=(",", ":"),
                                use_decimal=True
                                ).encode("utf-8")
