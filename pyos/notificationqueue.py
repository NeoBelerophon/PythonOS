
class NotificationQueue(object):
    def __init__(self):
        self.notifications = []
        self.new = False

    def sweep(self):
        for notification in self.notifications:
            if not notification.active:
                self.notifications.remove(notification)

    def push(self, notification):
        self.notifications.insert(0, notification)
        self.new = True

    def clear(self):
        self.notifications = []