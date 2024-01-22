from datetime import date

from plone import api
from plone.dexterity.browser.view import DefaultView


class MemberInformationView(DefaultView):
    @property
    def member_information(self):
        users = api.user.get_users()
        infos = []
        for u in users:
            birthdate = u.getProperty("birthdate")
            if birthdate:
                birthday = date(date.today().year, birthdate.month, birthdate.day)
            else:
                birthday = None
            user_infos = {
                "lastname": u.getProperty("lastname"),
                "firstname": u.getProperty("firstname"),
                "birthday": birthday,
                "email": u.getProperty("email"),
                "phone": u.getProperty("phone"),
                "address": f'{u.getProperty("address_street")} - {u.getProperty("address_postalcode")} {u.getProperty("address_city")}',
            }
            infos.append(user_infos)

        return infos
