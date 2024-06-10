from typing import List
import firebase_admin
from firebase_admin import credentials, messaging, auth

cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "mas50-89e2a",
        "private_key_id": "2ecef9cfa0cbaf5ef205491dc68fc6c92866cf7a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC6rsBqwXBodruG\nhILZdpjfqP2xr51FV4tF/UTI1xDiMHqVwsxDhpNqubp2RJtRkgYx/SA7LTMD5GxR\nhQORWTtmK70eWp4NL9G0tha6SLEMzDKF4wGPhmvTbz+sebR6gVhU9DKCbJWDU20r\nAVe3kLUE8V27GpJRMw0S9QMsGhGKpOOu4bxfivafxD9xoaSgE4FeRAekqJeHC+yc\ntvKRANG9XeaV/8CmvVBafp0jc1T5WLLicUTMmD4dGiGErBIYvoUGga900d1MhJOW\n/Vu50JKCzynmmGhRlPsPexErMlWC3iPQWxiHhIblYDj4CCrQlERqgt9c2+WF+RWw\nui5dan2dAgMBAAECggEAWl8qiwOl1QxVb6NKbNe63dtDJPds3RqqM3GOEOP8KmNp\nlII+vBmz16CdoY9I2U4lbaGqLruMzL+RqE0KExztYmKeJMmdZajWjfLwQbHa8+UO\nOD5SjRZ3sF1Up7wrIHrpNgcZRIYoQvDqEj2OJzEIUKI/y8nrNx/NnnW52WmtQD4J\n0c9sr8AB5LKZyzogJSD/IAvr+aycr5xAFjpqFgwUgLmg4pu7DKqe74XkhlBP24V3\nXxT7WzenmB6cbs6VyEWUpOeKvUZcjpM4lVlCgzrQof0ZCpIMrUSnz3cmepDlkNSZ\nohnvccp6wLkbPKDggE4s5SXwVA02WaNGDA5GD6YfSQKBgQDwjgETPod+PaNlda6S\nodgMsiQ/534dfiOOpHFYDnd4L9XZiV6OBdeeIHt0TWdFz5gJzfBrZepU43Qi99/1\njrhn+HznvOUZFymwZy7dygwd0w4OiXeGGUbeWlZPiJ9jz5cGZ816bsNjtFja1wOc\n1gN7Zl+CxWsdtX5zdt22usB2bwKBgQDGq0ChY6iderPqMDSg71wZ6z+OXvZtm0oi\ndud3jQZmcNYx+Lnwu6xUAr+e7wWzDDWChYQjS9VYoP7lJzcimaaZr5/74vkAI1i7\nUiJADxCUqnq0Lc1wb2PftEvwuoMQJ77npX6Ul/Co96R9Rx5+5WtJWjqGMiUW1hDd\n2IudNKoyswKBgFpk0kyb+6hZmzP+I+qf/KLQskR9RevpQY1Rh/ISBZzZRN/o+eoe\nkeauyBVtHLikCLruc0C4XHUnv7WANd19kxgmzTD7z489IAJU08yuJx1x+N9Hku2G\nRBY8FiDu8w47rMHQcetnAe9OjvE1SPs/hLFzR8LJUrYoRGs5KJmI1dfrAoGBALgD\n4Y5bP8/12nW9htHWQ2nig3D8tqaZYtZ/ajBK2LXEKDILHzdCrgD2tsSgwpewZFPs\nFZOX5xn7rX1VkHUk+rJ5gOcPufGNy99d2UmaapI5QgRoNFTDaC/J0Vk9eK5bEjGA\nEbnS7l+jWaGMYUvKdlBwGas5AS+gweiqbc8D++2PAoGBAKTCkq16fK8VtPYvoSAg\nMVcXrHExOpV2hO0Yb7cWYdsNkbiYoeiXSh8o9EZSpv+TIsptwi0igbnLyHI3/xNu\nwCAb2KCBQ06d3nv0eUKRcqvDFuw77nVxSXW1n5U57dg5ktlr8ESNWokRK4dUlFzJ\nE0WlTleA9EVubkLhrIA3PU/8\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-reg7t@mas50-89e2a.iam.gserviceaccount.com",
        "client_id": "117980570692247923986",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-reg7t%40mas50-89e2a.iam.gserviceaccount.com"
    }

)
firebase_admin.initialize_app(cred)


def sendPush(title: str, msg: str, registration_tokens: List[str], dataObject=None):
    # See documentation on defining a message payload.
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        tokens=registration_tokens,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send_multicast(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


def delete_firebase_user(uuid):
    auth.delete_user(uuid)
    print("Usuario eliminado exitosamente")
