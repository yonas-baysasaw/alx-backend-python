import os
import django
import random
from faker import Faker

# --- Setup Django environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messaging_app.settings")
django.setup()

from chats.models import User, Conversation, Message  # adjust import if your app name differs

fake = Faker()


def create_users(n=5):
    """Create fake users"""
    users = []
    for _ in range(n):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="password123",  # default for testing
            phone_number=fake.phone_number(),
            role=random.choice([User.Role.GUEST, User.Role.HOST, User.Role.ADMIN]),
        )
        users.append(user)
    return users


def create_conversations(users, n=3):
    """Create fake conversations with random participants"""
    conversations = []
    for _ in range(n):
        conv = Conversation.objects.create()
        conv.participants_id.set([random.choice(users)])  # ✅ fixed
        conversations.append(conv)
    return conversations



def create_messages(users, conversations, n=10):
    """Create fake messages in conversations"""
    for _ in range(n):
        sender = random.choice(users)
        conversation = random.choice(conversations)
        Message.objects.create(
            sender_id=sender,
            message_body=fake.sentence(nb_words=10),
        )


if __name__ == "__main__":
    print("Populating database with fake data...")
    users = create_users(5)
    conversations = create_conversations(users, 3)
    create_messages(users, conversations, 20)
    print("Done ✅")
