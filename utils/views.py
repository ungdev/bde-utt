from showcase.models import Partner
import json


def common_data():

    partners_qs = Partner.objects.filter(enable=True).order_by("order")
    partners_list = [
        {
            "name": p.name,
            "description": p.description,
            "icon_url": p.icon_url,
            "url": p.url,
        }
        for p in partners_qs
    ]

    return {
        "partners_qs": partners_qs,
        "partners_json": json.dumps(partners_list),
    }
