from holehe.core import *
from holehe.localuseragent import *


async def smule(email, client, out):

    name = "smule"
    headers = {
        'User-Agent': random.choice(ua["browsers"]["firefox"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.smule.com',
        'Connection': 'keep-alive',
        'TE': 'Trailers',
    }

    r = await client.get('https://www.smule.com/user/check_email', headers=headers)
    try:
        csrf_token = (
            r.text.split(
                'authenticity_token" name="csrf-param" />\n<meta content="')
            [1]).split('"')[0]
    except BaseException:
        out.append({"name": name,
                    "rateLimit": True,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
        return None

    headers['X-CSRF-Token'] = str(csrf_token)

    data = {
        'email': str(email)
    }

    response = await client.post('https://www.smule.com/user/check_email', headers=headers, data=data)
    if str(response.json()['email']) == 'True':
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
