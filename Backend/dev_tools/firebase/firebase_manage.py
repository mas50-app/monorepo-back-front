from typing import List
import firebase_admin
from firebase_admin import credentials, messaging, auth
from dotenv import load_dotenv

load_dotenv()


cred = credentials.Certificate(
    {
        "type": "service_account",
        "project_id": "mas50-89e2a",
        "private_key_id": "2ecef9cfa0cbaf5ef205491dc68fc6c92866cf7a",
        "private_key": os.environ.get("FIREBASE_PRIVATE_KEY"),
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
